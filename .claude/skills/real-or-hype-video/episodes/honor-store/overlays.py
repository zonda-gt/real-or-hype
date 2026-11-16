# Title cards in her style: soft serif (DM Serif Display), white, soft drop shadow, colour emoji.
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
os.makedirs('ov', exist_ok=True)
SERIF = 'fonts/dm.woff'
SANS = '/home/user/real-or-hype/.claude/skills/real-or-hype-video/scripts/Montserrat-ExtraBold.ttf'
EMOJI = '/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf'
W, H = 1080, 1920

def emoji_img(ch, size):
    f = ImageFont.truetype(EMOJI, 109)
    im = Image.new('RGBA', (160, 160), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((10, 10), ch, font=f, embedded_color=True)
    im = im.crop(im.getbbox())
    return im.resize((size, int(size * im.height / im.width)), Image.LANCZOS)

def title(name, lines, y0, size=118, emoji=None, font=SERIF, fill=(255, 255, 255, 255)):
    f = ImageFont.truetype(font, size)
    txt = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(txt)
    y = y0; boxes = []
    for i, ln in enumerate(lines):
        bb = d.textbbox((0, 0), ln, font=f); w = bb[2] - bb[0]
        ew = int(size * 0.9) + 18 if (emoji and i == len(lines) - 1) else 0
        x = (W - w - ew) // 2 - bb[0]
        d.text((x, y), ln, font=f, fill=fill); boxes.append((x + bb[2], y, bb))
        y += int(size * 1.08)
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    sh.paste((0, 0, 0, 170), (0, 0), txt.split()[3].point(lambda a: a))
    sh = sh.filter(ImageFilter.GaussianBlur(9))
    out = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    out.alpha_composite(sh, (4, 7)); out.alpha_composite(txt)
    if emoji:
        xe, ye, bb = boxes[-1]
        e = emoji_img(emoji, int(size * 0.9)); out.alpha_composite(e, (xe + 18, ye + bb[1] + (bb[3] - bb[1] - e.height) // 2))
    out.save(f'ov/{name}.png')

# A: robot phone hook
title('titleA', ['Honor’s ROBOT', 'phone?!'], 230, emoji='🤖')
# B: countdown hook + item badges
title('titleB', ['3 crazy gadgets', 'in a phone store'], 230, size=108, emoji='🤯')
for n in (3, 2, 1):
    title(f'num{n}', [f'#{n}'], 210, size=190)
# price card (both)
title('price', ['¥9,999'], 700, size=170, font=SANS, fill=(255, 226, 26, 255))
title('price2', ['≈ $1,400'], 900, size=110, font=SANS)
print('ok')
