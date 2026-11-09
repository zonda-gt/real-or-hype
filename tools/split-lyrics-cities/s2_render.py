"""Split-screen lyric reel: bottom half (lyrics-app recording) and audio kept exactly; top half replaced
by Chinese city clips cut on the song's drum hits.  Run in the s2/ work dir:  python s2_render.py out.mp4
"""
import sys, json, subprocess
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont

OUT = sys.argv[1]
W, H, FPS, SPLIT = 720, 1280, 30, 632          # source reel geometry; top panel = rows 0..631
OUT_W, OUT_H = 1080, 1920
FONT_CUTE = "../work/fonts/ZCOOL_Ku.ttf"
FONT_EN = "/home/user/real-or-hype/.claude/skills/real-or-hype-video/scripts/Montserrat-ExtraBold.ttf"
NAVY = (31, 38, 104)

CUTS = json.load(open("cuts.json"))["cuts"]       # snapped to the drum hits (pickcuts_s2.py)
DUR = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", "reel.mp4"],
                           capture_output=True, text=True).stdout)
# (clip, source start, city CN, city EN) - order follows the lyrics: rush hour / streets piled with cars / jammed
SEQ = [("7656406813604445691", 1.0, "上海", "Shanghai"),       # 怎么办呀 - hook: Lujiazui from above
       ("7665789076604664506", 1.5, "成都", "Chengdu"),        # Fashion Center - Taikoo Li 3D panda screen
       ("7697215322038376639", 1.0, "北京", "Beijing"),        # 高峰期的 (rush hour) - Guomao CBD traffic
       ("7687204763720674661", 4.3, "郑州", "Zhengzhou"),      # 街上堆满车子 - jammed avenue from above
       ("7702733788778487650", 6.4, "郑州", "Zhengzhou"),      # 长长的一队堵塞Max - overpass
       ("7645323101978299686", 2.5, "深圳", "Shenzhen"),
       ("7664650818422852879", 5.6, "重庆", "Chongqing"),
       ("7668294824147667930", 2.0, "广州", "Guangzhou"),
       ("7645889930825422257", 6.6, "杭州", "Hangzhou"),
       ("7657737264316175973", 1.0, "深圳", "Shenzhen"),
       ("7646710982395432226", 3.0, "长沙", "Changsha"),
       ("7656406813604445691", 10.0, "上海", "Shanghai")]       # end on the Shanghai tower 'bottle opener'
bounds = [0.0] + CUTS + [DUR]
assert len(bounds) - 1 == len(SEQ), (len(bounds) - 1, len(SEQ))
shots = [dict(src=s, st=st, cn=cn, en=en, t0=bounds[i], t1=bounds[i + 1]) for i, (s, st, cn, en) in enumerate(SEQ)]

def load_clip(sh, n):
    p = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{sh['st']:.3f}", "-i", f"dy/{sh['src']}.mp4", "-map", "0:v:0",
                        "-frames:v", str(n), "-vf", f"fps={FPS}", "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], capture_output=True)
    w, h = map(int, subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
                                    "-of", "csv=p=0", f"dy/{sh['src']}.mp4"], capture_output=True, text=True).stdout.split(","))
    fr = np.frombuffer(p.stdout, np.uint8).reshape(-1, h, w, 3)
    return np.concatenate([fr, np.repeat(fr[-1:], n - len(fr), 0)]) if len(fr) < n else fr[:n]

def cover(img, tw, th, zoom=1.0):
    h, w = img.shape[:2]
    s = max(tw / w, th / h) * zoom
    img = cv2.resize(img, (round(w * s), round(h * s)), interpolation=cv2.INTER_AREA if s < 1 else cv2.INTER_LANCZOS4)
    y0 = (img.shape[0] - th) // 2; x0 = (img.shape[1] - tw) // 2
    return img[y0:y0 + th, x0:x0 + tw]

def label_img(cn, en):
    fc = ImageFont.truetype(FONT_CUTE, 34); fe = ImageFont.truetype(FONT_EN, 20)
    d = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    b1 = d.textbbox((0, 0), cn, font=fc); b2 = d.textbbox((0, 0), en, font=fe)
    w = 34 + (b1[2] - b1[0]) + 10 + (b2[2] - b2[0]) + 22; h = 50
    im = Image.new("RGBA", (w + 6, h + 6)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((3, 3, 3 + w, 3 + h), radius=h // 2, fill=(255, 255, 255, 235), outline=NAVY, width=3)
    px, py = 3 + 22, 3 + h // 2 - 4
    d.ellipse((px - 10, py - 13, px + 10, py + 7), fill=(255, 92, 120))
    d.polygon([(px - 8, py + 1), (px + 8, py + 1), (px, py + 17)], fill=(255, 92, 120))
    d.ellipse((px - 4, py - 7, px + 4, py + 1), fill=(255, 255, 255))
    x = 3 + 38
    d.text((x - b1[0], 3 + (h - (b1[3] - b1[1])) // 2 - b1[1]), cn, font=fc, fill=NAVY)
    x += (b1[2] - b1[0]) + 10
    d.text((x - b2[0], 3 + (h - (b2[3] - b2[1])) // 2 - b2[1] + 2), en, font=fe, fill=(232, 80, 120))
    return np.asarray(im).astype(np.float32)

def blend(dst, rgba, x0, y0, scale=1.0, alpha=1.0):
    if scale != 1.0:
        rgba = cv2.resize(rgba, None, fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)
    h, w = rgba.shape[:2]
    a = rgba[:, :, 3:4] / 255 * alpha
    reg = dst[y0:y0 + h, x0:x0 + w].astype(np.float32)
    dst[y0:y0 + h, x0:x0 + w] = (rgba[:, :, :3][:, :, ::-1] * a + reg * (1 - a)).astype(np.uint8)

speak = cv2.imread("speak_overlay.png", cv2.IMREAD_UNCHANGED).astype(np.float32)   # BGRA, lifted from the original
speak = speak[:, :, [2, 1, 0, 3]]                                                     # -> RGBA for blend()
sing = cv2.imread("sing_overlay.png", cv2.IMREAD_UNCHANGED).astype(np.float32)[:, :, [2, 1, 0, 3]]
# the original's top panel grows from y=633 to y=675 at ~14.4 s (measured per frame, split.json)
SPLITS = [675 if (y >= 670 and i / FPS > 14) else 634 for i, y in enumerate(json.load(open("split.json")))]
labels = {}
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", "reel.mp4", "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], capture_output=True).stdout
reel = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
nfr = len(reel)
enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS),
                        "-i", "-", "-i", "reel.mp4", "-map", "0:v", "-map", "1:a", "-vf", f"scale={OUT_W}:{OUT_H}:flags=lanczos",
                        "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-c:a", "copy",
                        "-movflags", "+faststart", OUT], stdin=subprocess.PIPE)
cur, frames = None, None
for f in range(nfr):
    t = f / FPS
    si = max(i for i, s in enumerate(shots) if s["t0"] - 1e-6 <= t)
    sh = shots[si]
    if si != cur:
        cur = si; frames = load_clip(sh, round((sh["t1"] - sh["t0"]) * FPS) + 2)
    k = min(len(frames) - 1, f - round(sh["t0"] * FPS))
    lt = t - sh["t0"]
    z = 1 + 0.07 * max(0, 1 - lt / 0.3) ** 2                     # zoom punch on each cut
    out = reel[f].copy()
    sp = SPLITS[min(f, len(SPLITS) - 1)]
    out[:sp] = cover(frames[k], W, sp, z)
    # city label (pops when the city changes)
    first = next(s for s in shots if s["cn"] == sh["cn"] and abs(s["t1"] - sh["t0"]) < 1e-6) if si and shots[si - 1]["cn"] == sh["cn"] else sh
    lc = t - first["t0"]
    key = sh["cn"]
    if key not in labels: labels[key] = label_img(sh["cn"], sh["en"])
    pop = 1 + 0.15 * np.sin(np.pi * min(lc / 0.2, 1)) * (1 - min(lc / 0.2, 1)) * 2 if lc < 0.2 else 1.0
    lab = labels[key]; s_ = min(1, 0.7 + lc / 0.08 * 0.3) * pop
    lh, lw = lab.shape[:2]
    blend(out, lab, 20 + round(lw * (1 - s_) / 2), 24 + round(lh * (1 - s_) / 2), scale=s_, alpha=min(1, lc / 0.05))
    blend(out, speak, 190, 505)
    if sp > 640: blend(out, sing, 190, 625)      # caption straddles the moved split: put it back on top
    enc.stdin.write(out.tobytes())
enc.stdin.close(); enc.wait()
print("done", OUT, nfr, "frames")
