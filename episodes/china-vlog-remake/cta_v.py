# End card CTA: big Anton "DM US" (DM in title yellow) + Montserrat line "for a FREE personalized itinerary" (FREE in yellow).
# The video under it is blurred/dimmed by apply_labels_v.py, so the text only needs a soft shadow.
import os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, here)
from labels_v import NAME_FONT, PILL_FONT, W, H
YEL = (242, 219, 17); WHITE = (255, 255, 255)
HEAD = [('DM', YEL), (' US', WHITE)]
SUB = [[('for a ', WHITE), ('FREE', YEL)], [('personalized itinerary', WHITE)]]
HEAD_SIZE, SUB_SIZE, CENTER_Y = 230, 74, 900
def runs_width(f, runs): return sum(f.getlength(t) for t, _ in runs)
def draw_runs(d, f, runs, y, top):
    x = (W - runs_width(f, runs)) / 2
    for t, c in runs:
        d.text((x, y - top), t, font=f, fill=c + (255,)); x += f.getlength(t)
def cta():
    hf = ImageFont.truetype(NAME_FONT, HEAD_SIZE); sf = ImageFont.truetype(PILL_FONT, SUB_SIZE)
    ht, hb = hf.getbbox('DM US')[1], hf.getbbox('DM US')[3]; st, sb = sf.getbbox('dfhkpy')[1], sf.getbbox('dfhkpy')[3]
    sub_lines = SUB
    rule_gap, rule_h, line_gap = 44, 6, 14
    total = (hb - ht) + rule_gap * 2 + rule_h + len(sub_lines) * (sb - st) + line_gap * (len(sub_lines) - 1)
    y = CENTER_Y - total // 2
    fg = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(fg)
    draw_runs(d, hf, HEAD, y, ht); y += (hb - ht) + rule_gap
    d.rounded_rectangle(((W - 90) // 2, y, (W + 90) // 2, y + rule_h), radius=3, fill=YEL + (255,)); y += rule_h + rule_gap
    for ln in sub_lines:
        draw_runs(d, sf, ln, y, st); y += (sb - st) + line_gap
    a = fg.split()[3]
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sh.putalpha(a.point(lambda v: int(v * 0.45)))
    sh = sh.transform((W, H), Image.AFFINE, (1, 0, 0, 0, 1, -4)).filter(ImageFilter.GaussianBlur(9))
    return Image.alpha_composite(sh, fg), len(sub_lines)
if __name__ == '__main__':
    im, n = cta(); print('sub lines', n)
    im.save(f"{here}/{os.environ.get('LABELDIR', 'labels_v')}/cta.png")
