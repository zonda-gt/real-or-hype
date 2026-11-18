# Redraw <workdir>/ov/title.png with the serif title near the top (plan.TITLE_Y), for heroes whose subject fills the middle.
# Same look as graphics.py (DM Serif on pale-yellow boxes + Chewy tag). usage: title_top.py <workdir>   (run after graphics.py)
import sys,os
from PIL import Image,ImageDraw,ImageFont
SK='/home/user/real-or-hype/.claude/skills/china-spot-video'
SERIF=f'{SK}/fonts/dm-serif-display-latin-400-normal.ttf'; HAND=f'{SK}/fonts/chewy-latin-400-normal.ttf'
YEL=(255,240,150); WHITE=(255,255,255); INK=(20,20,20)
W=sys.argv[1]; sys.path.insert(0,W); import plan as P
def box(im,text,size,cx,y,bg,padx=26,pady=10):
    f=ImageFont.truetype(SERIF,size); d=ImageDraw.Draw(im); l,t,r,b=d.textbbox((0,0),text,font=f)
    while r-l>960: size-=4; f=ImageFont.truetype(SERIF,size); l,t,r,b=d.textbbox((0,0),text,font=f)
    tile=Image.new('RGBA',(r-l+2*padx,b-t+2*pady),bg+(255,)); ImageDraw.Draw(tile).text((padx-l,pady-t),text,font=f,fill=INK)
    sh=Image.new('RGBA',tile.size,(0,0,0,0)); sh.paste((0,0,0,90),mask=tile.split()[3])
    x=int(cx-tile.width/2); im.alpha_composite(sh,(x+6,y+8)); im.alpha_composite(tile,(x,y)); return y+tile.height
def hand(im,text,size,cx,y,rot=-5):
    f=ImageFont.truetype(HAND,size); tmp=Image.new('RGBA',(1080,400),(0,0,0,0)); d=ImageDraw.Draw(tmp)
    while d.textlength(text,font=f)>980: size-=4; f=ImageFont.truetype(HAND,size)
    w=d.textlength(text,font=f); d.text(((1080-w)/2,100),text,font=f,fill=WHITE,stroke_width=6,stroke_fill=(40,30,20))
    im.alpha_composite(tmp.rotate(rot,resample=Image.BICUBIC),(int(cx-540),y-100))
im=Image.new('RGBA',(1080,1920),(0,0,0,0)); y=getattr(P,'TITLE_Y',150)
for k,line in enumerate(P.TITLE): y=box(im,line,108 if k==0 else 132,500+80*k,y-6*k,YEL)
if getattr(P,'TAG',None): hand(im,P.TAG,62,640,y+100,rot=-6)
im.save(f'{W}/ov/title.png'); print('title (top) ->',f'{W}/ov/title.png')
