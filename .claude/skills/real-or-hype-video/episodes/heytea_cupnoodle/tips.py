# Numbered tip labels for variant B: "No. 1" (Instrument Serif italic) + tracked caps (Inter Display Medium), soft shadow,
# with a light top gradient. usage: tips.py <outdir> <y_top>
import sys,os
from PIL import Image,ImageDraw,ImageFont,ImageFilter
D=os.path.dirname(os.path.abspath(__file__)); out=sys.argv[1]; Y=int(sys.argv[2])
W,H=1080,1920
it=ImageFont.truetype(D+'/fonts/InstrumentSerif-Italic.ttf',112); cap=ImageFont.truetype('/usr/share/fonts/opentype/inter/InterDisplay-Medium.otf',36)
TIPS=[('No. 1','GO EARLY'),('No. 2','THE LID IS THE NOODLES'),('No. 3','IT\'S SWEET, NOT SAVORY')]
for i,(n,t) in enumerate(TIPS,1):
    txt=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(txt)
    d.text(((W-d.textlength(n,font=it))/2,Y),n,font=it,fill=(255,236,170,255))
    w=sum(d.textlength(c,font=cap) for c in t)+8*(len(t)-1); x=(W-w)/2
    for c in t: d.text((x,Y+150),c,font=cap,fill=(255,255,255,240)); x+=d.textlength(c,font=cap)+8
    a=txt.getchannel('A'); sh=Image.new('RGBA',(W,H),(0,0,0,0)); sh.putalpha(a.point(lambda v:int(v*0.6))); sh=sh.filter(ImageFilter.GaussianBlur(10))
    g=Image.new('RGBA',(W,H),(0,0,0,0)); px=g.load()
    for y in range(Y+320):
        al=int(95*(1-y/(Y+320))**1.4)
        for xx in range(W): px[xx,y]=(0,0,0,al)
    g.alpha_composite(sh,(0,5)); g.alpha_composite(txt); g.save(f'{out}/tip{i}.png')
print('tips ->',out)
