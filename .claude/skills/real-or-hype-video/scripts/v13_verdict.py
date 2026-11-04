import os,sys
from PIL import Image,ImageDraw,ImageFont
os.chdir(sys.argv[1]); W,H=1080,1920; O='v13/ov/'
ANTON='fonts/Anton-Regular.ttf'; EMO='/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf'
GREEN=(40,220,90,255); RED=(240,50,50,255); WHITE=(255,255,255,255); BLACK=(0,0,0,255)
def emoji(ch,size):
    f=ImageFont.truetype(EMO,109); im=Image.new('RGBA',(140,140)); ImageDraw.Draw(im).text((4,4),ch,font=f,embedded_color=True)
    im=im.crop(im.getbbox()); return im.resize((size,int(size*im.height/im.width)),Image.LANCZOS)
def box(kind,s):
    im=Image.new('RGBA',(s+12,s+12)); d=ImageDraw.Draw(im)
    fill=GREEN if kind=='tick' else RED
    d.rectangle((4,4,s+8,s+8),fill=fill,outline=BLACK,width=8)
    if kind=='tick':
        pts=[(s*0.22+6,s*0.52+6),(s*0.43+6,s*0.74+6),(s*0.84+6,s*0.22+6)]
        d.line(pts,fill=BLACK,width=22,joint='curve'); d.line(pts,fill=WHITE,width=12,joint='curve')
    else:
        for a,b in [((s*0.25+6,s*0.25+6),(s*0.75+6,s*0.75+6)),((s*0.75+6,s*0.25+6),(s*0.25+6,s*0.75+6))]:
            d.line([a,b],fill=BLACK,width=22); d.line([a,b],fill=WHITE,width=12)
    return im
def txt(t,size,col):
    f=ImageFont.truetype(ANTON,size); d=ImageDraw.Draw(Image.new('RGBA',(1,1))); b=d.textbbox((0,0),t,font=f,stroke_width=7)
    im=Image.new('RGBA',(b[2]-b[0]+10,b[3]-b[1]+10)); ImageDraw.Draw(im).text((5-b[0],5-b[1]),t,font=f,fill=col,stroke_width=7,stroke_fill=BLACK); return im
def row(c,y,parts):
    tw=sum(p.width for p in parts)+16*(len(parts)-1); x=int(W/2-tw/2)
    for p in parts: c.alpha_composite(p,(x,int(y-p.height/2))); x+=p.width+16
size=130
c=Image.new('RGBA',(W,H)); row(c,H*0.40,[txt('TREES',size,WHITE),box('tick',int(size*0.82)),txt('REAL',size,GREEN)]); c.save(O+'v1.png')
row(c,H*0.50,[txt('MALL',size,WHITE),box('cross',int(size*0.82)),txt('HYPE',size,RED),emoji('💩',int(size*0.6))]); c.save(O+'v2.png')
print('ok')
