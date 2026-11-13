# End call to action: "DM us for a FREE personalized itinerary", with DM and FREE in yellow highlight boxes.
import os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, here)
from labels_v import NAME_FONT, YELLOW, W, H
LINES = [[('DM', True), ('US FOR A', False)], [('FREE', True), ('PERSONALIZED', False)], [('ITINERARY', False)]]
SIZE = 118; LINE_GAP = 26; WORD_GAP = 26; PAD = (18, 10); CENTER_Y = 1060
def cta():
    f = ImageFont.truetype(NAME_FONT, SIZE)
    asc = f.getbbox('HDMFIT')[1]; cap = f.getbbox('HDMFIT')[3] - asc   # cap height for uniform lines
    widths = [sum(f.getbbox(w)[2] - f.getbbox(w)[0] for w, _ in ln) + WORD_GAP * (len(ln) - 1) + sum(2 * PAD[0] for _, hl in ln if hl) for ln in LINES]
    total_h = len(LINES) * (cap + 2 * PAD[1]) + LINE_GAP * (len(LINES) - 1)
    y = CENTER_Y - total_h // 2
    fg = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(fg)
    for ln, lw in zip(LINES, widths):
        x = (W - lw) // 2
        for w, hl in ln:
            l, t, r, b = f.getbbox(w)
            if hl:
                d.rounded_rectangle((x, y, x + (r - l) + 2 * PAD[0], y + cap + 2 * PAD[1]), radius=10, fill=YELLOW + (255,))
                d.text((x + PAD[0] - l, y + PAD[1] - asc), w, font=f, fill=(17, 17, 17, 255)); x += (r - l) + 2 * PAD[0]
            else:
                d.text((x - l, y + PAD[1] - asc), w, font=f, fill=(255, 255, 255, 255)); x += r - l
            x += WORD_GAP
        y += cap + 2 * PAD[1] + LINE_GAP
    # soft dark glow behind the block for readability on any shot, plus a drop shadow like the labels
    a = fg.split()[3]
    glow = Image.new('RGBA', (W, H), (0, 0, 0, 0)); glow.putalpha(a.filter(ImageFilter.MaxFilter(41)).filter(ImageFilter.GaussianBlur(45)).point(lambda v: int(v * 0.55)))
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sh.putalpha(a.point(lambda v: int(v * 0.6)))
    sh = sh.transform((W, H), Image.AFFINE, (1, 0, 0, 0, 1, -5)).filter(ImageFilter.GaussianBlur(10))
    return Image.alpha_composite(Image.alpha_composite(glow, sh), fg), widths
if __name__ == '__main__':
    im, widths = cta(); print('line widths', widths)
    im.save(f"{here}/{os.environ.get('LABELDIR', 'labels_v')}/cta.png")
