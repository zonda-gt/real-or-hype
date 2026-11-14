# Gate M / West Bund Dream Center reel: shots -> base video, then graphics composited per frame, then mix.
import subprocess, json, os, sys, math, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0, '.')
from edl import shots, END

FPS = 30; W, H = 1080, 1920
LEAD = 0.07          # cut slightly before the word onset
os.makedirs('segs', exist_ok=True); os.makedirs('out', exist_ok=True)
MONT = '/home/user/real-or-hype/.claude/skills/real-or-hype-video/scripts/Montserrat-ExtraBold.ttf'
PF = 'fonts/PlayfairDisplay.ttf'; PFI = 'fonts/PlayfairDisplay-Italic.ttf'; CAV = 'fonts/Caveat.ttf'

def run(cmd): subprocess.run(cmd, check=True)

# ---------- 1. shot segments ----------
S = shots()
bounds = [0] + [round((s['t0'] - LEAD) * FPS) for s in S[1:]] + [round(END * FPS)]
seglist = []
for k, s in enumerate(S):
    n = bounds[k + 1] - bounds[k]
    z, ay, ax = s['z'], s['ay'], s['ax']
    cw, ch = W / z, H / z
    vf = (f"scale={W}:{H}:flags=lanczos,setsar=1,"
          f"crop={cw:.1f}:{ch:.1f}:{ax*(W-cw):.1f}:{ay*(H-ch):.1f},scale={W}:{H}:flags=lanczos,"
          f"fps={FPS},unsharp=5:5:0.4,tpad=stop_mode=clone:stop_duration=1")
    # the in-point shifts back with LEAD so the chosen frame still lands on the word
    inn = max(0, s['inn'] - (LEAD if k else 0))
    out = f"segs/s{k:02d}.mp4"
    run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{inn:.3f}', '-i', f"src/{s['src']}.mp4", '-vf', vf,
         '-frames:v', str(n), '-an', '-c:v', 'libx264', '-preset', 'medium', '-crf', '14', '-pix_fmt', 'yuv420p', out])
    seglist.append(out)
with open('segs/list.txt', 'w') as f:
    for p in seglist: f.write(f"file '{os.path.basename(p)}'\n")
run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', 'segs/list.txt', '-c', 'copy', 'out/base.mp4'])
NF = bounds[-1]

# ---------- 2. graphics ----------
def shadowed(img, radius=10, alpha=150, offset=(0, 4)):
    """Return RGBA layer with a soft dark shadow under img's alpha."""
    pad = radius * 3
    big = Image.new('RGBA', (img.width + 2 * pad, img.height + 2 * pad), (0, 0, 0, 0))
    a = img.split()[3].point(lambda v: v * alpha // 255)
    sh = Image.new('RGBA', img.size, (0, 0, 0, 255)); sh.putalpha(a)
    big.paste(sh, (pad + offset[0], pad + offset[1]), sh)
    big = big.filter(ImageFilter.GaussianBlur(radius))
    big.alpha_composite(img, (pad, pad))
    return big

def text_img(txt, font, fill=(255, 255, 255, 255), tracking=0, stroke=0, stroke_fill=(0, 0, 0, 255)):
    tmp = ImageDraw.Draw(Image.new('RGBA', (10, 10)))
    widths = [tmp.textlength(c, font=font) for c in txt]
    tw = int(sum(widths) + tracking * (len(txt) - 1)) + 2 * stroke + 4
    asc, desc = font.getmetrics()
    im = Image.new('RGBA', (tw, asc + desc + 2 * stroke + 4), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    x = stroke + 2
    for c, w in zip(txt, widths):
        d.text((x, stroke + 2), c, font=font, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill); x += w + tracking
    return im

def var(path, size, name=None, wght=None):
    f = ImageFont.truetype(path, size)
    if wght is not None:
        try: f.set_variation_by_axes([wght])
        except Exception: pass
    return f

# Title card (her Lego opener: big white serif title over the hero shot)
def make_title():
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    t1 = text_img('GATE M', var(PF, 200, wght=600), tracking=14)
    t2 = text_img('West Bund Dream Center', var(PFI, 76, wght=500))
    t3 = text_img('in  Shanghai', var(PF, 46, wght=500), tracking=6)
    y = 430
    for im, gap in [(t1, 0), (t2, 0), (None, 34), (t3, 0)]:
        if im is None:
            d = ImageDraw.Draw(L); d.line([(W // 2 - 110, y + gap // 2), (W // 2 + 110, y + gap // 2)], fill=(255, 255, 255, 230), width=3); y += gap; continue
        L.alpha_composite(im, ((W - im.width) // 2, y)); y += im.height - (20 if im is t1 else 4)
    return shadowed(L, radius=14, alpha=170, offset=(0, 5))

# One-word captions (her style: small, white, bold caps, centre-low), a touch bigger for muted viewers
CAPF = var(MONT, 50)
def word_img(w):
    w = w.upper().replace('龙耀路', 'LONGYAO LU')
    return shadowed(text_img(w, CAPF, tracking=2), radius=6, alpha=200, offset=(0, 3))

# Handwritten labels (her dish labels)
LABF = var(CAV, 104, wght=700)
def label_img(txt, angle=-4):
    im = text_img(txt, LABF, fill=(255, 255, 255, 255), stroke=3, stroke_fill=(30, 30, 30, 255))
    im = shadowed(im, radius=8, alpha=160, offset=(0, 4))
    return im.rotate(angle, resample=Image.BICUBIC, expand=True)

def pill_img(lines):
    f = var(MONT, 50); padx, pady = 44, 24
    ims = [text_img(l, f, fill=(20, 20, 20, 255)) for l in lines]
    w = max(i.width for i in ims) + 2 * padx; h = sum(i.height for i in ims) + 2 * pady
    P = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(P)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=26, fill=(255, 255, 255, 245))
    y = pady
    for i in ims: P.alpha_composite(i, ((w - i.width) // 2, y)); y += i.height
    return shadowed(P, radius=12, alpha=120, offset=(0, 6))

def follow_img():
    f = var(MONT, 92)
    rows = [text_img(t, f, stroke=7, stroke_fill=(15, 15, 15, 255)) for t in ['FOLLOW ME', 'FOR MORE']]
    w = max(r.width for r in rows); h = sum(r.height for r in rows) - 18
    im = Image.new('RGBA', (w + 120, h + 40), (0, 0, 0, 0)); y = 10
    for r in rows: im.alpha_composite(r, ((im.width - r.width) // 2, y)); y += r.height - 18
    # fake italic
    im = im.transform(im.size, Image.AFFINE, (1, 0.2, -0.1 * im.height, 0, 1, 0), resample=Image.BICUBIC)
    return im

words = json.load(open('vo/words.json'))
items = []   # (start_frame, end_frame, image, x, y, anim)
title = make_title()
items.append((0, round(3.17 * FPS), title, (W - title.width) // 2, 0 - 42, 'fadeout'))
# captions: each word from 2 frames before its onset until the next word's onset (cap 0.6 s)
for i, (w, a, b) in enumerate(words):
    s0 = max(0, round(a * FPS) - 2)
    nxt = words[i + 1][1] if i + 1 < len(words) else b + 0.3
    e0 = round(min(nxt, b + 0.6) * FPS) - 2
    im = word_img(w)
    items.append((s0, max(s0 + 3, e0), im, (W - im.width) // 2, 1430 - im.height // 2, None))
def at(t): return round((t - LEAD) * FPS)
LAB = [  # (start, end, text, cx, cy, angle)
    (17.38, 19.24, 'silo rooftop', 560, 520, -4),
    (22.31, 23.90, '800m riverfront', 520, 640, -3),
    (30.58, 31.87, 'light show on the silos', 540, 1180, -3),
    (34.48, 35.86, 'ice rink, last winter', 540, 330, -3),
    (42.20, 45.23, 'walk to Tank Shanghai', 540, 640, -3),
]
for a, b, t, cx, cy, ang in LAB:
    im = label_img(t, ang); items.append((at(a), at(b), im, cx - im.width // 2, cy - im.height // 2, 'pop'))
pill = pill_img(['Metro Line 11', 'Longyao Rd · Exit 4'])
items.append((at(39.33), at(42.20), pill, (W - pill.width) // 2, 520, 'pop'))
fol = follow_img()
items.append((at(47.22), NF, fol, (W - fol.width) // 2, 230, 'pop'))

def place(frame, im, x, y, anim, f, s0, e0):
    if anim == 'pop' and f - s0 < 5:
        k = 0.72 + 0.28 * (f - s0 + 1) / 5
        im2 = im.resize((max(1, int(im.width * k)), max(1, int(im.height * k))), Image.BICUBIC)
        x += (im.width - im2.width) // 2; y += (im.height - im2.height) // 2; im = im2
    if anim == 'fadeout' and e0 - f < 7:
        a = im.split()[3].point(lambda v: int(v * (e0 - f) / 7)); im = im.copy(); im.putalpha(a)
    frame.alpha_composite(im, (int(x), int(y)))

dec = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', 'out/base.mp4', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-'], stdout=subprocess.PIPE)
enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                        '-c:v', 'libx264', '-preset', 'medium', '-crf', '15', '-pix_fmt', 'yuv420p', 'out/gfx.mp4'], stdin=subprocess.PIPE)
f = 0
while True:
    buf = dec.stdout.read(W * H * 4)
    if len(buf) < W * H * 4: break
    fr = Image.frombuffer('RGBA', (W, H), buf, 'raw', 'RGBA', 0, 1).copy()
    for s0, e0, im, x, y, anim in items:
        if s0 <= f < e0: place(fr, im, x, y, anim, f, s0, e0)
    enc.stdin.write(fr.tobytes()); f += 1
enc.stdin.close(); enc.wait(); dec.wait()
print('frames', f, 'expected', NF)

# ---------- 3. mix ----------
MUSIC_OFF = 6.0; MUSIC_DB = float(os.environ.get('MUSIC_DB', '-9'))
dur = NF / FPS
run(['ffmpeg', '-v', 'error', '-y', '-i', 'vo/narr.wav', '-ss', str(MUSIC_OFF), '-i', 'music/m3.mp3',
     '-filter_complex',
     f"[1:a]aresample=48000,loudnorm=I=-16:TP=-2,volume={MUSIC_DB}dB,afade=t=in:d=0.25,afade=t=out:st={dur-1.3:.2f}:d=1.3,atrim=0:{dur:.3f}[m];"
     f"[0:a]aresample=48000,apad[v];[v][m]amix=inputs=2:normalize=0:duration=longest,atrim=0:{dur:.3f},"
     f"loudnorm=I=-14:TP=-1.5:LRA=7,aresample=48000[a]",
     '-map', '[a]', '-c:a', 'pcm_s16le', 'out/mix.wav'])
run(['ffmpeg', '-v', 'error', '-y', '-i', 'out/gfx.mp4', '-i', 'out/mix.wav', '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
     '-c:a', 'aac', '-b:a', '256k', '-shortest', '-movflags', '+faststart', 'out/gatem_1080.mp4'])
run(['ffmpeg', '-v', 'error', '-y', '-i', 'out/gatem_1080.mp4', '-vf', 'scale=540:960', '-c:v', 'libx264', '-crf', '23',
     '-c:a', 'aac', '-b:a', '128k', 'out/gatem_540.mp4'])
print('done')
