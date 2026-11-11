# Composite + captions renderer for the "5 days in Shanghai" reel.
# usage: python3 -I render.py <work_dir> <out.mp4> [t0 t1]   (t0/t1 = optional preview range in seconds)
import sys, os, json, subprocess, math
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter

WD = sys.argv[1]; OUT = sys.argv[2]
T0 = float(sys.argv[3]) if len(sys.argv) > 3 else 0.0
T1 = float(sys.argv[4]) if len(sys.argv) > 4 else None
S = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H, FPS = 1080, 1920, 30
EARLY = 2 / FPS                       # captions appear 2 frames before the word
FONT = {
    'sans': '/home/user/real-or-hype/.claude/skills/real-or-hype-video/scripts/Montserrat-ExtraBold.ttf',
    'anton': '/home/user/real-or-hype/.claude/skills/real-or-hype-video/scripts/Anton-Regular.ttf',
    'serif': S + '/fonts/InstrumentSerif-Italic.ttf',
    'mono': S + '/fonts/JetBrainsMono.ttf',
}

# ---------------------------------------------------------------- timeline
TALK, BROLL = 'talk', 'broll'
BR = {  # rc start, rc end, file, src start, zoom, crop anchor (fx, fy in 0..1 of the spare area)
    'flight': (7.10, 8.30, '7674813533926206918', 3.5, 1.00, (0.5, 0.5)),
    'hotel':  (11.00, 12.15, '7336941621159742758', 9.0, 1.00, (0.5, 0.5)),
    'cub':    (15.20, 16.00, '7696085747824999153', 0.6, 1.35, (0.5, 0.45)),
    'zoo':    (16.95, 18.60, '7543408040507477248', 1.5, 1.30, (0.5, 0.95)),
    'bund':   (27.85, 29.30, '7608048919034301416', 0.0, 1.00, (0.5, 0.5)),
    'dumpl':  (29.30, 31.20, '7605480080974188712', 21.2, 1.40, (0.5, 0.0)),
    'sky':    (31.20, 33.95, '7649340396719545530', 13.0, 1.00, (0.5, 0.5)),
}
# punch-in zoom on him at phrase starts (hard jump cuts, like the reference)
ZOOMS = [(0.00, 1.00), (1.92, 1.12), (3.56, 1.00), (5.20, 1.10), (8.30, 1.16), (12.15, 1.00), (13.22, 1.10),
         (16.00, 1.18), (18.60, 1.00), (21.00, 1.12), (22.60, 1.00), (24.10, 1.12), (26.25, 1.00),
         (33.95, 1.08), (36.50, 1.00), (40.35, 1.10), (43.30, 1.00)]

def P(t0, t1, layer, anchor, lines, extra=None):
    return dict(t0=t0, t1=t1, layer=layer, anchor=anchor, lines=lines, extra=extra or {})
s, sf, c3, g3, gl, ol, mo = 'sans', 'serif', 'caps3d', 'gold3d', 'glow', 'outline', 'mono'
PH = [
    P(0.00, 1.90, 'front', 'above', [[('would', s, 58, 0.00), ('you', s, 58, 0.24), ('fly', s, 58, 0.36)],
                                     [('600', sf, 120, 0.58), ('miles', sf, 120, 1.02)]]),
    P(1.92, 3.45, 'behind', 'behind', [[('to', s, 54, 1.92), ('China', s, 54, 1.92), ('just', s, 54, 2.26), ('to', s, 54, 2.68), ('see', s, 54, 2.82), ('a', s, 54, 2.90)],
                                      [('panda?', sf, 270, 2.98)]]),
    P(3.56, 5.60, 'behind', 'behind', [[("here's", s, 54, 3.56), ('what', s, 54, 4.04)],
                                      [('5', c3, 160, 4.18), ('DAYS', c3, 160, 4.40), ('IN', c3, 160, 4.70)],
                                      [('SHANGHAI', c3, 200, 4.90)]]),
    P(5.60, 7.10, 'front', 'above', [[('would', s, 54, 5.20), ('cost,', s, 54, 5.42)],
                                    [('flying', sf, 112, 5.68), ('from', sf, 112, 6.34)],
                                    [('London.', gl, 116, 6.56)]]),
    P(7.10, 8.30, 'front', 'center', [[('the', sf, 150, 7.16), ('flights?', sf, 150, 7.46)]]),
    P(8.30, 11.00, 'behind', 'behind', [[('return', s, 58, 8.84), ('in', s, 58, 9.52), ('December', sf, 104, 10.38)],
                                       [('$600', g3, 300, 8.32)]]),
    P(11.00, 12.15, 'front', 'center', [[('hotel?', sf, 180, 11.06)]]),
    P(12.15, 13.22, 'behind', 'behind', [[('each', sf, 112, 12.70)], [('$100', g3, 300, 12.18)]]),
    P(13.22, 15.20, 'front', 'above', [[('for', s, 58, 13.22), ('four', s, 58, 13.50), ('nights', s, 58, 13.74)],
                                      [('if', sf, 104, 13.96), ('you', sf, 104, 14.16), ('share', sf, 104, 14.26)],
                                      [('with', s, 58, 14.46), ('a', s, 58, 14.62), ('friend.', gl, 100, 14.78)]]),
    P(15.20, 16.00, 'front', 'center', [[('the', sf, 150, 15.26), ('pandas?', sf, 150, 15.44)]]),
    P(16.00, 16.95, 'behind', 'behind', [[('just', sf, 112, 16.00)], [('$6', g3, 340, 16.26)]]),
    P(16.95, 18.60, 'front', 'center', [[('you', s, 58, 17.18), ('see', s, 58, 17.34), ('them', s, 58, 17.58), ('at', s, 58, 17.70), ('the', s, 58, 17.84)],
                                       [('SHANGHAI', c3, 190, 17.92)], [('ZOO', c3, 260, 18.20)]]),
    P(18.60, 21.00, 'behind', 'behind', [[('and', s, 56, 18.70), ('yes,', s, 56, 18.84), ('shanghai', sf, 100, 19.12), ('has', sf, 100, 19.50)],
                                        [('GIANT', c3, 190, 19.82)], [('PANDAS', c3, 200, 20.20)]]),
    P(21.00, 22.85, 'front', 'above', [[('no', s, 58, 21.06), ('need', s, 58, 21.46), ('to', s, 58, 21.64), ('fly', s, 58, 21.80), ('to', s, 58, 21.96)],
                                      [('Chengdu.', sf, 150, 22.12)]], extra={'strike': (1, 0, 22.32)}),
    P(22.85, 24.10, 'front', 'above', [[('food', sf, 130, 22.66), ('&', sf, 130, 23.08)], [('transport?', gl, 112, 23.24)]]),
    P(24.10, 26.25, 'behind', 'behind', [[('budget', s, 58, 24.14), ('another', s, 58, 24.66)], [('$200', g3, 300, 25.04)]]),
    P(26.25, 27.85, 'behind', 'behind', [[('and', s, 56, 26.28), ("you're", s, 56, 26.52), ('not', s, 56, 26.70), ('just', s, 56, 26.82)],
                                        [('there', s, 56, 27.06), ('for', s, 56, 27.28)], [('PANDAS.', ol, 200, 27.48)]]),
    P(27.85, 29.30, 'front', 'center', [[('walk', s, 64, 27.92), ('along', s, 64, 28.44), ('the', s, 64, 28.80)], [('Bund,', sf, 210, 28.94)]]),
    P(29.30, 31.20, 'front', 'center', [[('eat', s, 64, 29.34)], [('soup', gl, 150, 29.88)], [('dumplings', gl, 150, 30.44)]]),
    P(31.20, 33.95, 'front', 'center', [[('and', s, 60, 31.20), ('explore', s, 60, 31.26), ('one', s, 60, 31.58), ('of', s, 60, 31.86), ('the', s, 60, 32.00)],
                                       [('CRAZIEST', c3, 180, 32.08)], [('SKYLINES', c3, 180, 32.56)],
                                       [('in', sf, 104, 33.26), ('the', sf, 104, 33.48), ('world.', sf, 104, 33.58)]]),
    P(33.95, 36.50, 'behind', 'behind', [[('600', mo, 50, 34.00), ('+ 100', mo, 50, 34.22), ('+ 6', mo, 50, 34.44), ('+ 200', mo, 50, 34.66)],
                                        [('total', sf, 112, 34.00), ('just', sf, 112, 34.40)], [('$906', g3, 320, 35.26)]]),
    P(36.50, 40.35, 'front', 'above', [[("let's", s, 58, 36.54), ('call', s, 58, 36.98), ('it', s, 58, 37.12)], [('$910', g3, 230, 37.30)],
                                      [('for', sf, 100, 38.04), ('5', sf, 100, 38.70), ('days', sf, 100, 39.26), ('in', sf, 100, 39.56), ('Shanghai.', sf, 100, 39.74)]]),
    P(40.35, 43.30, 'front', 'above', [[('want', s, 58, 40.40), ('to', s, 58, 40.88), ('visit', s, 58, 41.00), ('China', s, 58, 41.18)],
                                      [('without', sf, 110, 41.58), ('figuring', sf, 110, 42.02)],
                                      [('it', sf, 110, 42.36), ('out', sf, 110, 42.60), ('yourself?', gl, 104, 42.74)]]),
    P(43.30, 99.0, 'behind', 'behind', [[('and', s, 52, 44.88), ("we'll", s, 52, 45.12), ('help', s, 52, 45.32), ('you', s, 52, 45.58), ('plan', s, 52, 45.72), ('it.', s, 52, 45.96)],
                                       [('your', sf, 100, 44.12), ('date', sf, 100, 44.24), ('&', sf, 100, 44.48), ('budget', sf, 100, 44.62)],
                                       [('DM US', g3, 330, 43.38)]], extra={'arrow': 43.90}),
]

# ---------------------------------------------------------------- word sprites
_fc = {}
def font(kind, size):
    k = (kind, size)
    if k not in _fc:
        f = ImageFont.truetype(FONT[kind], size)
        if kind == 'mono':
            try: f.set_variation_by_name('Bold')
            except Exception: pass
        _fc[k] = f
    return _fc[k]

def shadow_of(img, r, a):
    al = img.split()[3].filter(ImageFilter.GaussianBlur(r)).point(lambda v: int(v * a))
    sh = Image.new('RGBA', img.size, (0, 0, 0, 0)); sh.putalpha(al)
    return sh

def text_mask(text, f, pad, stroke=0):
    l, t, r, b = f.getbbox(text, stroke_width=stroke)
    w, h = r - l + 2 * pad, b - t + 2 * pad
    m = Image.new('L', (w, h), 0)
    ImageDraw.Draw(m).text((pad - l, pad - t), text, font=f, fill=255, stroke_width=stroke, stroke_fill=255)
    return m

_sc = {}
def sprite(text, style, size):
    key = (text, style, size)
    if key in _sc: return _sc[key]
    pad = int(size * 0.35) + 10
    if style in ('sans', 'glow', 'mono', 'serif'):
        f = font({'sans': 'sans', 'glow': 'sans', 'mono': 'mono', 'serif': 'serif'}[style], size)
        m = text_mask(text, f, pad)
        col = {'sans': (255, 255, 255), 'glow': (255, 255, 255), 'mono': (255, 214, 92), 'serif': (255, 244, 228)}[style]
        face = Image.new('RGBA', m.size, col + (0,)); face.putalpha(m)
        base = Image.new('RGBA', m.size, (0, 0, 0, 0))
        if style == 'glow':
            g = Image.new('RGBA', m.size, (150, 200, 255, 0)); g.putalpha(m.filter(ImageFilter.GaussianBlur(size * 0.16)))
            g2 = Image.new('RGBA', m.size, (210, 230, 255, 0)); g2.putalpha(m.filter(ImageFilter.GaussianBlur(size * 0.05)))
            base = Image.alpha_composite(Image.alpha_composite(base, g), g2)
            base = Image.alpha_composite(base, g)
        else:
            base = Image.alpha_composite(base, shadow_of(face, max(4, size * 0.08), 0.55))
        img = Image.alpha_composite(base, face)
    elif style == 'outline':
        f = font('anton', size)
        sw = max(3, size // 40)
        l, t_, r, b = f.getbbox(text, stroke_width=sw)
        size_ = (r - l + 2 * pad, b - t_ + 2 * pad)
        m_out = Image.new('L', size_, 0); m_in = Image.new('L', size_, 0)
        ImageDraw.Draw(m_out).text((pad - l, pad - t_), text, font=f, fill=255, stroke_width=sw, stroke_fill=255)
        ImageDraw.Draw(m_in).text((pad - l, pad - t_), text, font=f, fill=255)
        ring = Image.fromarray(np.clip(np.asarray(m_out, np.int16) - np.asarray(m_in, np.int16), 0, 255).astype(np.uint8))
        face = Image.new('RGBA', ring.size, (255, 255, 255, 0)); face.putalpha(ring)
        img = Image.alpha_composite(shadow_of(face, 6, 0.6), face)
    else:  # caps3d / gold3d: Anton with an extruded side
        f = font('anton', size)
        m = text_mask(text, f, pad)
        depth = max(4, int(size * 0.055))
        w, h = m.size
        img = Image.new('RGBA', (w + depth, h + depth), (0, 0, 0, 0))
        side = (92, 62, 22) if style == 'gold3d' else (70, 60, 56)
        for k in range(depth, 0, -1):
            shade = tuple(int(c * (0.65 + 0.35 * (1 - k / depth))) for c in side)
            layer = Image.new('RGBA', m.size, shade + (0,)); layer.putalpha(m)
            img.alpha_composite(layer, (k, k))
        if style == 'gold3d':
            grad = np.zeros((h, w, 3), np.float32)
            yy = np.linspace(0, 1, h)[:, None]
            top, mid, bot = np.array([255, 241, 190]), np.array([246, 196, 78]), np.array([186, 122, 28])
            g = np.where(yy < 0.5, top + (mid - top) * (yy / 0.5), mid + (bot - mid) * ((yy - 0.5) / 0.5))
            grad[:] = g[:, None, :] if g.ndim == 2 else g
            grad = np.broadcast_to(g.reshape(h, 1, 3), (h, w, 3))
            face = Image.fromarray(grad.astype(np.uint8), 'RGB').convert('RGBA'); face.putalpha(m)
        else:
            face = Image.new('RGBA', m.size, (255, 255, 255, 0)); face.putalpha(m)
        img.alpha_composite(face, (0, 0))
        img = Image.alpha_composite(shadow_of(img, max(6, size * 0.07), 0.6), img)
    arr = np.asarray(img).astype(np.float32) / 255.0
    # tight visual box (without padding) for layout
    a = arr[..., 3] > 0.5
    ys, xs = np.where(a)
    box = (xs.min(), ys.min(), xs.max(), ys.max()) if len(xs) else (0, 0, arr.shape[1], arr.shape[0])
    _sc[key] = (arr, box)
    return _sc[key]

def layout(ph, cx, ref_y, fh=280):
    """Return list of (sprite_arr, x, y, t_word, style) for a phrase. Positions are top-left of the sprite."""
    lines = []
    for ln in ph['lines']:
        items = [(sprite(t, st, sz), t, st, sz, tw) for (t, st, sz, tw) in ln]
        gap = int(np.median([sz for (_, _, _, sz, _) in items]) * 0.26)
        widths = [it[0][1][2] - it[0][1][0] for it in items]
        heights = [it[0][1][3] - it[0][1][1] for it in items]
        lines.append((items, widths, sum(widths) + gap * (len(items) - 1), max(heights), gap))
    lead = 18
    total_h = sum(l[3] for l in lines) + lead * (len(lines) - 1)
    widest = max(l[2] for l in lines)
    cx = int(np.clip(cx, 60 + widest / 2, W - 60 - widest / 2)) if widest < W - 120 else W // 2
    anchor = ph['anchor']
    if anchor == 'above':
        top = ref_y - 120 - total_h
    elif anchor == 'behind':   # centre of the last (big) line sits on the top of his head
        top = ref_y + 0.30 * lines[-1][3] - total_h   # head covers only the bottom ~30% of the big word
    else:
        top = 860 - total_h / 2
    top = max(top, 250)
    out = []; y = top
    for items, widths, lw, lh, gap in lines:
        x = cx - lw / 2
        for (spr, t, st, sz, tw), wdt in zip(items, widths):
            arr, box = spr
            # baseline-ish alignment: bottom of the visual box on the line bottom
            out.append((arr, int(x - box[0]), int(y + lh - box[3]), max(tw, ph['t0']) - EARLY, st, (int(x), int(y + lh - (box[3] - box[1])), int(x + wdt), int(y + lh))))
            x += wdt + gap
        y += lh + lead
    return out

def blit(dst_rgb, dst_a, spr, x, y):
    """Alpha-over a float RGBA sprite onto dst (float rgb HxWx3) and keep a coverage map."""
    h, w = spr.shape[:2]
    x0, y0 = max(x, 0), max(y, 0); x1, y1 = min(x + w, W), min(y + h, H)
    if x1 <= x0 or y1 <= y0: return
    s = spr[y0 - y:y1 - y, x0 - x:x1 - x]
    a = s[..., 3:4]
    dst_rgb[y0:y1, x0:x1] = dst_rgb[y0:y1, x0:x1] * (1 - a) + s[..., :3] * a
    if dst_a is not None:
        dst_a[y0:y1, x0:x1] = dst_a[y0:y1, x0:x1] * (1 - a[..., 0]) + a[..., 0]

def animate(arr, p, fade):
    """p: 0..1 entrance progress, fade: 0..1 exit progress."""
    if p >= 1 and fade <= 0: return arr, 0
    e = 1 - (1 - min(p, 1)) ** 3
    sc = 1.14 - 0.14 * e
    blur = 9 * (1 - e) + 10 * fade
    alpha = e * (1 - fade)
    out = arr
    if abs(sc - 1) > 1e-3:
        out = cv2.resize(arr, None, fx=sc, fy=sc, interpolation=cv2.INTER_LINEAR)
    if blur > 0.6:
        out = cv2.GaussianBlur(out, (0, 0), blur)
    out = out.copy(); out[..., 3] *= alpha
    off = (out.shape[0] - arr.shape[0]) // 2
    return out, off

def draw_layer(rgb, cov, phs, t, face, zoom_state):
    for ph in phs:
        if not (ph['t0'] - EARLY <= t < ph['t1']): continue
        if 'pos' not in ph:
            fx, fy, fw, fh = face_at(ph['t0'], zoom_state)
            ph['pos'] = layout(ph, fx + fw / 2, fy, fh)
        fade = 0.0
        if ph['t1'] - t < 0.12: fade = 1 - (ph['t1'] - t) / 0.12
        for arr, x, y, tw, st, vb in ph['pos']:
            if t < tw: continue
            p = (t - tw) / 0.16
            a2, _ = animate(arr, p, fade)
            dx = (a2.shape[1] - arr.shape[1]) // 2; dy = (a2.shape[0] - arr.shape[0]) // 2
            blit(rgb, cov, a2, x - dx, y - dy)
        if 'strike' in ph['extra']:
            li, wi, ts = ph['extra']['strike']
            if t >= ts:
                k = min(1, (t - ts) / 0.22)
                items = [it for it in ph['pos']]
                # find the word: line li, index wi -> count words in earlier lines
                idx = sum(len(l) for l in ph['lines'][:li]) + wi
                x0, y0, x1, y1 = items[idx][5]
                ym = (y0 + y1) // 2 + 6
                xe = int(x0 - 10 + (x1 - x0 + 20) * k)
                cv2.line(rgb, (x0 - 10, ym + 8), (xe, ym - 8), (1.0, 0.33, 0.30), 9, cv2.LINE_AA)
        if 'arrow' in ph['extra'] and t >= ph['extra']['arrow']:
            k = min(1, (t - ph['extra']['arrow']) / 0.35)
            draw_arrow(rgb, k)

def draw_arrow(rgb, k):
    # hand-drawn style curve pointing at Instagram's share button (right column, lower third)
    p0, p1, p2 = np.array([760., 1180.]), np.array([940., 1150.]), np.array([985., 1395.])
    n = max(2, int(40 * k))
    ts = np.linspace(0, k, n)
    pts = ((1 - ts)[:, None] ** 2) * p0 + (2 * (1 - ts) * ts)[:, None] * p1 + (ts ** 2)[:, None] * p2
    cv2.polylines(rgb, [pts.astype(np.int32)], False, (1, 1, 1), 8, cv2.LINE_AA)
    if k >= 1:
        tip = p2; d = (p2 - p1) / np.linalg.norm(p2 - p1)
        nrm = np.array([-d[1], d[0]])
        for s_ in (1, -1):
            q = tip - d * 38 + nrm * 26 * s_
            cv2.line(rgb, tuple(tip.astype(int)), tuple(q.astype(int)), (1, 1, 1), 8, cv2.LINE_AA)

# ---------------------------------------------------------------- him: matte clean-up, relight, table
wall = cv2.cvtColor(cv2.imread(WD + '/wall_est.png'), cv2.COLOR_BGR2RGB).astype(np.float32) / 255
plate = cv2.cvtColor(cv2.imread(os.environ.get('ROOM_PLATE', S + '/rs/room_plate1.jpg')), cv2.COLOR_BGR2RGB)
plate = cv2.resize(plate, (W, H), interpolation=cv2.INTER_AREA).astype(np.float32) / 255
plate = cv2.GaussianBlur(plate, (0, 0), 6)
plate_wrap = cv2.GaussianBlur(plate, (0, 0), 25)
xx = np.arange(W)[None, :]; yy = np.arange(H)[:, None]
TABLE_Y = 1521 + 5 * xx / W
table = np.clip((yy - TABLE_Y) / 4 + 0.5, 0, 1).astype(np.float32)
lamp = (1.10 - 0.22 * (xx / W)).astype(np.float32)[..., None]   # warm key from the lamp on the left
lamp = np.broadcast_to(lamp, (H, W, 1))
vig = (1 - 0.38 * (((xx - W / 2) / (W / 2)) ** 2 + ((yy - H * 0.45) / (H * 0.62)) ** 2)).clip(0.45, 1).astype(np.float32)[..., None]
rng = np.random.default_rng(7)

def grade_person(F):
    g = F * 0.80
    g = g * np.array([1.06, 0.97, 0.86], np.float32)
    g = np.clip(g, 0, 1)
    g = g * g * (3 - 2 * g) * 0.35 + g * 0.65          # gentle S-curve for contrast
    return g * lamp

def grade_table(I):
    lum = I.mean(2, keepdims=True)
    walnut = np.array([0.42, 0.27, 0.17], np.float32)
    return np.clip(walnut * (lum / 0.62) ** 1.25 + (I - lum) * 0.25, 0, 1) * lamp

def comp_him(I, a_raw):
    a = np.clip((a_raw - 0.12) / 0.76, 0, 1)
    a3 = a[..., None]
    dec = (I - (1 - a3) * wall) / np.maximum(a3, 0.06)
    F = np.where(table[..., None] > 0.5, I, np.clip(dec, 0, 1))
    Pg = grade_person(F)
    Tg = grade_table(I)
    er = cv2.erode(a, np.ones((11, 11), np.uint8))
    band = np.clip(a - er, 0, 1)[..., None] * (yy < 1450)[..., None]
    rim = np.array([0.30, 0.42, 0.62], np.float32) * band * (0.45 + 0.35 * (xx / W))[..., None]
    t3 = table[..., None]
    cov = a3 + (1 - a3) * t3
    col = a3 * Pg + (1 - a3) * t3 * Tg
    out = col + (1 - cov) * plate
    out = out + rim + band * plate_wrap * 0.35
    return out

# ---------------------------------------------------------------- zoom (jump-cut punch-ins)
faces = json.load(open(WD + '/faces.json'))
last = None
for i, f in enumerate(faces):
    if f is None: faces[i] = last
    else: last = f
first = next(f for f in faces if f)
faces = [f or first for f in faces]
fa = np.array([f[:4] for f in faces], np.float32)
for i in range(1, len(fa)): fa[i] = 0.75 * fa[i - 1] + 0.25 * fa[i]

def zoom_at(t):
    z = 1.0
    for ts, zz in ZOOMS:
        if t >= ts: z = zz
    return z

def crop_box(t):
    z = zoom_at(t)
    i = min(int(t * FPS), len(fa) - 1)
    fx, fy, fw, fh = fa[i]
    cx, cy = fx + fw / 2, fy + fh * 0.75
    cw, ch = W / z, H / z
    x0 = float(np.clip(cx - cw / 2, 0, W - cw)); y0 = float(np.clip(cy - ch * 0.46, 0, H - ch))
    return z, x0, y0

def apply_zoom(img, t):
    z, x0, y0 = crop_box(t)
    if z == 1.0: return img
    M = np.array([[z, 0, -x0 * z], [0, z, -y0 * z]], np.float32)
    return cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)

def face_at(t, _):
    z, x0, y0 = crop_box(t)
    i = min(int(t * FPS), len(fa) - 1)
    # median over the first few frames of the phrase for a steady anchor
    seg = fa[i:i + 6]
    fx, fy, fw, fh = np.median(seg, 0)
    fy = fy - fh * 0.42                     # top of the hair, not the eyebrows
    return (fx - x0) * z, (fy - y0) * z, fw * z, fh * z

# ---------------------------------------------------------------- b-roll readers
class BRoll:
    def __init__(self, key):
        t0, t1, fid, ss, z, (ax, ay) = BR[key]
        self.t0, self.t1 = t0, t1
        n = int(round((t1 - t0) * FPS)) + 2
        sw, sh = int(W * z), int(H * z)
        cx, cy = int((sw - W) * ax), int((sh - H) * ay)
        vf = (f'fps={FPS},scale={sw}:{sh}:force_original_aspect_ratio=increase,crop={sw}:{sh},crop={W}:{H}:{cx}:{cy},'
              f'eq=contrast=1.06:saturation=1.05')
        self.p = subprocess.Popen(['ffmpeg', '-nostdin', '-loglevel', 'error', '-ss', str(ss), '-i', S + f'/broll/{fid}.mp4',
                                   '-frames:v', str(n), '-vf', vf, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
        self.last = None
    def frame(self, t):
        b = self.p.stdout.read(W * H * 3)
        if len(b) == W * H * 3: self.last = np.frombuffer(b, np.uint8).reshape(H, W, 3).astype(np.float32) / 255
        img = self.last
        k = (t - self.t0) / max(self.t1 - self.t0, 1e-3)
        sc = 1.0 + 0.06 * k                      # slow push-in
        if t - self.t0 < 0.1:                    # quick zoom-blur entrance
            e = (t - self.t0) / 0.1; sc += 0.12 * (1 - e)
        M = cv2.getRotationMatrix2D((W / 2, H / 2), 0, sc)
        img = cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        if t - self.t0 < 0.1:
            img = cv2.GaussianBlur(img, (0, 0), 6 * (1 - (t - self.t0) / 0.1) + 0.1)
        return img

def broll_key(t):
    for k, v in BR.items():
        if v[0] <= t < v[1]: return k
    return None

# ---------------------------------------------------------------- main loop
for _ph in PH:                      # build every caption sprite up front so a bad style fails fast
    for _ln in _ph['lines']:
        for _w in _ln: sprite(_w[0], _w[1], _w[2])
print('sprites ok', len(_sc), flush=True)
src = WD + '/out/roughcut_1080.mp4'
args_ss = ['-ss', f'{T0:.3f}'] if T0 > 0 else []
args_t = ['-t', f'{T1 - T0:.3f}'] if T1 else []
rd = subprocess.Popen(['ffmpeg', '-nostdin', '-loglevel', 'error'] + args_ss + ['-i', src] + args_t + ['-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
ra = subprocess.Popen(['ffmpeg', '-nostdin', '-loglevel', 'error'] + args_ss + ['-i', WD + '/alpha_full.mkv'] + args_t + ['-f', 'rawvideo', '-pix_fmt', 'gray', '-'], stdout=subprocess.PIPE)
wr = subprocess.Popen(['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                       '-c:v', 'libx264', '-crf', '17', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709', OUT],
                      stdin=subprocess.PIPE)
behind = [p for p in PH if p['layer'] == 'behind']; front = [p for p in PH if p['layer'] == 'front']
active = {}
n = int(round(T0 * FPS))
import time; tic = time.time(); k = 0
while True:
    b = rd.stdout.read(W * H * 3); ab = ra.stdout.read(W * H)
    if len(b) < W * H * 3 or len(ab) < W * H: break
    t = n / FPS
    I = np.frombuffer(b, np.uint8).reshape(H, W, 3).astype(np.float32) / 255
    a_raw = np.frombuffer(ab, np.uint8).reshape(H, W).astype(np.float32) / 255
    bk = broll_key(t)
    if bk:
        if bk not in active:
            if T0 > BR[bk][0]:   # preview started mid-b-roll: skip ahead
                pass
            active[bk] = BRoll(bk)
        out = active[bk].frame(t)
        draw_layer(out, None, front + behind, t, None, None)
    else:
        z = zoom_at(t)
        Iz = apply_zoom(I, t); az = apply_zoom(a_raw, t)
        # the plate and the table mask move with him
        global_plate = plate
        a = np.clip((az - 0.45) / 0.35, 0, 1); a3 = a[..., None]
        tbl = apply_zoom(table, t)[..., None] if z != 1.0 else table[..., None]
        pl = apply_zoom(plate, t) if z != 1.0 else plate
        wl = apply_zoom(wall, t) if z != 1.0 else wall
        dec = (Iz - (1 - a3) * wl) / np.maximum(a3, 0.06)
        F = np.where(tbl > 0.5, Iz, np.clip(dec, 0, 1))
        Pg = grade_person(F); Tg = grade_table(Iz)
        er = cv2.erode(a, np.ones((7, 7), np.uint8))
        band = (np.clip(a - er, 0, 1)[..., None]) * (1 - tbl)
        rim = np.array([0.30, 0.42, 0.62], np.float32) * band * (0.10 + 0.12 * (xx / W))[..., None] * (yy < 1150)[..., None]
        cov = a3 + (1 - a3) * tbl
        base = pl.copy()
        draw_layer(base, None, behind, t, None, None)          # words behind his head
        out = a3 * Pg + (1 - a3) * tbl * Tg + (1 - cov) * base
        out = out + rim + band * plate_wrap * 0.12
        draw_layer(out, None, front, t, None, None)
    out = out * vig
    out = out + rng.normal(0, 0.012, (H // 2, W // 2, 1)).astype(np.float32).repeat(2, 0).repeat(2, 1)
    wr.stdin.write((np.clip(out, 0, 1) * 255).astype(np.uint8).tobytes())
    for kk in list(active):
        if t >= BR[kk][1] + 0.1: active[kk].p.kill(); del active[kk]
    n += 1; k += 1
    if k % 150 == 0: print(f'{t:.1f}s  {k / (time.time() - tic):.2f} fps', flush=True)
wr.stdin.close(); wr.wait(); print('done', k, 'frames')
