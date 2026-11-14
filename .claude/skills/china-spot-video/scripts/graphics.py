# Reference-style graphics from <workdir>/plan.py -> <workdir>/ov/*.png (1080x1920 RGBA).
#   TITLE = ["CHINA'S", "Giraffe Hotel"]  serif lines on pale-yellow highlight boxes, over the collage
#   TAG   = "breakfast included"           handwritten tag under the title (or None)
#   LABELS= [("capybara", word_idx), ...]   handwritten labels on things
#   CARDS = [(top, big, bottom, i0, i1), ...] serif info cards (big line on yellow), shown from word i0 to i1
#   CTA   = ('Comment "GIRAFFE"', word_idx) or None   handwritten sticker at the end
import sys,os
from PIL import Image,ImageDraw,ImageFont
SK=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SERIF=f'{SK}/fonts/dm-serif-display-latin-400-normal.ttf'; HAND=f'{SK}/fonts/chewy-latin-400-normal.ttf'
YEL=(255,240,150); WHITE=(255,255,255); INK=(20,20,20)
W=sys.argv[1]; sys.path.insert(0,W); import plan as P
os.makedirs(f'{W}/ov',exist_ok=True)
def new(): return Image.new('RGBA',(1080,1920),(0,0,0,0))
def box(im,text,size,cx,y,bg,rot=0,padx=26,pady=10):
    f=ImageFont.truetype(SERIF,size); d=ImageDraw.Draw(im); l,t,r,b=d.textbbox((0,0),text,font=f)
    while r-l>960: size-=4; f=ImageFont.truetype(SERIF,size); l,t,r,b=d.textbbox((0,0),text,font=f)
    tile=Image.new('RGBA',(r-l+2*padx,b-t+2*pady),bg+(255,)); ImageDraw.Draw(tile).text((padx-l,pady-t),text,font=f,fill=INK)
    if rot: tile=tile.rotate(rot,expand=True,resample=Image.BICUBIC)
    sh=Image.new('RGBA',tile.size,(0,0,0,0)); sh.paste((0,0,0,90),mask=tile.split()[3])
    x=int(cx-tile.width/2); im.alpha_composite(sh,(x+6,y+8)); im.alpha_composite(tile,(x,y)); return y+tile.height
def hand(im,text,size,cx,y,rot=-5):
    f=ImageFont.truetype(HAND,size); tmp=Image.new('RGBA',(1080,400),(0,0,0,0)); d=ImageDraw.Draw(tmp)
    while d.textlength(text,font=f)>980: size-=4; f=ImageFont.truetype(HAND,size)
    w=d.textlength(text,font=f); d.text(((1080-w)/2,100),text,font=f,fill=WHITE,stroke_width=6,stroke_fill=(40,30,20))
    im.alpha_composite(tmp.rotate(rot,resample=Image.BICUBIC),(int(cx-540),y-100))
im=new(); y=760
for k,line in enumerate(P.TITLE): y=box(im,line,108 if k==0 else 132,500+80*k,y-6*k,YEL)
if getattr(P,'TAG',None): hand(im,P.TAG,62,640,y+100,rot=-6)
im.save(f'{W}/ov/title.png')
for k,(txt,_) in enumerate(getattr(P,'LABELS',[])):
    im=new(); hand(im,txt,74,540,1260,rot=-4); im.save(f'{W}/ov/label{k}.png')
for k,(top,big,bot,_,_) in enumerate(getattr(P,'CARDS',[])):
    im=new(); y=560
    if top: y=box(im,top,62,540,y,WHITE)+4
    y=box(im,big,150,540,y,YEL)+4
    if bot: box(im,bot,58,540,y,WHITE)
    im.save(f'{W}/ov/card{k}.png')
if getattr(P,'CTA',None):
    im=new(); hand(im,P.CTA[0],92,540,1250,rot=-5); im.save(f'{W}/ov/cta.png')
print('graphics ->',f'{W}/ov')
