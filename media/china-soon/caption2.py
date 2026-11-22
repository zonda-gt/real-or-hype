# Caption matched to the original reel's text (white, thin dark outline), same place and size; plus a feathered blur mask.
import sys, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
out,maskout=sys.argv[1],sys.argv[2]
W,H=1080,1920; FP='/usr/share/fonts/opentype/inter/Inter-Bold.otf'
l1,l2="don't worry,","you'll be in China soon"
TARGET=708-6  # line-2 width incl. flag, from the original (472 px at 720 wide)
def wid(s):
    F=ImageFont.truetype(FP,s); fh=int(s*0.72); return F.getlength(l2)+int(s*0.28)+int(fh*1.5)
s=20
while wid(s)<TARGET: s+=1
F=ImageFont.truetype(FP,s); fh=int(s*0.72); fw=int(fh*1.5); gap=int(s*0.28)
def flag(w,h):
    im=Image.new('RGBA',(w,h),(222,41,16,255)); d=ImageDraw.Draw(im); u=w/30
    def star(cx,cy,r,rot=0):
        d.polygon([(cx+(r if k%2==0 else r*.382)*math.cos(math.radians(-90+rot+36*k)),cy+(r if k%2==0 else r*.382)*math.sin(math.radians(-90+rot+36*k))) for k in range(10)],fill=(255,222,0,255))
    star(5*u,5*u,3*u)
    for (x,y) in [(10,2),(12,4),(12,7),(10,9)]: star(x*u,y*u,u,math.degrees(math.atan2(5-y,5-x))+90)
    m=Image.new('L',(w,h),0); ImageDraw.Draw(m).rounded_rectangle([0,0,w-1,h-1],radius=max(2,h//8),fill=255); im.putalpha(m); return im
# original: line tops at ~546 and ~609 (1080 space), lines centred on x=540
top1=546; lh=int(s*1.19)
w1=F.getlength(l1); w2=F.getlength(l2)+gap+fw
x1=(W-w1)/2; x2=(W-w2)/2
asc=F.getbbox('d')[1]
img=Image.new('RGBA',(W,H),(0,0,0,0))
sh=Image.new('RGBA',(W,H),(0,0,0,0)); sd=ImageDraw.Draw(sh)
for (x,y,t) in [(x1,top1-asc,l1),(x2,top1-asc+lh,l2)]: sd.text((x+1,y+3),t,font=F,fill=(0,0,0,170))
img=Image.alpha_composite(img,sh.filter(ImageFilter.GaussianBlur(5))); d=ImageDraw.Draw(img)
for (x,y,t) in [(x1,top1-asc,l1),(x2,top1-asc+lh,l2)]:
    d.text((x,y),t,font=F,fill='white',stroke_width=3,stroke_fill=(40,30,30,235))
fy=int(top1+lh+(F.getbbox('o')[3]-asc)-fh)+2
img.alpha_composite(flag(fw,fh),(int(x2+F.getlength(l2)+gap),fy))
img.save(out)
m=Image.new('L',(W,H),0); ImageDraw.Draw(m).rounded_rectangle([150,515,930,700],radius=60,fill=255)
m.filter(ImageFilter.GaussianBlur(22)).save(maskout)
print('font',s)
