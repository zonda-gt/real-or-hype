# PIL overlay cards (1080x1920 RGBA). Montserrat ExtraBold, black outline; CJK in WenQuanYi Zen Hei.
from PIL import Image,ImageDraw,ImageFont
F='../../.claude/skills/real-or-hype-video/scripts/Montserrat-ExtraBold.ttf'; CJK='/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
WHITE=(255,255,255); YEL=(255,226,26); GREEN=(80,220,120)
def card(name,rows):
    im=Image.new('RGBA',(1080,1920),(0,0,0,0)); d=ImageDraw.Draw(im)
    for text,size,y,col,font in rows:
        f=ImageFont.truetype(font or F,size); w=d.textlength(text,font=f)
        while w>1000: size-=2; f=ImageFont.truetype(font or F,size); w=d.textlength(text,font=f)
        d.text(((1080-w)/2,y),text,font=f,fill=col,stroke_width=max(5,size//11),stroke_fill=(0,0,0))
    im.save(f'ov/{name}.png')
# hooks / context lines (top, y 120-260)
card('titleA',[("Breakfast with giraffes",64,130,WHITE,None),("Huzhou, China",48,215,YEL,None)])
card('titleC',[("How to have breakfast",60,120,WHITE,None),("with giraffes in China",60,195,WHITE,None)])
card('kenya',[("Giraffe Manor, KENYA",56,130,WHITE,None),("$1,400+ / night",96,205,YEL,None),("per person",44,320,WHITE,None)])
card('china',[("Giraffe Manor, CHINA",56,130,WHITE,None),("Huzhou · 2 h from Shanghai",44,205,YEL,None)])
# price punch (mid-upper)
card('price',[("1 night + breakfast",52,560,WHITE,None),("¥1,000",150,630,YEL,None),("≈ $140",84,800,WHITE,None)])
card('price_b',[("CHINA",52,560,WHITE,None),("¥1,000",150,630,YEL,None),("≈ $140 / night",76,800,WHITE,None)])
card('tenx',[("10x",200,600,YEL,None),("cheaper",90,830,WHITE,None)])
card('name',[("湖州长颈鹿庄园",92,560,YEL,CJK),("Giraffe Manor, Huzhou",56,690,WHITE,None)])
card('time',[("Breakfast 7:00",70,580,WHITE,None),("Be there 6:30",96,680,YEL,None)])
print('ok')
