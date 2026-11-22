# Caption PNG 1080x1920: "don't worry, / you'll be in China soon [flag]" in Instagram-like style.
import sys, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
out=sys.argv[1]
W,H=1080,1920
F=ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-Bold.otf',10)
l1,l2="don't worry,","you'll be in China soon"
# size so line 1 is ~360 px wide (as measured on the original)
s=10
while ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-Bold.otf',s).getlength(l1)<360: s+=1
F=ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-Bold.otf',s)
fh=int(s*0.75); fw=int(fh*1.5)
def flag(w,h):
    im=Image.new('RGBA',(w,h),(222,41,16,255)); d=ImageDraw.Draw(im); u=w/30
    def star(cx,cy,r,rot=0):
        pts=[]
        for k in range(10):
            a=math.radians(-90+rot+36*k); rr=r if k%2==0 else r*0.382
            pts.append((cx+rr*math.cos(a),cy+rr*math.sin(a)))
        d.polygon(pts,fill=(255,222,0,255))
    star(5*u,5*u,3*u)
    for (x,y) in [(10,2),(12,4),(12,7),(10,9)]:
        rot=math.degrees(math.atan2(5-y,5-x))+90
        star(x*u,y*u,1*u,rot)
    m=Image.new('L',(w,h),0); ImageDraw.Draw(m).rounded_rectangle([0,0,w-1,h-1],radius=max(2,h//8),fill=255)
    im.putalpha(m); return im
img=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(img)
y0=560; lh=int(s*1.22)
w1=F.getlength(l1); w2=F.getlength(l2)+12+fw
x1=(W-w1)/2; x2=(W-w2)/2
sh=Image.new('RGBA',(W,H),(0,0,0,0)); sd=ImageDraw.Draw(sh)
for (x,y,t) in [(x1,y0,l1),(x2,y0+lh,l2)]:
    sd.text((x+2,y+3),t,font=F,fill=(0,0,0,150))
sh=sh.filter(ImageFilter.GaussianBlur(4)); img=Image.alpha_composite(img,sh); d=ImageDraw.Draw(img)
d.text((x1,y0),l1,font=F,fill='white'); d.text((x2,y0+lh),l2,font=F,fill='white')
fy=y0+lh+int(s*0.22); img.alpha_composite(flag(fw,fh),(int(x2+F.getlength(l2)+12),fy))
img.save(out)
