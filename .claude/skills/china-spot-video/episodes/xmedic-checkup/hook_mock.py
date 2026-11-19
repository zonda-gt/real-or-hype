# Mock up text-hook designs on real hook frames and tile them for comparison.
import sys
from PIL import Image,ImageDraw,ImageFont,ImageFilter
SK='/home/user/real-or-hype/.claude/skills/china-spot-video/fonts'; RH='/home/user/real-or-hype/.claude/skills/real-or-hype-video/scripts'
SERIF=f'{SK}/dm-serif-display-latin-400-normal.ttf'; POP=f'{SK}/poppins-latin-600-normal.ttf'; MONT=f'{RH}/Montserrat-ExtraBold.ttf'; HAND=f'{SK}/chewy-latin-400-normal.ttf'
YEL=(255,236,140); INK=(20,20,20); WHITE=(255,255,255)
def F(p,s): return ImageFont.truetype(p,s)
def fit(d,t,font,path,size,maxw):
    while d.textlength(t,font=font)>maxw: size-=3; font=F(path,size)
    return font
def boxed(im,text,path,size,cy,bg,fg=INK,padx=28,pady=12,rot=0,maxw=960,shadow=True):
    d=ImageDraw.Draw(im); f=fit(d,text,F(path,size),path,size,maxw); l,t,r,b=d.textbbox((0,0),text,font=f)
    tile=Image.new('RGBA',(r-l+2*padx,b-t+2*pady),bg+(255,)); ImageDraw.Draw(tile).text((padx-l,pady-t),text,font=f,fill=fg)
    if rot: tile=tile.rotate(rot,expand=True,resample=Image.BICUBIC)
    x=int(540-tile.width/2); y=int(cy-tile.height/2)
    if shadow:
        sh=Image.new('RGBA',im.size,(0,0,0,0)); m=Image.new('RGBA',tile.size,(0,0,0,110)); sh.paste(m,(x+7,y+9),tile); im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6)))
    im.alpha_composite(tile,(x,y)); return y+tile.height
def text(im,t,path,size,cy,fill=WHITE,stroke=0,sc=(0,0,0),spacing=0,shadow=True,maxw=980):
    d=ImageDraw.Draw(im); f=fit(d,t,F(path,size),path,size,maxw)
    if spacing: t=(' '*0).join(t)  # placeholder
    w=d.textlength(t,font=f); l,tp,r,b=d.textbbox((0,0),t,font=f); x=540-w/2; y=cy-(b+tp)/2
    if shadow:
        sh=Image.new('RGBA',im.size,(0,0,0,0)); ImageDraw.Draw(sh).text((x+4,y+6),t,font=f,fill=(0,0,0,170),stroke_width=stroke,stroke_fill=(0,0,0,170)); im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(7)))
    ImageDraw.Draw(im).text((x,y),t,font=f,fill=fill,stroke_width=stroke,stroke_fill=sc); return y+b
def grad(im,y0,y1,a=150):
    g=Image.new('RGBA',im.size,(0,0,0,0)); d=ImageDraw.Draw(g); mid=(y0+y1)/2
    for y in range(int(y0),int(y1)): d.line([(0,y),(1080,y)],fill=(0,0,0,int(a*(1-abs(y-mid)/((y1-y0)/2))**0.8)))
    im.alpha_composite(g)

def design(n,bg,top,big,small=None):
    im=Image.open(bg).convert('RGBA').resize((1080,1920))
    if n==1:   # one system: white box (topic) + big yellow box (hook), same serif
        y=boxed(im,top,SERIF,78,700,WHITE); boxed(im,big.replace('|',' '),SERIF,128,y+80,YEL)
    elif n==2: # magazine: kicker in letter-spaced sans + headline in big white serif, soft dark band
        grad(im,520,1060,170); text(im,' '.join(top.upper()),POP,40,610,fill=YEL,shadow=False)
        y=text(im,big.split('|')[0],SERIF,150,740); text(im,big.split('|')[1] if '|' in big else '',SERIF,150,y+90)
    elif n==3: # bold sans: topic huge white, hook yellow, black outline (one family)
        y=text(im,top.upper(),MONT,92,680,stroke=7); text(im,big.replace('|',' ').upper(),MONT,112,y+90,fill=YEL,stroke=8)
    elif n==4: # stacked yellow highlight, two sizes, one block (topic line on yellow too)
        y=boxed(im,big.replace('|',' '),SERIF,124,700,YEL); boxed(im,top,SERIF,74,y+58,YEL,shadow=False)
    return im.convert('RGB')
bg,top,big,out=sys.argv[1:5]
ims=[design(n,bg,top,big) for n in (1,2,3,4)]
W=Image.new('RGB',(4*540+30,960+70),(30,30,30)); d=ImageDraw.Draw(W)
for k,im in enumerate(ims):
    W.paste(im.resize((540,960)),(k*550,60)); d.text((k*550+10,10),f'option {k+1}',font=F(POP,36),fill=WHITE)
W.save(out)
