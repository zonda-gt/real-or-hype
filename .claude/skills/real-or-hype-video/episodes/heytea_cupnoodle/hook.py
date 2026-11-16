# Aesthetic hook text: three transparent 1080x1920 layers (revealed one after another in finish.py).
#   k0  small tracked caps  "HEYTEA × CUP NOODLES"   Inter Medium 30 px, letter-spacing 9 px
#   k1  "a cup noodle"      Instrument Serif 132 px
#   k2  "you drink?"        Instrument Serif Italic 132 px
# Soft drop shadow only (no outline). Usage: hook.py <outdir> [y_top]
import sys,os
from PIL import Image,ImageDraw,ImageFont,ImageFilter
D=os.path.dirname(os.path.abspath(__file__)); out=sys.argv[1]; Y=int(sys.argv[2]) if len(sys.argv)>2 else 300
INTER='/usr/share/fonts/opentype/inter/InterDisplay-Medium.otf'
W,H=1080,1920
def layer(draw_fn):
    txt=Image.new('RGBA',(W,H),(0,0,0,0)); draw_fn(ImageDraw.Draw(txt))
    a=txt.getchannel('A'); sh=Image.new('RGBA',(W,H),(0,0,0,0)); sh.putalpha(a.point(lambda v:int(v*0.55)))
    sh=sh.filter(ImageFilter.GaussianBlur(10)); base=Image.new('RGBA',(W,H),(0,0,0,0))
    base.alpha_composite(sh,(0,5)); base.alpha_composite(txt); return base
def tracked(d,y,s,f,sp,fill):
    w=sum(d.textlength(c,font=f) for c in s)+sp*(len(s)-1); x=(W-w)/2
    for c in s: d.text((x,y),c,font=f,fill=fill); x+=d.textlength(c,font=f)+sp
small=ImageFont.truetype(INTER,30); ser=ImageFont.truetype(D+'/fonts/InstrumentSerif-Regular.ttf',132); it=ImageFont.truetype(D+'/fonts/InstrumentSerif-Italic.ttf',132)
def k0(d):
    tracked(d,Y,'HEYTEA  ×  CUP NOODLES',small,9,(255,255,255,235))
    d.line([(W/2-60,Y+56),(W/2+60,Y+56)],fill=(255,255,255,200),width=2)
def k1(d):
    s='a cup noodle'; d.text(((W-d.textlength(s,font=ser))/2,Y+80),s,font=ser,fill=(255,255,255,255))
def k2(d):
    s='you drink?'; d.text(((W-d.textlength(s,font=it))/2,Y+215),s,font=it,fill=(255,236,170,255))
for n,fn in (('k0',k0),('k1',k1),('k2',k2)): layer(fn).save(f'{out}/{n}.png')
# soft top gradient behind the text (black 45% -> 0 over the top 760 px)
g=Image.new('RGBA',(W,H),(0,0,0,0)); px=g.load()
for y in range(760):
    a=int(115*(1-y/760)**1.6)
    for x in range(W): px[x,y]=(0,0,0,a)
g.save(f'{out}/kgrad.png')
print('hook layers ->',out)
