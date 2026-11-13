# End card CTA. FREE is the hero (big Anton, title yellow); the rest of the sentence sits around it in Montserrat.
#   DM US FOR A        (small, DM in yellow)
#   FREE               (big)
#   PERSONALIZED ITINERARY  (small, letter-spaced)
# The video under it is blurred/dimmed by apply_labels_v.py, so the text only needs a soft shadow.
import os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, here)
from labels_v import NAME_FONT, PILL_FONT, W, H
YEL = (242, 219, 17); WHITE = (255, 255, 255)
LINES = [  # (font, size, tracking px, runs, gap after)
    (PILL_FONT, 66, 3, [('DM', YEL), (' US FOR A', WHITE)], 30),
    (NAME_FONT, 300, 4, [('FREE', YEL)], 34),
    (PILL_FONT, 54, 4, [('PERSONALIZED ITINERARY', WHITE)], 0),
]
CENTER_Y = 900
def tracked_len(f, s, tr): return sum(f.getlength(c) for c in s) + tr * (len(s) - 1)
def cta():
    fg = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(fg)
    blocks = []
    for path, size, tr, runs, gap in LINES:
        f = ImageFont.truetype(path, size); text = ''.join(t for t, _ in runs)
        top, bot = f.getbbox('HDMFREPI')[1], f.getbbox('HDMFREPI')[3]
        blocks.append((f, tr, runs, gap, top, bot - top, tracked_len(f, text, tr)))
    total = sum(b[5] + b[3] for b in blocks)
    y = CENTER_Y - total // 2
    for f, tr, runs, gap, top, h, w in blocks:
        x = (W - w) / 2
        for t, c in runs:
            for ch in t:
                d.text((x, y - top), ch, font=f, fill=c + (255,)); x += f.getlength(ch) + tr
        y += h + gap
    a = fg.split()[3]
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sh.putalpha(a.point(lambda v: int(v * 0.45)))
    sh = sh.transform((W, H), Image.AFFINE, (1, 0, 0, 0, 1, -4)).filter(ImageFilter.GaussianBlur(9))
    return Image.alpha_composite(sh, fg), [round(b[6]) for b in blocks]
if __name__ == '__main__':
    im, widths = cta(); print('line widths', widths)
    im.save(f"{here}/{os.environ.get('LABELDIR', 'labels_v')}/cta.png")
