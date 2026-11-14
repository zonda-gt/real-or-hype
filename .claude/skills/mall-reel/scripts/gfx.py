# On-screen text styles for mall-reel videos (1080x1920). Single source of truth for fonts, sizes and positions.
# Used by render.py (final video) and stylecheck.py (preview sheet). Change a style here and both follow.
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1080, 1920
FONTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'fonts')
MONT = os.path.join(FONTS, 'Montserrat-ExtraBold.ttf')      # captions, pill, follow sticker
PF = os.path.join(FONTS, 'PlayfairDisplay.ttf')               # title card (variable, wght 400-900)
PFI = os.path.join(FONTS, 'PlayfairDisplay-Italic.ttf')       # title card subtitle
CAV = os.path.join(FONTS, 'Caveat.ttf')                       # handwritten labels (variable, wght 400-700)

CAPTION_Y = 960       # centre line of the one-word captions: screen centre (user's choice; edl.CAPTION_Y overrides)
TITLE_TOP = 430       # top of the title block
FOLLOW_Y = 230        # top of the follow sticker


def var(path, size, wght=None):
    f = ImageFont.truetype(path, size)
    if wght is not None:
        try: f.set_variation_by_axes([wght])
        except Exception: pass
    return f


def shadowed(img, radius=10, alpha=150, offset=(0, 4)):
    """img with a soft dark drop shadow (no hard outline)."""
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


def _fit(im, maxw=980):
    return im if im.width <= maxw else im.resize((maxw, int(im.height * maxw / im.width)), Image.LANCZOS)


def title_img(line1, line2, line3, style='headline'):
    """Full-frame title layer over the opening shot(s).
    style 'headline' (default): CONTEXT for a viewer who doesn't know the place, e.g. SHANGHAI'S / Cement Factory /
      turned riverside hangout  (her "Full body health checkup in Shanghai", "SHANGHAI'S Basement Seafood").
    style 'name': the place's name, e.g. GATE M / West Bund Dream Center / in Shanghai (only if the name itself is famous)."""
    if style == 'headline':
        L = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        t1 = _fit(text_img(line1, var(PF, 84, 600), tracking=22), 820)
        t2 = _fit(text_img(line2, var(PF, 150, 700), tracking=2))
        t3 = _fit(text_img(line3, var(PFI, 74, 500)))
        y = TITLE_TOP - 40
        for im, dy in [(t1, -10), (t2, -6), (t3, 0)]:
            L.alpha_composite(im, ((W - im.width) // 2, y)); y += im.height + dy
        return shadowed(L, radius=14, alpha=175, offset=(0, 5))
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    t1 = _fit(text_img(line1, var(PF, 200, 600), tracking=14))
    t2 = _fit(text_img(line2, var(PFI, 76, 500)))
    t3 = text_img(line3, var(PF, 46, 500), tracking=6)
    y = TITLE_TOP
    for im, gap in [(t1, 0), (t2, 0), (None, 34), (t3, 0)]:
        if im is None:
            ImageDraw.Draw(L).line([(W // 2 - 110, y + gap // 2), (W // 2 + 110, y + gap // 2)], fill=(255, 255, 255, 230), width=3); y += gap; continue
        L.alpha_composite(im, ((W - im.width) // 2, y)); y += im.height - (20 if im is t1 else 4)
    return shadowed(L, radius=14, alpha=170, offset=(0, 5))


_CAPF = None
def word_img(w, replacements=None):
    """One spoken word, caps, white Montserrat ExtraBold 50 px with soft shadow (hers is ~34 px; 50 stays readable muted)."""
    global _CAPF
    _CAPF = _CAPF or var(MONT, 50)
    for k, v in (replacements or {}).items(): w = w.replace(k, v)
    return shadowed(text_img(w.upper(), _CAPF, tracking=2), radius=6, alpha=200, offset=(0, 3))


_LABF = None
def label_img(txt, angle=-4):
    """Handwritten spot/dish label: Caveat Bold 104 px, white, thin dark stroke, soft shadow, tilted 3-4 degrees."""
    global _LABF
    _LABF = _LABF or var(CAV, 104, 700)
    im = text_img(txt, _LABF, stroke=3, stroke_fill=(30, 30, 30, 255))
    im = shadowed(im, radius=8, alpha=160, offset=(0, 4))
    return im.rotate(angle, resample=Image.BICUBIC, expand=True)


def pill_img(lines):
    """Practical info (metro, hours): white rounded pill, dark Montserrat 50 px."""
    f = var(MONT, 50); padx, pady = 44, 24
    ims = [text_img(l, f, fill=(20, 20, 20, 255)) for l in lines]
    w = max(i.width for i in ims) + 2 * padx; h = sum(i.height for i in ims) + 2 * pady
    P = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(P).rounded_rectangle([0, 0, w - 1, h - 1], radius=26, fill=(255, 255, 255, 245))
    y = pady
    for i in ims: P.alpha_composite(i, ((w - i.width) // 2, y)); y += i.height
    return shadowed(P, radius=12, alpha=120, offset=(0, 6))


def follow_img(lines=('FOLLOW ME', 'FOR MORE')):
    """End sticker: white Montserrat 92 px with 7 px black outline, slanted like italic."""
    f = var(MONT, 92)
    rows = [text_img(t, f, stroke=7, stroke_fill=(15, 15, 15, 255)) for t in lines]
    w = max(r.width for r in rows); h = sum(r.height for r in rows) - 18
    im = Image.new('RGBA', (w + 120, h + 40), (0, 0, 0, 0)); y = 10
    for r in rows: im.alpha_composite(r, ((im.width - r.width) // 2, y)); y += r.height - 18
    im = im.transform(im.size, Image.AFFINE, (1, 0.2, -0.1 * im.height, 0, 1, 0), resample=Image.BICUBIC)
    if im.width > 960:   # long CTA text: shrink to keep ~60 px side margins
        k = 960 / im.width; im = im.resize((960, int(im.height * k)), Image.LANCZOS)
    return im


def place(frame, im, x, y, anim, f, s0, e0):
    """Composite im onto frame at frame index f of an item shown [s0, e0). 'pop' scales in over 5 frames, 'fadeout' fades over the last 7."""
    if anim == 'pop' and f - s0 < 5:
        k = 0.72 + 0.28 * (f - s0 + 1) / 5
        im2 = im.resize((max(1, int(im.width * k)), max(1, int(im.height * k))), Image.BICUBIC)
        x += (im.width - im2.width) // 2; y += (im.height - im2.height) // 2; im = im2
    if anim == 'fadeout' and e0 - f < 7:
        a = im.split()[3].point(lambda v: int(v * (e0 - f) / 7)); im = im.copy(); im.putalpha(a)
    frame.alpha_composite(im, (int(x), int(y)))
