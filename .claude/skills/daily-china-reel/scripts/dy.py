#!/usr/bin/env python3
"""Douyin B-roll via TikHub (the proxy injects the key).

  dy.py search "<关键词>" [--sort 1] [--cache DIR]   list vertical clips < 1 min (sort 0=relevance 1=likes 2=latest)
  dy.py get ID[,ID...] OUTDIR [--cache DIR]          download clips (H.264) found in earlier searches
  dy.py sheet CLIP.mp4 OUT.jpg [--every 1]           contact sheet with timestamps, to pick in-points

Search results are cached as JSON in --cache (default ./dy_cache) so `get` can find the play URLs.
"""
import argparse, glob, json, os, re, subprocess, sys, time, hashlib
import requests

API = "https://api.tikhub.io/api/v1/douyin/search/fetch_video_search_v2"
DETAIL = "https://api.tikhub.io/api/v1/douyin/web/fetch_one_video"
HDR = {"Authorization": "Bearer " + os.environ.get("TIKHUB_API_KEY", "x")}


def walk(o):
    if isinstance(o, dict):
        if "aweme_id" in o and "video" in o:
            yield o
        else:
            for v in o.values():
                yield from walk(v)
    elif isinstance(o, list):
        for v in o:
            yield from walk(v)


def search(kw, sort, cache, publish_time="0"):
    os.makedirs(cache, exist_ok=True)
    body = {"keyword": kw, "cursor": 0, "sort_type": sort, "publish_time": publish_time,
            "filter_duration": "0-1", "content_type": "1", "search_id": "", "backtrace": ""}
    j = {}
    for i in range(4):
        try:
            r = requests.post(API, json=body, headers=HDR, timeout=90)
            if r.status_code == 200:
                j = r.json(); break
            print("tikhub", r.status_code, r.text[:120], file=sys.stderr)
        except requests.RequestException as e:
            print("tikhub", e, file=sys.stderr)
        time.sleep(2 ** (i + 1))
    name = hashlib.md5(f"{kw}|{sort}".encode()).hexdigest()[:10]
    json.dump({"keyword": kw, "resp": j}, open(f"{cache}/{name}.json", "w"), ensure_ascii=False)
    seen, rows = set(), []
    for a in walk(j.get("data")):
        if a["aweme_id"] in seen:
            continue
        seen.add(a["aweme_id"])
        v = a["video"]; st = a.get("statistics", {})
        w, h = v.get("width") or 0, v.get("height") or 0
        rows.append(a)
        print(a["aweme_id"], f"{w}x{h}", f"{(v.get('duration') or 0)/1000:.1f}s",
              "likes", st.get("digg_count"), "|", (a.get("desc") or "")[:70].replace("\n", " "))
    if not rows:
        print("no results", (j.get("message") or "")[:100])
    return rows


def find(ids, cache):
    found = {}
    for f in glob.glob(f"{cache}/*.json"):
        d = json.load(open(f))
        for a in walk((d.get("resp") or {}).get("data")):
            if a["aweme_id"] in ids:
                found[a["aweme_id"]] = a
    for i in ids:  # not in a cached search: ask TikHub for the single video
        if i in found:
            continue
        try:
            r = requests.get(DETAIL, params={"aweme_id": i}, headers=HDR, timeout=60)
            for a in walk(r.json().get("data")):
                if a["aweme_id"] == i:
                    found[i] = a; break
        except Exception as e:
            print(i, "detail failed", e, file=sys.stderr)
    return found


def get(ids, outdir, cache):
    os.makedirs(outdir, exist_ok=True)
    found = find(ids, cache)
    meta_path = f"{outdir}/meta.json"
    meta = json.load(open(meta_path)) if os.path.exists(meta_path) else {}
    for i in ids:
        out = f"{outdir}/{i}.mp4"
        if os.path.exists(out) and os.path.getsize(out) > 100000:
            continue
        a = found.get(i)
        if not a:
            print(i, "NOT FOUND"); continue
        v = a["video"]
        cands = []
        for br in v.get("bit_rate") or []:
            pa = br.get("play_addr") or {}
            if "bvc2" in (br.get("gear_name") or "") or br.get("is_bytevc1") == 2:
                continue
            cands.append(((pa.get("height") or 0) * (pa.get("width") or 0), br.get("bit_rate", 0), pa.get("url_list", [])))
        cands.sort(key=lambda c: (-c[0], -c[1]))
        # ByteVC2 streams do not decode in ffmpeg, so try the H.264 address first
        urls = (v.get("play_addr_h264") or {}).get("url_list", []) + [u for c in cands for u in c[2]] \
            + (v.get("play_addr") or {}).get("url_list", [])
        ok = False
        for u in urls:
            try:
                r = requests.get(u, headers={"User-Agent": "Mozilla/5.0", "Referer": "https://www.douyin.com/"}, timeout=90)
                if r.status_code == 200 and len(r.content) > 100000 and r.content[4:8] == b"ftyp":
                    open(out, "wb").write(r.content)
                    codec = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                                            "stream=codec_name,width,height", "-of", "csv=p=0", out],
                                           capture_output=True, text=True).stdout.strip()
                    if not codec or codec.startswith(("bytevc2", "vvc")):
                        os.remove(out); continue
                    ok = True; break
            except Exception:
                pass
        meta[i] = {"desc": a.get("desc"), "author": (a.get("author") or {}).get("nickname"),
                   "likes": (a.get("statistics") or {}).get("digg_count"), "ok": ok,
                   "url": f"https://www.douyin.com/video/{i}"}
        print(i, "ok" if ok else "FAILED", meta[i]["author"], codec if ok else "")
    json.dump(meta, open(meta_path, "w"), ensure_ascii=False, indent=1)


def sheet(clip, out, every):
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", clip],
                               capture_output=True, text=True).stdout.strip() or 0)
    n = max(1, min(30, int(dur / every)))
    cols = 6; rows = (n + cols - 1) // cols
    vf = (f"fps=1/{every},scale=200:-2,drawtext=text='%{{pts\\:hms}}':x=4:y=4:fontsize=18:fontcolor=yellow:box=1:boxcolor=black@0.6,"
          f"tile={cols}x{rows}")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", clip, "-vf", vf, "-frames:v", "1", out], check=True)
    print(out, f"{dur:.1f}s")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("cmd"); p.add_argument("a"); p.add_argument("b", nargs="?")
    p.add_argument("--sort", default="1"); p.add_argument("--cache", default="dy_cache")
    p.add_argument("--every", type=float, default=1.0); p.add_argument("--publish-time", default="0")
    x = p.parse_args()
    if x.cmd == "search":
        search(x.a, x.sort, x.cache, x.publish_time)
    elif x.cmd == "get":
        get([i for i in x.a.split(",") if i], x.b, x.cache)
    elif x.cmd == "sheet":
        sheet(x.a, x.b, x.every)
    else:
        sys.exit(__doc__)
