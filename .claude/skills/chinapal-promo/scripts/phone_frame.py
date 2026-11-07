# usage: python3 phone_frame.py screen.png out.png [width]  -> screen inside an iPhone-style frame (RGBA)
import sys
from PIL import Image,ImageDraw
def phone(path,w=520):
    sc=Image.open(path).convert('RGB'); h=int(w*sc.height/sc.width); sc=sc.resize((w,h),Image.LANCZOS)
    b=18; R=78; W,H=w+2*b,h+2*b
    m=Image.new('L',(w,h),0); ImageDraw.Draw(m).rounded_rectangle((0,0,w-1,h-1),R-b,fill=255)
    ph=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(ph)
    d.rounded_rectangle((0,0,W-1,H-1),R,fill=(28,28,30)); d.rounded_rectangle((3,3,W-4,H-4),R-3,outline=(70,70,74),width=2)
    ph.paste(sc,(b,b),m); d.rounded_rectangle((W//2-62,b+14,W//2+62,b+48),17,fill=(0,0,0))
    return ph
if __name__=='__main__': phone(sys.argv[1],int(sys.argv[3]) if len(sys.argv)>3 else 520).save(sys.argv[2])
