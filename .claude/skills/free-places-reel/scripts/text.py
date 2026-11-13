"""On-screen text (Anton + Montserrat, from the real-or-hype-video skill)."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from common import W, H, FONTS
AN = ImageFont.truetype(os.path.join(FONTS, 'Anton-Regular.ttf'), 76)
ANH = ImageFont.truetype(os.path.join(FONTS, 'Anton-Regular.ttf'), 74)
ANC = ImageFont.truetype(os.path.join(FONTS, 'Anton-Regular.ttf'), 92)
MB = ImageFont.truetype(os.path.join(FONTS, 'Montserrat-ExtraBold.ttf'), 30)
YEL = (255, 214, 0)

def _wipe(layers, minx, maxx, reveal):
    edge = int(minx + (maxx-minx+40)*reveal)
    m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).rectangle([0, 0, edge, H], fill=255)
    for layer in layers: layer.putalpha(Image.composite(layer.getchannel('A'), Image.new('L', (W, H), 0), m))

def headline(lines, yc, bar, font=AN, reveal=1.0, barp=1.0, gap=10):
    """White headline with soft shadow; optional yellow bar under it. reveal/barp animate 0..1."""
    lh = font.getbbox('HG')[3]-font.getbbox('HG')[1]+gap
    txt = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sh = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ys = [yc+i*lh for i in range(len(lines))]; minx, maxx = W, 0
    for y, t in zip(ys, lines):
        b = font.getbbox(t); x = (W-(b[2]-b[0]))//2-b[0]
        ImageDraw.Draw(txt).text((x, y-(b[1]+b[3])//2), t, font=font, fill='white')
        ImageDraw.Draw(sh).text((x, y+4-(b[1]+b[3])//2), t, font=font, fill=(0, 0, 0, 170))
        minx = min(minx, x+b[0]); maxx = max(maxx, x+b[2])
    if reveal < 1: _wipe((txt, sh), minx, maxx, reveal)
    im = Image.alpha_composite(sh.filter(ImageFilter.GaussianBlur(9)), txt)
    if bar and barp > 0:
        b = MB.getbbox(bar); bw = b[2]-b[0]+34; bh = 48
        by = ys[-1]+(font.getbbox('H')[3]-font.getbbox('H')[1])//2+18; cw = int(bw*barp)
        bi = Image.new('RGBA', (W, H), (0, 0, 0, 0)); bd = ImageDraw.Draw(bi)
        bd.rectangle([(W-bw)//2, by, (W-bw)//2+bw, by+bh], fill=YEL)
        bd.text(((W-(b[2]-b[0]))//2-b[0], by+bh//2-(b[1]+b[3])//2), bar, font=MB, fill=(10, 10, 10))
        m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).rectangle([(W-cw)//2, 0, (W-cw)//2+cw, H], fill=255)
        bi.putalpha(Image.composite(bi.getchannel('A'), Image.new('L', (W, H), 0), m))
        im = Image.alpha_composite(im, bi)
    return im

def place(name, k):            # k = frames since the place's first shot
    return headline([name.upper()], 470, '$0 · FREE', reveal=min(1, k/6), barp=min(1, max(0, (k-3)/5)))

def hook(city):
    return headline([f'{city.upper()} IS EXPENSIVE, BUT...'], 780, None, font=ANH)

CTA_LINES = [[('DM', YEL), (' US FOR A ', 'white'), ('FREE', YEL)], [('PERSONALIZED ITINERARY', 'white')]]
def cta(k, yc=470, gap=14):    # ending call to action, DM and FREE in yellow
    F = ANC; reveal = min(1, k/6)
    txt = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sh = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    dt, ds = ImageDraw.Draw(txt), ImageDraw.Draw(sh); hb = F.getbbox('HG'); lh = hb[3]-hb[1]+gap; minx, maxx = W, 0
    for li, segs in enumerate(CTA_LINES):
        full = ''.join(t for t, _ in segs); bb = F.getbbox(full); x = (W-(bb[2]-bb[0]))//2-bb[0]
        y = yc+li*lh-(hb[1]+hb[3])//2; minx = min(minx, x+bb[0]); maxx = max(maxx, x+bb[2])
        for t, c in segs:
            ds.text((x, y+5), t, font=F, fill=(0, 0, 0, 190)); dt.text((x, y), t, font=F, fill=c, stroke_width=2, stroke_fill=(0, 0, 0, 140))
            x += F.getlength(t)
    if reveal < 1: _wipe((txt, sh), minx, maxx, reveal)
    return Image.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)), txt)
