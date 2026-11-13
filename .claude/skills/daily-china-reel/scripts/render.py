#!/usr/bin/env python3
"""Edit an episode: B-roll cut on "go to", captions, the narration, Kevin MacLeod music ducked under it.

  render.py EPISODE_DIR [--music "Happy Bee"] [--gap 0.2] [--out final.mp4]

Needs episode.json with "clip"/"in" picked for every shot, clips/<id>.mp4 and vo/lines.json (vo.py).
Shot A ("if you like X") runs from the line's start to just before "go to"; shot B ("go to CITY") runs
to the next line. Lines without "split" get one shot. Writes EPISODE_DIR/final.mp4 (1080x1920, 30 fps,
H.264 + AAC, about -14 LUFS) and EPISODE_DIR/timeline.json.
"""
import argparse, json, os, random, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, "..", "..", "real-or-hype-video", "scripts", "Montserrat[wght].ttf")
MUSIC_DIR = os.path.join(HERE, "..", "music")
W, H, FPS = 1080, 1920, 30
YELLOW = (255, 214, 10)
# free CC BY 4.0 tracks by Kevin MacLeod (incompetech.com) that suit the format; credit in the caption
TRACKS = ["Happy Bee", "Life of Riley", "Carefree", "Wallpaper", "Inspired", "Easy Lemon", "Bright Wish",
          "Hyperfun", "Funkorama", "Sunshine A", "Pamgaea", "Merry Go"]


def run(*a):
    subprocess.run(a, check=True)


def caption_png(text, out):
    """'go to |Harbin' -> 'go to ' white + 'Harbin' yellow. Lowercase-style small caption with a soft shadow."""
    if not text:
        Image.new("RGBA", (W, H), (0, 0, 0, 0)).save(out); return
    parts = text.split("|")
    segs = [(parts[0], (255, 255, 255))] + ([(parts[1], YELLOW)] if len(parts) > 1 else [])
    f = ImageFont.truetype(FONT, 46)
    try:
        f.set_variation_by_axes([650])
    except Exception:
        pass
    widths = [f.getlength(s) for s, _ in segs]
    tw = sum(widths)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    y = int(H * 0.79) - 30
    x = (W - tw) / 2
    d, ds = ImageDraw.Draw(img), ImageDraw.Draw(sh)
    for (s, col), w in zip(segs, widths):
        ds.text((x + 2, y + 3), s, font=f, fill=(0, 0, 0, 200), stroke_width=3, stroke_fill=(0, 0, 0, 120))
        d.text((x, y), s, font=f, fill=col + (255,))
        x += w
    sh = sh.filter(ImageFilter.GaussianBlur(4))
    Image.alpha_composite(sh, img).save(out)


def overlay_png(spec, out):
    """Centered text block. spec: {"lines": [...], "size": px, "y": 0.5}. Words in [brackets] get a yellow highlight box."""
    import re
    size = spec.get("size", 90)
    f = ImageFont.truetype(FONT, size)
    try:
        f.set_variation_by_axes([800])
    except Exception:
        pass
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d, ds = ImageDraw.Draw(img), ImageDraw.Draw(sh)
    lh = int(size * 1.35)
    lines = spec["lines"]
    y = int(H * spec.get("y", 0.5) - lh * len(lines) / 2)
    pad = int(size * 0.18)
    for line in lines:
        parts = [(m, m.startswith("[")) for m in re.findall(r"\[[^\]]+\]|[^\[]+", line)]
        parts = [(t.strip("[]"), hi) for t, hi in parts]
        tw = sum(f.getlength(t) + (2 * pad if hi else 0) for t, hi in parts)
        x = (W - tw) / 2
        for t, hi in parts:
            w = f.getlength(t)
            if hi:
                box = (x, y - pad * 0.6, x + w + 2 * pad, y + size * 1.12)
                ds.rounded_rectangle(box, radius=pad, fill=(0, 0, 0, 160))
                d.rounded_rectangle(box, radius=pad, fill=YELLOW + (255,))
                d.text((x + pad, y), t, font=f, fill=(0, 0, 0, 255))
                x += w + 2 * pad
            else:
                ds.text((x + 3, y + 4), t, font=f, fill=(0, 0, 0, 220), stroke_width=6, stroke_fill=(0, 0, 0, 160))
                d.text((x, y), t, font=f, fill=(255, 255, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0, 120))
                x += w
        y += lh
    sh = sh.filter(ImageFilter.GaussianBlur(6))
    Image.alpha_composite(sh, img).save(out)


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                                capture_output=True, text=True).stdout)


def shot(src, t_in, length, cap_png, zoom, out):
    vf = (f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},"
          + (f"scale={int(W*zoom)//2*2}:{int(H*zoom)//2*2}:flags=lanczos,crop={W}:{H}," if zoom != 1 else "")
          + f"fps={FPS},setsar=1,tpad=stop_mode=clone:stop_duration=3[v];[v][1]overlay=0:0")
    run("ffmpeg", "-v", "error", "-y", "-ss", f"{t_in:.3f}", "-i", src, "-i", cap_png, "-filter_complex", vf,
        "-t", f"{length:.3f}", "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p",
        "-r", str(FPS), out)


def get_music(name):
    os.makedirs(MUSIC_DIR, exist_ok=True)
    p = os.path.join(MUSIC_DIR, name + ".mp3")
    if not os.path.exists(p):
        import requests
        r = requests.get("https://incompetech.com/music/royalty-free/mp3-royaltyfree/" + requests.utils.quote(name) + ".mp3", timeout=120)
        r.raise_for_status(); open(p, "wb").write(r.content)
    return p


def best_offset(track, cuts, total):
    """Start point in the track that puts the most beats on our cuts (no tempo change)."""
    import librosa
    y, sr = librosa.load(track, sr=22050, mono=True)
    _, beats = librosa.beat.beat_track(y=y, sr=sr, units="time")
    tlen = len(y) / sr
    best = (-1, 0.0)
    cuts = np.array(cuts)
    for off in np.arange(0, max(0.05, min(60, tlen - total - 1)), 0.05):
        b = beats[(beats >= off) & (beats <= off + total)] - off
        if len(b) == 0:
            continue
        hit = np.sum(np.min(np.abs(cuts[:, None] - b[None, :]), axis=1) < 0.07)
        if hit > best[0]:
            best = (hit, float(off))
    return best[1], int(best[0]), len(cuts)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("ep"); p.add_argument("--music", default=None); p.add_argument("--gap", type=float, default=0.2)
    p.add_argument("--lead", type=float, default=0.12); p.add_argument("--tail", type=float, default=0.7)
    p.add_argument("--music-db", type=float, default=-17.0, help="music level under the voice before ducking")
    p.add_argument("--out", default=None)
    x = p.parse_args()
    ep_path = f"{x.ep}/episode.json"
    ep = json.load(open(ep_path)); vo = json.load(open(f"{x.ep}/vo/lines.json"))
    work = f"{x.ep}/render"; os.makedirs(work, exist_ok=True)

    # 1. timeline
    t = x.lead; shots = []; voice = []
    lines = ep["lines"]
    for k, ln in enumerate(lines):
        v = vo[ln["id"]]
        voice.append((v["wav"], t))
        end = t + v["dur"] + (x.gap if k < len(lines) - 1 else x.tail)
        start = 0.0 if k == 0 else t - 0.04  # cut a hair before the word starts
        if ln.get("split", True) and ln.get("b"):
            cut = t + v["cut"] - 0.06
            shots.append((ln["a"], start, cut)); shots.append((ln["b"], cut, end - 0.04 if k < len(lines) - 1 else end))
        else:
            shots.append((ln["a"], start, end - 0.04 if k < len(lines) - 1 else end))
        t = end
    total = t
    # contiguous: each shot ends where the next starts
    for i in range(len(shots) - 1):
        shots[i] = (shots[i][0], shots[i][1], shots[i + 1][1])
    shots[-1] = (shots[-1][0], shots[-1][1], total)

    # 2. video
    parts = []
    for i, (s, a, b) in enumerate(shots):
        png = f"{work}/cap{i:02d}.png"; caption_png(s["cap"], png)
        out = f"{work}/shot{i:02d}.mp4"
        src = f"{x.ep}/clips/{s['clip']}.mp4"
        avail = dur(src) - s["in"]
        if avail < (b - a):
            print(f"note: shot {i} needs {b-a:.2f}s, clip has {avail:.2f}s after the in-point; last frame is held")
        shot(src, s["in"], b - a, png, s.get("zoom", 1.0), out)
        parts.append(out)
    open(f"{work}/concat.txt", "w").write("".join(f"file '{os.path.abspath(q)}'\n" for q in parts))
    run("ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{work}/concat.txt", "-c", "copy", f"{work}/video.mp4")

    # 3. voice track
    ins = sum([["-i", w] for w, _ in voice], [])
    fc = "".join(f"[{i}]adelay={int(st*1000)}:all=1[a{i}];" for i, (_, st) in enumerate(voice))
    fc += "".join(f"[a{i}]" for i in range(len(voice))) + f"amix=inputs={len(voice)}:normalize=0,apad,atrim=0:{total:.3f}[v]"
    run("ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", fc, "-map", "[v]", "-ar", "48000", "-ac", "1", f"{work}/voice.wav")

    # 4. music: pick a track (least recently used unless given), line its beats up with the cuts, duck it
    cuts = [a for _, a, _ in shots[1:]]
    name = x.music or ep.get("music")
    if not name:
        hist = os.path.join(HERE, "..", "history.json")
        recent = (json.load(open(hist)).get("music", []) if os.path.exists(hist) else [])[-3:]
        cands = [n for n in TRACKS if n not in recent][:4] or TRACKS[:4]
        scored = []
        for n in cands:
            off, hit, n_c = best_offset(get_music(n), cuts, total)
            scored.append((hit, n, off)); print(f"music {n}: {hit}/{n_c} cuts on a beat (start {off:.2f}s)")
        hit, name, off = max(scored)
    else:
        off, hit, n_c = best_offset(get_music(name), cuts, total); print(f"music {name}: {hit}/{n_c} cuts on a beat")
    track = get_music(name)
    fc = (f"[1]atrim={off:.3f}:{off+total:.3f},asetpts=N/SR/TB,volume={x.music_db}dB,"
          f"afade=t=in:d=0.3,afade=t=out:st={max(0,total-1.2):.3f}:d=1.2,aresample=48000,aformat=channel_layouts=stereo[m];"
          "[0]aformat=channel_layouts=stereo,asplit=2[vo][sc];"
          "[m][sc]sidechaincompress=threshold=0.02:ratio=6:attack=15:release=350:makeup=1[md];"
          "[vo][md]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[out]")
    run("ffmpeg", "-v", "error", "-y", "-i", f"{work}/voice.wav", "-i", track, "-filter_complex", fc, "-map", "[out]",
        "-ar", "48000", f"{work}/mix.wav")

    out = x.out or f"{x.ep}/final.mp4"
    # optional centered overlays (title, end card): "overlays": [{"lines": [...], "start": s, "end": e or "end", "size", "y"}]
    ov_in, ov_fc, last = [], "", "0:v"
    for i, o in enumerate(ep.get("overlays", [])):
        png = f"{work}/ov{i}.png"; overlay_png(o, png)
        a = o.get("start", 0); b = total if o.get("end", "end") == "end" else o["end"]
        if o.get("start") == "outro":  # from the start of the last shot
            a = shots[-1][1]
        ov_in += ["-loop", "1", "-t", f"{total:.3f}", "-i", png]
        ov_fc += (f"[{i+2}]format=rgba,fade=t=in:st={a:.3f}:d=0.15:alpha=1[o{i}];"
                  f"[{last}][o{i}]overlay=0:0:enable='between(t,{a:.3f},{b:.3f})'[v{i}];")
        last = f"v{i}"
    vmap = ["-filter_complex", ov_fc.rstrip(";"), "-map", f"[{last}]"] if ov_in else ["-map", "0:v"]
    run("ffmpeg", "-v", "error", "-y", "-i", f"{work}/video.mp4", "-i", f"{work}/mix.wav", *ov_in, *vmap, "-map", "1:a",
        "-c:v", "libx264", "-preset", "slow", "-crf", "21", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
        "-movflags", "+faststart", "-shortest", out)
    tl = {"total": round(total, 3), "music": name, "music_offset": off,
          "shots": [{"clip": s["clip"], "in": s["in"], "start": round(a, 3), "end": round(b, 3), "cap": s["cap"]} for s, a, b in shots]}
    json.dump(tl, open(f"{x.ep}/timeline.json", "w"), ensure_ascii=False, indent=1)
    ep["music"] = name; json.dump(ep, open(ep_path, "w"), ensure_ascii=False, indent=1)
    print(f"{out}: {total:.2f}s, {len(shots)} shots, music {name} @ {off:.2f}s, {os.path.getsize(out)/1e6:.1f} MB")


if __name__ == "__main__":
    main()
