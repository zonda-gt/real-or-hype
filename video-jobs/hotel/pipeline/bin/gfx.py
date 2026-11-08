"""Overlay graphics (PIL RGBA). All text is ours; nothing from source clips."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter

SK = '/home/user/real-or-hype/.claude/skills/real-or-hype-video/scripts/'
ANTON = SK + 'Anton-Regular.ttf'
MONT = SK + 'Montserrat-ExtraBold.ttf'
CJK = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
W, H = 1080, 1920
YELLOW = (255, 214, 0, 255)
GREEN = (62, 220, 120, 255)
RED = (255, 72, 72, 255)
WHITE = (255, 255, 255, 255)
INK = (14, 14, 18, 255)


def font(path, size):
    return ImageFont.truetype(path, size)


def text_size(d, txt, f, stroke=0):
    b = d.textbbox((0, 0), txt, font=f, stroke_width=stroke)
    return b[2] - b[0], b[3] - b[1], b[0], b[1]


def canvas():
    return Image.new('RGBA', (W, H), (0, 0, 0, 0))


def shadowed(img, radius=10, alpha=150, offset=(0, 6)):
    """add soft drop shadow under all non-transparent pixels"""
    a = img.split()[3]
    sh = Image.new('RGBA', img.size, (0, 0, 0, 0))
    sh.putalpha(a.point(lambda v: v * alpha // 255))
    sh = sh.filter(ImageFilter.GaussianBlur(radius))
    out = Image.new('RGBA', img.size, (0, 0, 0, 0))
    out.alpha_composite(sh, offset)
    out.alpha_composite(img)
    return out


def price_stamp(price, usd, x, y, color=YELLOW, size=150, anchor='l', sub_size=40, per_night=True, note=None):
    """big Anton price with a small USD line under it. anchor l/c/r on x."""
    c = canvas(); d = ImageDraw.Draw(c)
    f = font(ANTON, size); fs = font(MONT, sub_size)
    tw, th, ox, oy = text_size(d, price, f, 8)
    sub = f'≈ US${usd}' + (' / night' if per_night else '')
    sw, sh_, sox, soy = text_size(d, sub, fs, 5)
    bw = max(tw, sw)
    if anchor == 'c': x0 = x - tw // 2; sx = x - sw // 2
    elif anchor == 'r': x0 = x - tw; sx = x - sw
    else: x0 = x; sx = x
    d.text((x0 - ox, y - oy), price, font=f, fill=color, stroke_width=8, stroke_fill=INK)
    d.text((sx - sox, y + th + 14 - soy), sub, font=fs, fill=WHITE, stroke_width=5, stroke_fill=INK)
    if note:
        fn = font(MONT, 30); nw, nh, nox, noy = text_size(d, note, fn, 4)
        nx = x - nw // 2 if anchor == 'c' else (x - nw if anchor == 'r' else x)
        d.text((nx - nox, y + th + 14 + sh_ + 12 - noy), note, font=fn, fill=(210, 210, 210, 255), stroke_width=4, stroke_fill=INK)
    return shadowed(c)


def label(lines, x, y, anchor='l', sizes=(60, 40), fonts=(MONT, CJK), colors=(WHITE, (230, 230, 230, 255)), pill=True, gap=10):
    """stacked label lines, optional dark pill behind. lines: list of str"""
    c = canvas(); d = ImageDraw.Draw(c)
    fl = [font(fonts[min(i, len(fonts) - 1)], sizes[min(i, len(sizes) - 1)]) for i in range(len(lines))]
    dims = [text_size(d, t, f, 0) for t, f in zip(lines, fl)]
    bw = max(dm[0] for dm in dims)
    if bw > W - 140:   # shrink to fit the frame width
        k = (W - 140) / bw
        return label(lines, x, y, anchor, tuple(int(s * k) for s in sizes), fonts, colors, pill, gap)
    bh = sum(dm[1] for dm in dims) + gap * (len(lines) - 1)
    padx, pady = 30, 22
    if anchor == 'c': bx = x - bw // 2 - padx
    elif anchor == 'r': bx = x - bw - 2 * padx
    else: bx = x
    if pill:
        d.rounded_rectangle([bx, y, bx + bw + 2 * padx, y + bh + 2 * pady], radius=26, fill=(10, 10, 14, 200))
    cy = y + pady
    for i, (t, f, dm) in enumerate(zip(lines, fl, dims)):
        tx = bx + padx + (bw - dm[0]) // 2 if anchor == 'c' else bx + padx
        d.text((tx - dm[2], cy - dm[3]), t, font=f, fill=colors[min(i, len(colors) - 1)])
        cy += dm[1] + gap
    return c


def title(txt, y, size=86, color=WHITE, fnt=None):
    c = canvas(); d = ImageDraw.Draw(c)
    f = font(fnt or ANTON, size)
    tw, th, ox, oy = text_size(d, txt, f, 7)
    d.text(((W - tw) // 2 - ox, y - oy), txt, font=f, fill=color, stroke_width=7, stroke_fill=INK)
    return shadowed(c)


def vs_badge(cx, cy, r=62):
    c = canvas(); d = ImageDraw.Draw(c)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255, 255), outline=INK, width=6)
    f = font(ANTON, int(r * 1.05))
    tw, th, ox, oy = text_size(d, 'VS', f)
    d.text((cx - tw // 2 - ox, cy - th // 2 - oy), 'VS', font=f, fill=INK)
    return shadowed(c)


def caption(words, active, y, size=64):
    """words: list[str] shown; active: index highlighted yellow. centred at y (top)."""
    c = canvas(); d = ImageDraw.Draw(c)
    f = font(MONT, size)
    sp = text_size(d, ' ', f)[0] + 14
    dims = [text_size(d, w, f, 7) for w in words]
    total = sum(dm[0] for dm in dims) + sp * (len(words) - 1)
    if total > W - 80:  # shrink to fit
        return caption(words, active, y, int(size * (W - 80) / total))
    x = (W - total) // 2
    for i, (w, dm) in enumerate(zip(words, dims)):
        d.text((x - dm[2], y - dm[3]), w, font=f, fill=YELLOW if i == active else WHITE, stroke_width=7, stroke_fill=INK)
        x += dm[0] + sp
    return c


def pick_badge(text, cx, y, color=GREEN):
    c = canvas(); d = ImageDraw.Draw(c)
    f = font(ANTON, 64)
    tw, th, ox, oy = text_size(d, text, f)
    d.rounded_rectangle([cx - tw // 2 - 34, y, cx + tw // 2 + 34, y + th + 36], radius=20, fill=color)
    d.text((cx - tw // 2 - ox, y + 18 - oy), text, font=f, fill=INK)
    return shadowed(c)


def cta(y):
    c = canvas(); d = ImageDraw.Draw(c)
    f1 = font(MONT, 54); f2 = font(ANTON, 120)
    t1 = 'COMMENT'; t2 = 'HOTEL'; t3 = 'for our Shanghai hotel list'
    f3 = font(MONT, 40)
    w1 = text_size(d, t1, f1); w2 = text_size(d, t2, f2); w3 = text_size(d, t3, f3)
    bw = max(w1[0] + 30 + w2[0], w3[0]) + 80
    bh = max(w1[1], w2[1]) + w3[1] + 90
    x0 = (W - bw) // 2
    d.rounded_rectangle([x0, y, x0 + bw, y + bh], radius=34, fill=(255, 255, 255, 245))
    rowh = max(w1[1], w2[1])
    rx = (W - (w1[0] + 30 + w2[0])) // 2
    d.text((rx - w1[2], y + 30 + (rowh - w1[1]) - w1[3] - 8), t1, font=f1, fill=INK)
    d.rounded_rectangle([rx + w1[0] + 14, y + 22, rx + w1[0] + 30 + w2[0] + 16, y + 30 + rowh + 12], radius=16, fill=YELLOW)
    d.text((rx + w1[0] + 30 - w2[2], y + 30 - w2[3]), t2, font=f2, fill=INK)
    d.text(((W - w3[0]) // 2 - w3[2], y + 30 + rowh + 26 - w3[3]), t3, font=f3, fill=(60, 60, 66, 255))
    return shadowed(c)
