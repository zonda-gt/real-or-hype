# PIL overlay PNGs (1080x1920, transparent)
from PIL import Image,ImageDraw,ImageFont
import os
SK='/home/user/real-or-hype/.claude/skills/real-or-hype-video/scripts/'
MB=SK+'Montserrat-ExtraBold.ttf'; AN=SK+'Anton-Regular.ttf'; CJK='/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
COL={'online':((255,212,0),(0,0,0)),'real':((230,57,70),(255,255,255)),'fix':((43,213,118),(0,0,0))}
def F(p,s): return ImageFont.truetype(p,s)
def outlined(d,xy,t,f,fill,ow=5,anchor='la'):
    d.text(xy,t,font=f,fill=fill,stroke_width=ow,stroke_fill=(0,0,0),anchor=anchor)
def tag(kind,label,sub,out):
    im=Image.new('RGBA',(1080,1920),(0,0,0,0)); d=ImageDraw.Draw(im)
    bg,fg=COL[kind]; f=F(MB,62); x,y=70,250
    w=d.textlength(label,font=f); d.rounded_rectangle((x,y,x+w+56,y+92),radius=46,fill=bg+(255,))
    d.text((x+28,y+46),label,font=f,fill=fg,anchor='lm')
    if sub: outlined(d,(x+6,y+112),sub,F(MB,44),(255,255,255),5)
    im.save(out)
def big(kind,out):
    im=Image.new('RGBA',(1080,1920),(0,0,0,0)); d=ImageDraw.Draw(im)
    if kind=='SPOTS':
        d.rounded_rectangle((90,640,990,1000),radius=40,fill=(0,0,0,170))
        outlined(d,(540,735),'COMMENT',F(AN,120),(255,255,255),0,'mm')
        outlined(d,(540,860),'"SPOTS"',F(AN,150),(255,212,0),0,'mm')
        outlined(d,(540,955),'for the best times to go',F(MB,40),(255,255,255),0,'mm')
    elif kind=='REAL':
        outlined(d,(540,820),"LET'S",F(AN,170),(255,255,255),8,'mm')
        outlined(d,(540,1000),"GET REAL",F(AN,210),(43,213,118),8,'mm')
    elif kind=='SCAM':
        outlined(d,(540,700),'照骗?',F(CJK,190),(255,212,0),9,'mm')
        outlined(d,(540,860),'PHOTO SCAM?',F(AN,120),(255,255,255),7,'mm')
    im.save(out)
