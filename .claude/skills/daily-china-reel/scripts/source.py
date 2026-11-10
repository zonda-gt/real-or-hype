#!/usr/bin/env python3
"""Find and download Douyin B-roll candidates for every shot of an episode, and make one review sheet per shot.

  source.py EPISODE_DIR [--per-shot 4] [--history HISTORY.json] [--only l1a,l3b] [--kw-override "l1a=新关键词"]

For each shot ("a" and "b" of each line, "kw" = Douyin search keywords) it searches by likes, keeps
vertical clips of 4–60 s that were never used before (history.json), downloads the top N, and writes
EPISODE_DIR/sheets/<shot>.jpg: one row per candidate (aweme id on the left, a frame every 1.5 s).
Look at the sheets, then write the pick into episode.json as  "clip": "<aweme id>", "in": <seconds>.
"""
import argparse, json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(__file__))
import dy

FONT = os.path.join(os.path.dirname(__file__), "..", "..", "real-or-hype-video", "scripts", "Montserrat-ExtraBold.ttf")


def probe(p):
    o = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height:format=duration",
                        "-of", "json", p], capture_output=True, text=True).stdout
    j = json.loads(o or "{}"); s = (j.get("streams") or [{}])[0]
    return s.get("width", 0), s.get("height", 0), float((j.get("format") or {}).get("duration", 0))


def row(clip, out, label):
    w, h, d = probe(clip)
    n = 10; step = max(0.5, min(1.5, (d - 0.5) / n))
    vf = (f"fps=1/{step},scale=144:256:force_original_aspect_ratio=increase,crop=144:256,"
          f"drawtext=fontfile='{FONT}':text='%{{pts\\:gmtime\\:0\\:%S}}':x=3:y=3:fontsize=16:fontcolor=yellow:box=1:boxcolor=black@0.6,"
          f"tile={n}x1")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", clip, "-vf", vf, "-frames:v", "1", out], check=True)
    # label strip on the left
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", out, "-vf",
                    f"pad=iw+160:ih:160:0:black,drawtext=fontfile='{FONT}':text='{label}':x=6:y=10:fontsize=13:fontcolor=white,"
                    f"drawtext=fontfile='{FONT}':text='{d:.0f}s step {step:.1f}':x=6:y=34:fontsize=13:fontcolor=white", out], check=True)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("ep"); p.add_argument("--per-shot", type=int, default=4)
    p.add_argument("--history", default=os.path.join(os.path.dirname(__file__), "..", "history.json"))
    p.add_argument("--only", default=""); p.add_argument("--kw-override", action="append", default=[])
    x = p.parse_args()
    ep = json.load(open(f"{x.ep}/episode.json"))
    used = set(json.load(open(x.history)).get("used_clips", [])) if os.path.exists(x.history) else set()
    over = dict(o.split("=", 1) for o in x.kw_override)
    cache, clips = f"{x.ep}/dy_cache", f"{x.ep}/clips"
    os.makedirs(f"{x.ep}/sheets", exist_ok=True)
    taken = set()
    for ln in ep["lines"]:
        for side in ("a", "b"):
            shot = ln.get(side)
            if not shot:
                continue
            sid = ln["id"] + side
            if x.only and sid not in x.only.split(","):
                continue
            kw = over.get(sid, shot["kw"])
            print(f"== {sid}: {kw}")
            import io, contextlib
            with contextlib.redirect_stdout(io.StringIO()):
                rows = dy.search(kw, "1", cache)
            picks = []
            for a in rows:
                v = a["video"]; i = a["aweme_id"]
                w, h, d = v.get("width") or 0, v.get("height") or 0, (v.get("duration") or 0) / 1000
                if i in used or i in taken or h <= w or not (4 <= d <= 60):
                    continue
                picks.append(i)
                if len(picks) >= x.per_shot:
                    break
            if not picks:
                print("   no vertical candidates; try other keywords with --kw-override"); continue
            dy.get(picks, clips, cache)
            rows_img = []
            for i in picks:
                c = f"{clips}/{i}.mp4"
                if os.path.exists(c):
                    r = f"{x.ep}/sheets/{sid}_{i}.jpg"; row(c, r, i); rows_img.append(r); taken.add(i)
            if len(rows_img) == 1:
                os.replace(rows_img[0], f"{x.ep}/sheets/{sid}.jpg"); rows_img = []
                print("   sheet:", f"{x.ep}/sheets/{sid}.jpg")
            elif rows_img:
                args = sum([["-i", r] for r in rows_img], [])
                subprocess.run(["ffmpeg", "-v", "error", "-y", *args, "-filter_complex",
                                "".join(f"[{k}]" for k in range(len(rows_img))) + f"vstack={len(rows_img)}",
                                f"{x.ep}/sheets/{sid}.jpg"], check=True)
                for r in rows_img:
                    os.remove(r)
                print("   sheet:", f"{x.ep}/sheets/{sid}.jpg")


if __name__ == "__main__":
    main()
