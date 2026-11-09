"""Composite: Douyin place clips cut to the beat + cut-out character + lyric subtitles + place labels.
Run from the work dir:  python render.py out.mp4 [preview_seconds]
"""
import sys, os, json, subprocess, glob
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
BEAT = 0.66667                     # 90 BPM, phase 0 (fitted to kick + lyric-change onsets)
BAR = 4 * BEAT
SONG_DUR = 29.833
OUT = sys.argv[1]
PREVIEW = float(sys.argv[2]) if len(sys.argv) > 2 else None
FONT_CN = "fonts/Noto_San.ttf"           # Noto Sans SC Black
FONT_CUTE = "fonts/ZCOOL_Ku.ttf"
FONT_EN = "/home/user/real-or-hype/.claude/skills/real-or-hype-video/scripts/Montserrat-ExtraBold.ttf"
NAVY = (31, 38, 104)

# ---- places: one per bar; each bar = shots (src, start, n_beats) -------------
P = {
 "panda": "7704258711699220687", "redpanda": "7643117918070514673", "hz": "7654209858460714344",
 "xm": "7665601807955632457", "hf": "7696465235804855281", "py": "7685187711413607281",
 "dt": "7698644721291301042", "wx": "7704836276721744233", "ly": "7673892305191884282",
 "rz": "7664818114395980970", "yx": "7690214385700574323"}
BARS = [
 ("重庆动物园", "Chongqing Zoo",        [("panda", 2.0, 2), ("panda", 5.0, 2)]),
 ("成都熊猫谷", "Chengdu Panda Valley", [("redpanda", 12.0, 2), ("redpanda", 2.0, 2)]),
 ("杭州 · 鹿野森谷", "Hangzhou",        [("hz", 0.5, 2), ("hz", 9.0, 2)]),
 ("厦门", "Xiamen, Fujian",            [("xm", 2.05, 2), ("xm", 5.15, 2)]),
 ("合肥 · 粉黛花海", "Hefei, Anhui",     [("hf", 0.3, 1), ("hf", 2.0, 1), ("hf", 5.1, 1), ("hf", 6.8, 1)]),
 ("鄱阳湖", "Poyang Lake, Jiangxi",     [("py", 0.2, 2), ("py", 4.0, 2)]),
 ("大同古城", "Datong, Shanxi",          [("dt", 4.5, 2), ("dt", 9.5, 2)]),
 ("望仙谷", "Wangxian Valley, Jiangxi", [("wx", 4.0, 2), ("wx", 13.4, 2)]),
 ("龙岩 · 童话森林", "Longyan, Fujian",  [("ly", 1.0, 2), ("ly", 5.0, 2)]),
 ("日照 · 童话小镇", "Rizhao, Shandong", [("rz", 1.0, 2), ("rz", 4.0, 2)]),
 ("宜兴 · 窑湖小镇", "Yixing, Jiangsu",  [("yx", 0.6, 2), ("yx", 6.5, None)]),   # None = to the end
]
LYRICS = {"A": ("我真的特别爱你", "I really do love you so much"),
          "B": ("为什么你会流泪", "Why did you cry?"),
          "C": ("答应我不再流泪", "Promise me you won't cry anymore"),
          "D": ("在这世界", "In this world"),
          "E": ("没有多少的时间", "There isn't much time"),
          "F": ("能让我对你思念", "Making me endlessly long for you")}
# measured from the reel's own burned-in lyrics (frame classification), gaps < 0.4 s closed
LYR_T = [("A", 0.2, 2.2), ("B", 2.2, 7.4), ("A", 7.4, 9.333), ("C", 9.333, 10.967), ("D", 10.967, 12.133),
         ("E", 12.133, 13.9), ("F", 13.9, 15.067), ("A", 15.067, 16.4), ("B", 16.4, 21.367), ("A", 21.367, 23.333),
         ("C", 23.333, 24.933), ("D", 24.933, 26.133), ("E", 26.133, 27.867), ("F", 27.867, 29.6)]

# ---- shot list on the beat grid ---------------------------------------------
shots, t = [], 0.0
for bi, (cn, en, ss) in enumerate(BARS):
    for (k, st, nb) in ss:
        dur = (SONG_DUR - t) if nb is None else nb * BEAT
        shots.append(dict(src=P[k], st=st, t0=t, t1=t + dur, bar=bi))
        t += dur
assert abs(t - SONG_DUR) < 1e-6, t
json.dump(shots, open("shots.json", "w"), indent=1)

# ---- frame readers -------------------------------------------------------------
def cover(img):
    h, w = img.shape[:2]
    s = max(W / w, H / h)
    img = cv2.resize(img, (round(w * s), round(h * s)), interpolation=cv2.INTER_LANCZOS4)
    y0 = (img.shape[0] - H) // 2; x0 = (img.shape[1] - W) // 2
    return img[y0:y0 + H, x0:x0 + W]

def load_shot(sh):
    n = round((sh["t1"] - sh["t0"]) * FPS)
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{sh['st']:.3f}", "-i", f"dy/{sh['src']}.mp4", "-map", "0:v:0",
           "-frames:v", str(n), "-vf", f"fps={FPS}", "-f", "rawvideo", "-pix_fmt", "bgr24", "-"]
    p = subprocess.run(cmd, capture_output=True)
    w, h = map(int, subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
        "stream=width,height", "-of", "csv=p=0", f"dy/{sh['src']}.mp4"], capture_output=True, text=True).stdout.strip().split(","))
    fr = np.frombuffer(p.stdout, np.uint8).reshape(-1, h, w, 3)
    if len(fr) < n:
        fr = np.concatenate([fr, np.repeat(fr[-1:], n - len(fr), 0)])
    return fr[:n]

# ---- character -----------------------------------------------------------------
CROP_X, CROP_Y = 0, 40        # frames/ were cropped 440x560 at (0,40) from the 720x720 reel
def char_rgba(i):
    rgb = cv2.imread(f"frames/{i:04d}.png")[:, :, ::-1]
    a = cv2.imread(f"alpha/{i:04d}.png", cv2.IMREAD_GRAYSCALE).astype(np.float32) / 255
    return rgb, a

# figure bbox over the whole clip, to centre and scale it
NFR = len(glob.glob("alpha/*.png"))
xs0, ys0, xs1, ys1 = [], [], [], []
for i in range(1, NFR + 1, 10):
    _, a = char_rgba(i)
    yy, xx = np.where(a > 0.5)
    xs0.append(xx.min()); xs1.append(xx.max()); ys0.append(yy.min()); ys1.append(yy.max())
bx0, bx1, by0, by1 = np.median(xs0), np.median(xs1), np.median(ys0), np.median(ys1)
fig_h = by1 - by0
CH_SCALE = 600 / fig_h                     # figure ~600 px tall
FEET_Y = 1385                              # feet line in output
CX = 300
print("figure bbox", bx0, bx1, by0, by1, "scale", CH_SCALE)

# ---- text overlays (PIL RGBA) ----------------------------------------------------
def text_img(lines, pad=30):
    """lines: list of (text, font, fill, stroke_w, stroke_col, gap_after)"""
    tmp = Image.new("RGBA", (10, 10)); d = ImageDraw.Draw(tmp)
    sizes = [d.textbbox((0, 0), t, font=f, stroke_width=sw) for (t, f, _, sw, _, _) in lines]
    w = max(b[2] - b[0] for b in sizes) + 2 * pad
    h = sum(b[3] - b[1] + g for b, (*_, g) in zip(sizes, lines)) + 2 * pad
    im = Image.new("RGBA", (w, h)); d = ImageDraw.Draw(im)
    y = pad
    for b, (t, f, fill, sw, sc, g) in zip(sizes, lines):
        x = (w - (b[2] - b[0])) // 2 - b[0]
        d.text((x, y - b[1]), t, font=f, fill=fill, stroke_width=sw, stroke_fill=sc)
        y += b[3] - b[1] + g
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); sh.putalpha(im.split()[3].point(lambda v: v * 0.45))
    sh = sh.filter(ImageFilter.GaussianBlur(6))
    out = Image.new("RGBA", im.size); out.alpha_composite(sh, (0, 5)); out.alpha_composite(im)
    return out

fcn = ImageFont.truetype(FONT_CN, 92); fen = ImageFont.truetype(FONT_EN, 44)
SUB = {k: text_img([(cn, fcn, (255, 255, 255), 9, NAVY, 14), (en, fen, (255, 236, 150), 6, NAVY, 0)])
       for k, (cn, en) in LYRICS.items()}

def label_img(cn, en):
    fc = ImageFont.truetype(FONT_CUTE, 62); fe = ImageFont.truetype(FONT_EN, 34)
    d = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    b1 = d.textbbox((0, 0), cn, font=fc); b2 = d.textbbox((0, 0), en, font=fe)
    pin = 54
    tw = max(b1[2] - b1[0], b2[2] - b2[0])
    w = tw + pin + 90; h = (b1[3] - b1[1]) + (b2[3] - b2[1]) + 62
    im = Image.new("RGBA", (w + 20, h + 20)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((10, 10, 10 + w, 10 + h), radius=h // 2, fill=(255, 255, 255, 238), outline=NAVY, width=5)
    # pin icon
    px, py = 10 + 40, 10 + h // 2 - 8
    d.ellipse((px - 20, py - 26, px + 20, py + 14), fill=(255, 92, 120))
    d.polygon([(px - 17, py + 2), (px + 17, py + 2), (px, py + 34)], fill=(255, 92, 120))
    d.ellipse((px - 8, py - 14, px + 8, py + 2), fill=(255, 255, 255))
    tx = 10 + pin + 50
    d.text((tx - b1[0], 10 + 22 - b1[1]), cn, font=fc, fill=NAVY)
    d.text((tx - b2[0], 10 + 22 + (b1[3] - b1[1]) + 12 - b2[1]), en, font=fe, fill=(232, 80, 120))
    return im

LABELS = [label_img(cn, en) for (cn, en, _) in BARS]

def paste_rgba(dst, im, cx, cy, scale=1.0, alpha=1.0):
    if scale != 1.0:
        im = im.resize((max(1, round(im.width * scale)), max(1, round(im.height * scale))), Image.LANCZOS)
    a = np.asarray(im).astype(np.float32)
    x0 = round(cx - a.shape[1] / 2); y0 = round(cy - a.shape[0] / 2)
    blend(dst, a[:, :, :3][:, :, ::-1], a[:, :, 3] / 255 * alpha, x0, y0)

def blend(dst, rgb_bgr, al, x0, y0):
    h, w = al.shape
    sx0, sy0 = max(0, -x0), max(0, -y0)
    dx0, dy0 = max(0, x0), max(0, y0)
    dx1, dy1 = min(W, x0 + w), min(H, y0 + h)
    if dx1 <= dx0 or dy1 <= dy0: return
    a = al[sy0:sy0 + dy1 - dy0, sx0:sx0 + dx1 - dx0, None]
    s = rgb_bgr[sy0:sy0 + dy1 - dy0, sx0:sx0 + dx1 - dx0]
    reg = dst[dy0:dy1, dx0:dx1].astype(np.float32)
    dst[dy0:dy1, dx0:dx1] = (s * a + reg * (1 - a)).astype(np.uint8)

def ease_pop(x):          # 0..1 -> overshoot pop
    x = min(max(x, 0), 1)
    return 1 + 0.12 * np.sin(np.pi * x) * (1 - x) * 2 if x < 1 else 1.0

# ---- render ------------------------------------------------------------------------
dur = PREVIEW or SONG_DUR
nframes = round(dur * FPS)
enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS),
        "-i", "-", "-i", "reel.mp4", "-map", "0:v", "-map", "1:a", "-t", f"{dur:.3f}",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", OUT], stdin=subprocess.PIPE)

cur_shot, cur_frames = None, None
for f in range(nframes):
    t = f / FPS
    si = next(i for i, s in enumerate(shots) if s["t0"] - 1e-6 <= t < s["t1"] - 1e-6 or i == len(shots) - 1)
    if si != cur_shot:
        cur_shot, cur_frames = si, load_shot(shots[si])
    sh = shots[si]
    k = min(len(cur_frames) - 1, f - round(sh["t0"] * FPS))
    bg = cover(cur_frames[k])
    # beat punch: background zooms in 7% at each cut, eases back over 0.3 s
    lt = t - sh["t0"]
    z = 1 + 0.07 * max(0, 1 - lt / 0.3) ** 2
    if z > 1.0005:
        zh, zw = round(H * z), round(W * z)
        big = cv2.resize(bg, (zw, zh), interpolation=cv2.INTER_LINEAR)
        bg = big[(zh - H) // 2:(zh - H) // 2 + H, (zw - W) // 2:(zw - W) // 2 + W].copy()
    frame = np.ascontiguousarray(bg)

    # character (source frame index follows the song time 1:1)
    ci = min(NFR, 1 + int(round(t * 30)))
    rgb, a = char_rgba(ci)
    bt = (t % (2 * BEAT)) / (2 * BEAT)          # small bounce on every kick (2 beats)
    pulse = 1 + 0.035 * max(0, 1 - bt / 0.25)
    s = CH_SCALE * pulse
    rgb_s = cv2.resize(rgb[:, :, ::-1].copy(), None, fx=s, fy=s, interpolation=cv2.INTER_LANCZOS4)
    a_s = np.clip(cv2.resize(a, None, fx=s, fy=s, interpolation=cv2.INTER_LINEAR), 0, 1)
    x0 = round(CX - ((bx0 + bx1) / 2) * s); y0 = round(FEET_Y - by1 * s)
    # soft drop shadow under the character
    shadow = cv2.GaussianBlur(a_s, (0, 0), 10) * 0.35
    blend(frame, np.zeros_like(rgb_s), shadow, x0 + 8, y0 + 14)
    blend(frame, rgb_s, a_s, x0, y0)

    # place label (pops in at each bar)
    bar = sh["bar"]; bar_t0 = next(s_["t0"] for s_ in shots if s_["bar"] == bar)
    lt_bar = t - bar_t0
    paste_rgba(frame, LABELS[bar], 540, 250, scale=ease_pop(lt_bar / 0.22) * min(1, 0.6 + lt_bar / 0.08 * 0.4),
               alpha=min(1, lt_bar / 0.06))

    # lyric subtitle
    for key, a0, a1 in LYR_T:
        if a0 <= t < a1:
            ltl = t - a0
            paste_rgba(frame, SUB[key], 540, 1530, scale=ease_pop(ltl / 0.2) * 0.98, alpha=min(1, ltl / 0.06))
            break
    enc.stdin.write(frame.tobytes())
    if f % 90 == 0: print("frame", f, "/", nframes, flush=True)
enc.stdin.close(); enc.wait()
print("done", OUT)
