# Place-name labels for the 9:16 cut: big white Anton name + yellow pill (Montserrat ExtraBold), soft shadow.
import os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, here)
FONTS = '/home/user/real-or-hype/.claude/skills/real-or-hype-video/scripts'
NAME_FONT = f'{FONTS}/Anton-Regular.ttf'; PILL_FONT = f'{FONTS}/Montserrat-ExtraBold.ttf'
W, H = 1080, 1920
YELLOW = (247, 208, 46)
# shot index -> (name, pill)
LABELS = {
    3: ('XIJIANG MIAO VILLAGE', 'GUIZHOU'),
    4: ('YULONG RIVER', 'YANGSHUO'),
    5: ('SLENDER WEST LAKE', 'YANGZHOU'),
    7: ('POTALA PALACE', 'LHASA'),
    8: ('JINGXIU PARK', 'BAODING'),
    9: ('ERHAI LAKE', 'DALI'),
    10: ('HUANGSHAN', 'ANHUI'),
    11: ("XI'AN CITY WALL", 'SHAANXI'),
    12: ('ZIGONG LANTERNS', 'SICHUAN'),
    13: ('MINGSHA MOUNTAIN', 'DUNHUANG'),
}
NAME_SIZE = 150; MAX_W = 990; NAME_Y = 520   # top of the name block, clear of the Reels header
def label(name, pill):
    nf = ImageFont.truetype(NAME_FONT, NAME_SIZE)
    while nf.getbbox(name)[2] - nf.getbbox(name)[0] > MAX_W:
        nf = ImageFont.truetype(NAME_FONT, nf.size - 4)
    pf = ImageFont.truetype(PILL_FONT, 54)
    fg = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(fg)
    l, t, r, b = nf.getbbox(name); nw = r - l
    nx = (W - nw) // 2 - l; ny = NAME_Y - t
    d.text((nx, ny), name, font=nf, fill=(255, 255, 255, 255))
    name_bottom = NAME_Y + (b - t)
    pl, pt, pr, pb = pf.getbbox(pill); pw, ph = pr - pl, pb - pt
    padx, pady = 30, 18; bx0 = (W - pw) // 2 - padx; by0 = name_bottom + 34
    box = (bx0, by0, bx0 + pw + 2 * padx, by0 + ph + 2 * pady)
    d.rounded_rectangle(box, radius=8, fill=YELLOW + (255,))
    d.text((bx0 + padx - pl, by0 + pady - pt), pill, font=pf, fill=(17, 17, 17, 255))
    # soft drop shadow under everything (like the reference), mostly for the white name
    a = fg.split()[3]
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sh.putalpha(a.point(lambda v: int(v * 0.55)))
    sh = sh.transform((W, H), Image.AFFINE, (1, 0, 0, 0, 1, -5)).filter(ImageFilter.GaussianBlur(14))
    return Image.alpha_composite(sh, fg)
import importlib
_P = importlib.import_module(os.environ.get('PLAN', 'plan_v')); LABELS = getattr(_P, 'LABELS', LABELS)
LDIR = os.environ.get('LABELDIR', 'labels_v')
if __name__ == '__main__':
    os.makedirs(f'{here}/{LDIR}', exist_ok=True)
    for k, (n, p) in LABELS.items():
        label(n, p).save(f'{here}/{LDIR}/label{k:02d}.png'); print(k, n, p)
