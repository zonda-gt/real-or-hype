# Promo: "Send us a reel" (DM service). Hook = first ~4.9 s of a viral reel, then it shrinks into a DM chat,
# we reply with where / how / cost, more reels fly in, we reply with an itinerary, CTA.
# usage: promo_dm.py <workdir>   (workdir has src/viral.mp4, vo/L1..L6.wav + L*.json word stamps)
# writes <workdir>/promo_silent.mp4 and timeline.json; audio is mixed by promo_audio.py
import sys, os, json, subprocess, math, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W, H, FPS = 1080, 1920, 30
WD = sys.argv[1]; HERE = os.path.dirname(os.path.abspath(__file__))
CFG = json.load(open(os.path.join(WD, 'promo.json')))
F_XB = os.path.join(HERE, 'Montserrat-ExtraBold.ttf'); F_VAR = os.path.join(HERE, 'Montserrat[wght].ttf')
EMOJI = '/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf'
_fc = {}
def font(sz, w='ExtraBold'):
    k = (sz, w)
    if k not in _fc:
        if w == 'ExtraBold': _fc[k] = ImageFont.truetype(F_XB, sz)
        else:
            f = ImageFont.truetype(F_VAR, sz); f.set_variation_by_name(w); _fc[k] = f
    return _fc[k]
_ec = {}
def emoji(ch, sz):
    if (ch, sz) not in _ec:
        f = ImageFont.truetype(EMOJI, 109); im = Image.new('RGBA', (140, 140)); d = ImageDraw.Draw(im)
        d.text((4, 4), ch, font=f, embedded_color=True); im = im.crop(im.getbbox())
        _ec[(ch, sz)] = im.resize((sz, round(im.height * sz / im.width)), Image.LANCZOS)
    return _ec[(ch, sz)]

YEL = (255, 226, 26); BG = (14, 14, 16); BUB = (38, 38, 42); WHITE = (255, 255, 255); GREY = (150, 150, 158)
def ease(x): x = min(1, max(0, x)); return 1 - (1 - x) ** 3
def back(x):  # overshoot pop
    x = min(1, max(0, x)); c = 1.7; return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2

# ---------- timeline (seconds) ----------
VO = {}  # line -> (start, dur, words[(t,word)])
for i, st in enumerate(CFG['vo_starts'], 1):
    j = json.load(open(f'{WD}/vo/L{i}.json'))
    dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f'{WD}/vo/L{i}.wav'], capture_output=True, text=True).stdout)
    VO[i] = (st, dur, [(st + w['start'], w['end'] + st) for w in j['words']])
T = CFG['t']  # scene times
END = T['end']

# ---------- viral frames ----------
def read_frames(path, w, h, t0=0, t1=None):
    args = ['ffmpeg', '-loglevel', 'error', '-ss', str(t0), '-i', path] + (['-t', str(t1 - t0)] if t1 else []) + \
           ['-vf', f'scale={w}:{h}:flags=lanczos,fps={FPS}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-']
    raw = subprocess.run(args, capture_output=True).stdout; n = len(raw) // (w * h * 3)
    return [Image.frombuffer('RGB', (w, h), raw[i * w * h * 3:(i + 1) * w * h * 3]) for i in range(n)]
HOOK_END = T['hook_end']
full = read_frames(f'{WD}/src/viral.mp4', W, H, 0, HOOK_END + 0.7)
CW, CH = 470, 836
card_frames = read_frames(f'{WD}/src/viral.mp4', CW, CH, 0, CFG['loop_end'])
def viral_card(t):  # card keeps playing (muted), looping over the good part
    n = len(card_frames); i = int(t * FPS)
    if i >= n: i = int(CFG['loop_start'] * FPS) + (i - n) % (n - int(CFG['loop_start'] * FPS))
    return card_frames[i]

def rounded(im, r):
    m = Image.new('L', im.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, im.width - 1, im.height - 1), r, fill=255)
    out = im.convert('RGBA'); out.putalpha(m); return out

def outline_text(d, xy, txt, f, fill=WHITE, sw=7, anchor='mm'):
    d.text(xy, txt, font=f, fill=fill, stroke_width=sw, stroke_fill=(0, 0, 0), anchor=anchor)

# ---------- static assets ----------
def placeholder_reel(label, emo, c1, c2):
    px = np.zeros((CH, CW, 3)); yy = np.linspace(0, 1, CH)[:, None]
    for k in range(3): px[:, :, k] = c1[k] * (1 - yy) + c2[k] * yy
    im = Image.fromarray(px.astype('uint8')); d = ImageDraw.Draw(im)
    e = emoji(emo, 150); im.paste(e, ((CW - e.width) // 2, 230), e)
    f = font(44); lines = label.split('\n')
    for k, ln in enumerate(lines): outline_text(d, (CW // 2, 470 + k * 56), ln, f, sw=4)
    return im
REELS = [placeholder_reel(r['label'], r['emoji'], r['c1'], r['c2']) for r in CFG['more_reels']]

def reel_msg(img, scale=1.0):
    """Sent reel = rounded card with a small reel icon."""
    c = rounded(img, 34); d = ImageDraw.Draw(c)
    e = emoji('▶️', 54); c.alpha_composite(e, (CW - 54 - 22, 22))
    if scale != 1: c = c.resize((max(1, int(CW * scale)), max(1, int(CH * scale))), Image.LANCZOS)
    return c

def bubble(rows, maxw=900, title=None, light=False):
    """rows: list of (emoji, text). Returns RGBA bubble."""
    fb = font(48, 'SemiBold'); ft = font(52); pad = 38; gap = 20; isz = 54
    def wrap(txt, w):
        out, cur = [], ''
        for wd in txt.split():
            nxt = (cur + ' ' + wd).strip()
            if fb.getlength(nxt) <= w: cur = nxt
            else: out.append(cur); cur = wd
        out.append(cur); return out
    blocks = []; h = pad; tw = 0
    if title: h += 74; tw = ft.getlength(title)
    for emo, txt in rows:
        ls = wrap(txt, maxw - 2 * pad - isz - 20); blocks.append((emo, ls))
        tw = max(tw, isz + 20 + max(fb.getlength(l) for l in ls)); h += len(ls) * 62 + gap
    h += pad - gap; w = int(min(maxw, tw + 2 * pad))
    im = Image.new('RGBA', (w, int(h))); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 38, fill=(WHITE if light else BUB))
    tc = (20, 20, 22) if light else WHITE
    y = pad
    if title: d.text((pad, y), title, font=ft, fill=tc); y += 74
    for emo, ls in blocks:
        if emo: e = emoji(emo, isz); im.alpha_composite(e, (pad, y + 2))
        for k, l in enumerate(ls): d.text((pad + isz + 20, y + k * 62), l, font=fb, fill=tc)
        y += len(ls) * 62 + gap
    return im

def header(im):
    d = ImageDraw.Draw(im); d.rectangle((0, 0, W, 230), fill=BG)
    d.ellipse((44, 110, 144, 210), fill=YEL); d.text((94, 160), '?', font=font(60), fill=(0, 0, 0), anchor='mm')
    d.text((170, 118), CFG['name'], font=font(44), fill=WHITE)
    d.text((170, 172), CFG['sub'], font=font(32, 'Medium'), fill=GREY)
    d.line((0, 230, W, 230), fill=(40, 40, 44), width=2)

# chat items: (appear_time, side, kind, payload)
ITEMS = [(T['send'], 'r', 'viral', None)]
ITEMS.append((T['typing1'], 'l', 'typing', T['reply1']))
for k, (emo, txt) in enumerate(CFG['reply1']):
    ITEMS.append((T['reply1'] + T['reply1_step'][k], 'l', 'b', bubble([(emo, txt)])))
for k in range(len(REELS)):
    ITEMS.append((T['reels'] + k * T['reel_step'], 'r', 'reel', k))
ITEMS.append((T['typing2'], 'l', 'typing', T['plan']))
PLAN = bubble([(e, t) for e, t in CFG['plan_rows']], maxw=980, title=CFG['plan_title'], light=True)
ITEMS.append((T['plan'], 'l', 'plan', PLAN))
RS = 0.43  # reels in the stack are smaller, shown as a fan

def item_img(kind, payload, t):
    if kind == 'viral': return reel_msg(viral_card(t))
    if kind == 'reel': return reel_msg(REELS[payload], RS)
    if kind in ('b', 'plan'): return payload
    if kind == 'typing':
        im = Image.new('RGBA', (170, 92)); d = ImageDraw.Draw(im); d.rounded_rectangle((0, 0, 169, 91), 40, fill=BUB)
        for k in range(3):
            a = 0.5 + 0.5 * math.sin(t * 9 - k * 0.9); c = int(110 + 120 * a)
            d.ellipse((34 + k * 38, 34 - 6 * a, 58 + k * 38, 58 - 6 * a), fill=(c, c, c))
        return im

CHAT_TOP, CHAT_BOT = 260, 1440   # subtitles live below the chat
def chat_frame(t, intro=None):
    im = Image.new('RGBA', (W, H), BG + (255,))
    # layout: stack items that have appeared (typing bubble disappears when its reply arrives)
    vis = []
    for (ta, side, kind, p) in ITEMS:
        if t < ta: continue
        if kind == 'typing' and t >= p: continue
        vis.append((ta, side, kind, p))
    # reels after the first are laid out as a horizontal fan in one row
    rows = []; reel_row = None
    for it in vis:
        if it[2] == 'reel':
            if reel_row is None: reel_row = ['reelrow', []]; rows.append(reel_row)
            reel_row[1].append(it)
        else: rows.append(['one', it])
    imgs = []
    for r in rows:
        if r[0] == 'one':
            ta, side, kind, p = r[1]; imgs.append((side, item_img(kind, p, t), ta, kind))
        else:
            n = len(r[1]); w1 = int(CW * RS); h1 = int(CH * RS); ov = 190
            row = Image.new('RGBA', (w1 + (len(REELS) - 1) * ov, h1 + 40))
            for k, (ta, side, kind, p) in enumerate(r[1]):
                c = item_img(kind, p, t); a = back((t - ta) / 0.28)
                cs = c.resize((max(1, int(c.width * a)), max(1, int(c.height * a)))) if a < 0.999 else c
                cs = cs.rotate((2 - k) * 3, expand=True, resample=Image.BICUBIC)
                x = row.width - w1 - k * ov + (w1 - cs.width) // 2; y = 20 + (h1 - cs.height) // 2
                row.alpha_composite(cs, (max(0, x), max(0, y)))
            imgs.append(('r', row, 0, 'reelrow'))
    total = sum(i[1].height for i in imgs) + 28 * (len(imgs) - 1)
    # newest at bottom; scroll smoothly so the bottom sits at CHAT_BOT
    global _scroll
    target = CHAT_BOT - total          # messages stack up from the bottom, like a real DM
    if _scroll is None or intro is not None: _scroll = target
    else: _scroll = _scroll + (target - _scroll) * 0.3
    y = _scroll
    for side, c, ta, kind in imgs:
        a = 1.0 if kind in ('reelrow',) else back((t - ta) / 0.28)
        if kind == 'viral' and intro is not None: a = 1.0
        if a > 0.01:
            cs = c if a > 0.999 else c.resize((max(1, int(c.width * a)), max(1, int(c.height * a))))
            x = (W - 50 - c.width) if side == 'r' else 50
            ox = (c.width - cs.width) if side == 'r' else 0
            if not (kind == 'viral' and intro is not None):
                im.alpha_composite(cs, (int(x + ox), int(y + c.height - cs.height)))
            else:
                intro['pos'] = (x, int(y))
        y += c.height + 28
    header(im)
    return im
_scroll = None

def subs(im, t):
    """word-by-word subtitles, chunks of <=3 words, current word yellow."""
    for i, (st, dur, ws) in VO.items():
        if i in CFG['no_subs']: continue
        words = CFG['lines'][i - 1].replace('|', ' ').split()
        if len(words) != len(ws): ws = [(st + dur * k / len(words), st + dur * (k + 1) / len(words)) for k in range(len(words))]
        chunks, k = [], 0
        for part in CFG['lines'][i - 1].split('|'):
            n = len(part.split()); chunks.append(list(range(k, k + n))); k += n
        for ci, ch in enumerate(chunks):
            a = ws[ch[0]][0] - 2 / FPS; b = (ws[chunks[ci + 1][0]][0] - 2 / FPS) if ci + 1 < len(chunks) else ws[ch[-1]][1] + 0.25
            if not (a <= t < b): continue
            cw = max([k for k in ch if ws[k][0] - 2 / FPS <= t] or [ch[0]])
            f = font(66); parts = [words[k] for k in ch]
            tot = f.getlength(' '.join(parts)); x = (W - tot) / 2; y = CFG['sub_y']; d = ImageDraw.Draw(im)
            for k in ch:
                d.text((x, y), words[k], font=f, fill=(YEL if k == cw else WHITE), stroke_width=6, stroke_fill=(0, 0, 0))
                x += f.getlength(words[k] + ' ')

def toptext(im, t):
    for a, b, txt in CFG['top_text']:
        if a <= t < b:
            d = ImageDraw.Draw(im); s = back((t - a) / 0.25); f = font(int(64 * max(0.3, s)))
            for k, ln in enumerate(txt.split('\n')):
                outline_text(d, (W // 2, CFG['top_y'] + k * 80), ln, f, fill=(YEL if k else WHITE))

def cta(t):
    t0 = T['cta']; im = Image.new('RGBA', (W, H), BG + (255,)); d = ImageDraw.Draw(im)
    s = back((t - t0) / 0.35)
    big = font(int(124 * max(0.2, s)))
    for k, ln in enumerate(CFG['cta_big']): d.text((W // 2, 640 + k * 150), ln, font=big, fill=(YEL if k == len(CFG['cta_big']) - 1 else WHITE), anchor='mm')
    for k, (emo, txt) in enumerate(CFG['cta_rows']):
        ta = t0 + 0.5 + k * 0.35
        if t < ta: continue
        a = ease((t - ta) / 0.3); fy = 1000 + k * 110 + int(30 * (1 - a)); f = font(54, 'SemiBold')
        x = 230; e = emoji(emo, 60); im.alpha_composite(e, (x, fy - e.height // 2)); d.text((x + 90, fy), txt, font=f, fill=WHITE, anchor='lm')
    if t > t0 + 1.4:
        a = ease((t - t0 - 1.4) / 0.4); bob = 14 * math.sin((t - t0) * 6)
        d.text((W // 2, 1500 + bob), CFG['cta_arrow'], font=font(54), fill=YEL, anchor='mm')
        e = emoji('👇', 90); im.alpha_composite(e, (W // 2 - 45, int(1560 + bob)))
    return im

def frame(t):
    if t < HOOK_END:
        im = full[min(int(t * FPS), len(full) - 1)].convert('RGBA'); toptext(im, t)
    elif t < T['send'] + T['shrink']:
        # shrink the playing reel from full screen into the sent-card position in the chat
        intro = {}; im = chat_frame(T['send'] + 0.0001, intro)
        x1, y1 = intro.get('pos', (W - 50 - CW, CHAT_TOP))
        a = ease((t - HOOK_END) / T['shrink']); w = int(W + (CW - W) * a); h = int(H + (CH - H) * a)
        x = int(0 + (x1 - 0) * a); y = int(0 + (y1 - 0) * a)
        fr = full[min(int(t * FPS), len(full) - 1)].resize((w, h), Image.BILINEAR)
        im.alpha_composite(rounded(fr, int(34 * a) + 1), (x, y))
    elif t < T['cta']:
        im = chat_frame(t)
    else:
        im = cta(t)
    subs(im, t)
    return im.convert('RGB')

out = f'{WD}/promo_silent.mp4'
p = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                      '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709', out], stdin=subprocess.PIPE)
n = int(round(END * FPS))
for i in range(n):
    p.stdin.write(frame(i / FPS).tobytes())
p.stdin.close(); p.wait()
json.dump({'vo': {i: v[0] for i, v in VO.items()}, 't': T}, open(f'{WD}/timeline.json', 'w'))
print('video ok', n, 'frames')
