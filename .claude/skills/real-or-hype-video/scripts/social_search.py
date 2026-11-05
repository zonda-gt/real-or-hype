#!/usr/bin/env python3
"""Find viral clips and download them through TikHub (Douyin, TikTok, Instagram, Xiaohongshu).

  social_search.py search douyin "上海 网红商场" [--pages 2] [--sort likes|new] [--recent day|week|half_year] [-o res.json]
  social_search.py plays res.json            # Douyin only: real play counts ($0.025 per 20 videos)
  social_search.py download res.json <id> [<id> ...] [-d DIR]
  social_search.py download res.json --top 3 [-d DIR]
  social_search.py link <post URL> [-d DIR]   # one post from a link: stats + download

The key is a network secret on the cloud environment: the proxy adds it to requests to
api.tikhub.io, so no variable is needed. Elsewhere, set TIKHUB_API_KEY.
Prices per successful call (failed calls are free): Douyin search $0.01, TikTok search $0.001,
Instagram search $0.002, Xiaohongshu search $0.01, one post $0.001 ($0.01 Xiaohongshu).
Downloading the file from the platform's CDN costs nothing. CDN links expire after a few hours;
`download` re-fetches the post (one detail call) when a saved link no longer works.
"""
import argparse, json, os, re, subprocess, sys, time, urllib.parse, urllib.request

API = "https://api.tikhub.io"
KEY = os.environ.get("TIKHUB_API_KEY") or "proxy-injected"
UA = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"
PLATFORMS = ("douyin", "tiktok", "instagram", "xhs")


def call(path, params=None, body=None, tries=3):
    url = API + path + ("?" + urllib.parse.urlencode(params) if params else "")
    data = json.dumps(body).encode() if body is not None else None
    last = None
    for i in range(tries):
        req = urllib.request.Request(url, data=data, headers={
            "Authorization": "Bearer " + KEY, "Content-Type": "application/json",
            "User-Agent": "real-or-hype/1.0"})  # Cloudflare blocks Python's default agent (error 1010)
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.load(r)["data"]
        except urllib.error.HTTPError as e:
            last = f"HTTP {e.code}: {e.read()[:300].decode('utf-8', 'replace')}"
            if e.code in (401, 402, 403):
                break
        except Exception as e:  # network hiccup
            last = repr(e)
        time.sleep(2 * (i + 1))
    sys.exit(f"TikHub {path} failed: {last}")


def walk(o, pred):
    if isinstance(o, dict):
        if pred(o):
            yield o
            return
        for v in o.values():
            yield from walk(v, pred)
    elif isinstance(o, list):
        for v in o:
            yield from walk(v, pred)


def find_key(o, key):
    for d in walk(o, lambda x: key in x and not isinstance(x[key], (dict, list))):
        return d[key]


# ---------- normalisers: every platform -> one flat record ----------

def norm_aweme(a, platform):
    s = a.get("statistics") or {}
    v = a.get("video") or {}
    cands = []
    for b in v.get("bit_rate") or []:
        p = b.get("play_addr") or {}
        if p.get("url_list"):
            cands.append(((p.get("width") or 0) * (p.get("height") or 0), p))
    best = max(cands, key=lambda c: c[0])[1] if cands else (v.get("play_addr") or {})
    au = a.get("author") or {}
    handle = au.get("unique_id") or au.get("short_id") or au.get("uid")
    url = (f"https://www.tiktok.com/@{handle}/video/{a['aweme_id']}" if platform == "tiktok"
           else f"https://www.douyin.com/video/{a['aweme_id']}")
    return {
        "platform": platform, "id": str(a["aweme_id"]), "url": url,
        "title": (a.get("desc") or "").strip(), "author": au.get("nickname"),
        "followers": au.get("follower_count"), "created": a.get("create_time"),
        "duration_s": round((v.get("duration") or 0) / 1000, 1) or None,
        "plays": s.get("play_count") or None,  # Douyin search returns 0: use `plays`
        "likes": s.get("digg_count"), "comments": s.get("comment_count"),
        "saves": s.get("collect_count"), "shares": s.get("share_count"),
        "video_urls": best.get("url_list") or [], "audio_urls": [],
        "res": f"{best.get('width')}x{best.get('height')}" if best.get("width") else None,
    }


def norm_ig(m):
    vv = sorted(m.get("video_versions") or [], key=lambda x: (x.get("width") or 0) * (x.get("height") or 0), reverse=True)
    cap = m.get("caption")
    cap = cap.get("text", "") if isinstance(cap, dict) else (cap or "")
    if not cap:  # GraphQL-shaped responses (post by link)
        edges = (m.get("edge_media_to_caption") or {}).get("edges") or [{}]
        cap = (edges[0].get("node") or {}).get("text", "")
    u = m.get("user") or m.get("owner") or {}
    code = m.get("code") or m.get("shortcode")
    return {
        "platform": "instagram", "id": code, "url": f"https://www.instagram.com/reel/{code}/",
        "title": cap.strip(), "author": u.get("username"), "followers": u.get("follower_count"),
        "created": m.get("taken_at") or m.get("taken_at_timestamp"),
        "duration_s": round(m["video_duration"], 1) if m.get("video_duration") else None,
        "plays": m.get("play_count") or m.get("ig_play_count") or m.get("video_play_count") or m.get("video_view_count"),
        "likes": m.get("like_count") if m.get("like_count") is not None else (m.get("edge_media_preview_like") or {}).get("count"),
        "comments": m.get("comment_count") if m.get("comment_count") is not None
                    else (m.get("edge_media_to_comment") or m.get("edge_media_preview_comment") or {}).get("count"),
        "saves": None, "shares": m.get("reshare_count"),
        "video_urls": [x["url"] for x in vv[:1]] or ([m["video_url"]] if m.get("video_url") else []),
        "audio_urls": [], "res": f"{vv[0].get('width')}x{vv[0].get('height')}" if vv else None,
    }


def norm_xhs(n):
    media = ((n.get("video_info_v2") or {}).get("media") or {})
    streams = [x for v in (media.get("stream") or {}).values() for x in v if x.get("master_url")]
    muxed = [x for x in streams if x.get("format") == "mp4"]  # these carry their own audio
    best = max(streams, key=lambda x: (x.get("width") or 0) * (x.get("height") or 0), default=None)
    audio = []
    if best is not None and best.get("format") != "mp4":  # fmp4 streams are video-only
        aac = (media.get("audio_stream") or {}).get("AAC") or []
        if aac:
            a = max(aac, key=lambda x: x.get("audio_bitrate") or 0)
            audio = [a["master_url"]] + (a.get("backup_urls") or [])
        elif muxed:
            best = max(muxed, key=lambda x: (x.get("width") or 0) * (x.get("height") or 0))
    u = n.get("user") or {}
    dur = (n.get("video_info_v2") or {}).get("capa", {}).get("duration")
    return {
        "platform": "xhs", "id": n["id"], "url": f"https://www.xiaohongshu.com/explore/{n['id']}",
        "xsec_token": n.get("xsec_token"),
        "title": (n.get("desc") or "") if (n.get("desc") or "").startswith(n.get("title") or "\0")
                 else ((n.get("title") or "") + " " + (n.get("desc") or "")).strip(),
        "author": u.get("nickname"), "followers": None, "created": n.get("timestamp"),
        "duration_s": dur, "plays": None,  # Xiaohongshu never exposes plays
        "likes": n.get("liked_count"), "comments": n.get("comments_count"),
        "saves": n.get("collected_count"), "shares": n.get("shared_count"),
        "video_urls": ([best["master_url"]] + (best.get("backup_urls") or [])) if best else [],
        "audio_urls": audio, "res": f"{best.get('width')}x{best.get('height')}" if best else None,
    }


def extract(platform, data):
    if platform in ("douyin", "tiktok"):
        items = walk(data, lambda o: "aweme_id" in o and "statistics" in o)
        return [norm_aweme(a, platform) for a in items]
    if platform == "instagram":
        items = walk(data, lambda o: ("code" in o or "shortcode" in o) and ("video_versions" in o or "video_url" in o))
        return [norm_ig(m) for m in items]
    items = walk(data, lambda o: o.get("type") == "video" and "video_info_v2" in o and "id" in o)
    return [norm_xhs(n) for n in items]


# ---------- search ----------

def search(platform, kw, pages, sort, recent):
    out, state = [], {}
    for page in range(pages):
        if platform == "douyin":
            body = {"keyword": kw, "cursor": state.get("cursor", 0),
                    "sort_type": {"likes": "1", "new": "2"}.get(sort, "0"),
                    "publish_time": {"day": "1", "week": "7", "half_year": "180"}.get(recent, "0"),
                    "filter_duration": "0", "content_type": "1",
                    "search_id": state.get("search_id", ""), "backtrace": state.get("backtrace", "")}
            d = call("/api/v1/douyin/search/fetch_video_search_v2", body=body)
            state = {"cursor": find_key(d.get("business_config", d), "cursor") or 0,
                     "search_id": find_key(d.get("business_config", d), "search_id") or "",
                     "backtrace": find_key(d.get("business_config", d), "backtrace") or ""}
        elif platform == "tiktok":
            p = {"keyword": kw, "offset": state.get("cursor", 0), "count": 20,
                 "sort_type": {"likes": 1}.get(sort, 0),  # TikTok has no "newest" sort
                 "publish_time": {"day": 1, "week": 7, "half_year": 180}.get(recent, 0), "region": "US"}
            d = call("/api/v1/tiktok/app/v3/fetch_video_search_result", params=p)
            state = {"cursor": find_key(d, "cursor") or 0}
        elif platform == "instagram":
            p = {"keyword": kw}
            if state.get("token"):
                p["pagination_token"] = state["token"]
            d = call("/api/v1/instagram/v2/search_reels", params=p)
            state = {"token": find_key(d, "pagination_token")}
        else:
            p = {"keyword": kw, "page": page + 1, "note_type": "视频笔记",
                 "sort_type": {"likes": "popularity_descending", "new": "time_descending"}.get(sort, "general"),
                 "time_filter": {"day": "一天内", "week": "一周内", "half_year": "半年内"}.get(recent, "不限")}
            p.update({k: v for k, v in state.items() if v})
            d = call("/api/v1/xiaohongshu/app_v2/search_notes", params=p)
            state = {"search_id": find_key(d, "search_id"), "search_session_id": find_key(d, "search_session_id")}
        got = extract(platform, d)
        print(f"page {page + 1}: {len(got)} videos", file=sys.stderr)
        out += got
        if not got or not any(state.values()):
            break
    seen, uniq = set(), []
    for r in out:
        if r["id"] not in seen:
            seen.add(r["id"])
            uniq.append(r)
    return uniq


def rank_key(r):
    return (r["plays"] or 0, r["likes"] or 0)


def show(rows):
    print(f"{'plays':>10} {'likes':>8} {'saves':>7} {'shares':>7} {'cmts':>6} {'dur':>5}  id / title")
    for r in rows:
        f = lambda x: "-" if x is None else f"{x:,}"
        print(f"{f(r['plays']):>10} {f(r['likes']):>8} {f(r['saves']):>7} {f(r['shares']):>7} "
              f"{f(r['comments']):>6} {f(r['duration_s']):>5}  {r['id']}  {r['title'][:50]!s}".replace("\n", " "))


# ---------- play counts (Douyin) ----------

def fill_plays(rows):
    dy = [r for r in rows if r["platform"] == "douyin"]
    for i in range(0, len(dy), 20):
        chunk = dy[i:i + 20]
        d = call("/api/v1/douyin/app/v3/fetch_multi_video_statistics",
                 params={"aweme_ids": ",".join(r["id"] for r in chunk)})
        stats = {str(s.get("aweme_id")): s for s in walk(d, lambda o: "aweme_id" in o and "play_count" in o)}
        for r in chunk:
            s = stats.get(r["id"])
            if s:
                r["plays"] = s.get("play_count")


# ---------- detail (re-fetch for fresh links, or start from a link) ----------

def detail(platform, rec=None, link=None):
    if platform in ("douyin", "tiktok"):
        base = f"/api/v1/{platform}/app/v3/"
        d = (call(base + "fetch_one_video", params={"aweme_id": rec["id"]}) if rec
             else call(base + "fetch_one_video_by_share_url", params={"share_url": link}))
    elif platform == "instagram":
        d = call("/api/v1/instagram/v1/fetch_post_by_url", params={"post_url": link or rec["url"]})
    else:
        p = {"note_id": rec["id"]} if rec else {"share_text": link}
        d = call("/api/v1/xiaohongshu/app_v2/get_video_note_detail", params=p)
    got = extract(platform, d)
    if rec:
        got = [g for g in got if g["id"] == rec["id"]] or got
    if not got:
        sys.exit(f"No video found in the {platform} detail response (deleted, private or not a video?)")
    return got[0]


def platform_of(link):
    for pat, p in (("douyin", "douyin"), ("tiktok", "tiktok"), ("instagram", "instagram"),
                   ("xiaohongshu|xhslink", "xhs")):
        if re.search(pat, link):
            return p
    sys.exit("Unknown link: expected Douyin, TikTok, Instagram or Xiaohongshu")


# ---------- download ----------

def fetch(urls, dest):
    for u in urls:
        try:
            req = urllib.request.Request(u, headers={"User-Agent": UA, "Referer": "https://www.xiaohongshu.com/" if "xhscdn" in u else ""})
            with urllib.request.urlopen(req, timeout=300) as r, open(dest, "wb") as f:
                while chunk := r.read(1 << 20):
                    f.write(chunk)
            if os.path.getsize(dest) > 10_000:
                return True
        except Exception as e:
            print(f"  link failed ({e})", file=sys.stderr)
    return False


def download(rec, outdir, refetch=True):
    os.makedirs(outdir, exist_ok=True)
    dest = os.path.join(outdir, f"{rec['platform']}_{rec['id']}.mp4")
    vtmp, atmp = dest + ".video", dest + ".audio"
    ok = fetch(rec["video_urls"], vtmp) and (not rec["audio_urls"] or fetch(rec["audio_urls"], atmp))
    if not ok and refetch:
        print("  saved link expired; fetching the post again", file=sys.stderr)
        fresh = detail(rec["platform"], rec=rec)
        rec.update({k: fresh[k] for k in ("video_urls", "audio_urls", "res")})
        ok = fetch(rec["video_urls"], vtmp) and (not rec["audio_urls"] or fetch(rec["audio_urls"], atmp))
    if not ok:
        sys.exit(f"Could not download {rec['url']}")
    if rec["audio_urls"]:
        cmd = ["ffmpeg", "-v", "error", "-y", "-i", vtmp, "-i", atmp, "-map", "0:v:0", "-map", "1:a:0", "-c", "copy", dest]
    else:
        cmd = ["ffmpeg", "-v", "error", "-y", "-i", vtmp, "-c", "copy", "-movflags", "+faststart", dest]
    subprocess.run(cmd, check=True)
    for t in (vtmp, atmp):
        if os.path.exists(t):
            os.remove(t)
    with open(dest[:-4] + ".json", "w", encoding="utf-8") as f:
        json.dump({k: v for k, v in rec.items() if k not in ("video_urls", "audio_urls")}, f, ensure_ascii=False, indent=1)
    print(f"saved {dest} ({os.path.getsize(dest) / 1e6:.1f} MB, {rec.get('res')})  {rec['url']}")
    return dest


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search")
    s.add_argument("platform", choices=PLATFORMS)
    s.add_argument("keyword")
    s.add_argument("--pages", type=int, default=1)
    s.add_argument("--sort", choices=("default", "likes", "new"), default="default")
    s.add_argument("--recent", choices=("any", "day", "week", "half_year"), default="any")
    s.add_argument("-o", "--out")
    s.add_argument("--plays", action="store_true", help="Douyin: also fetch real play counts")
    p = sub.add_parser("plays")
    p.add_argument("results")
    d = sub.add_parser("download")
    d.add_argument("results")
    d.add_argument("ids", nargs="*")
    d.add_argument("--top", type=int)
    d.add_argument("-d", "--dir", default="viral")
    l = sub.add_parser("link")
    l.add_argument("url")
    l.add_argument("-d", "--dir", default="viral")
    a = ap.parse_args()

    if a.cmd == "search":
        rows = search(a.platform, a.keyword, a.pages, a.sort, a.recent)
        if a.plays and a.platform == "douyin":
            fill_plays(rows)
        rows.sort(key=rank_key, reverse=True)
        out = a.out or f"search_{a.platform}_{re.sub(r'[^0-9A-Za-z一-鿿]+', '_', a.keyword)}.json"
        with open(out, "w", encoding="utf-8") as f:
            json.dump(rows, f, ensure_ascii=False, indent=1)
        show(rows)
        print(f"\n{len(rows)} videos -> {out}")
    elif a.cmd == "plays":
        rows = json.load(open(a.results, encoding="utf-8"))
        fill_plays(rows)
        rows.sort(key=rank_key, reverse=True)
        json.dump(rows, open(a.results, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        show(rows)
    elif a.cmd == "download":
        rows = json.load(open(a.results, encoding="utf-8"))
        pick = [r for r in rows if r["id"] in a.ids] if a.ids else sorted(rows, key=rank_key, reverse=True)[:a.top or 1]
        if not pick:
            sys.exit("No matching ids in " + a.results)
        for r in pick:
            download(r, a.dir)
        json.dump(rows, open(a.results, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    else:
        plat = platform_of(a.url)
        rec = detail(plat, link=a.url)
        if plat == "douyin":
            fill_plays([rec])
        show([rec])
        download(rec, a.dir, refetch=False)


if __name__ == "__main__":
    main()
