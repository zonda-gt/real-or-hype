import subprocess, numpy as np, cv2
from scipy import ndimage
import sys
x0,y0,w,h=[int(v) for v in sys.argv[1:5]]; OUTP=sys.argv[5]
raw=subprocess.run(["ffmpeg","-v","error","-i","reel.mp4","-vf",f"crop={w}:{h}:{x0}:{y0}","-f","rawvideo","-pix_fmt","bgr24","-"],capture_output=True).stdout
fr=np.frombuffer(raw,np.uint8).reshape(-1,h,w,3).astype(np.float32)
med=np.median(fr,0); mad=np.median(np.abs(fr-med),0).max(-1)
mx,mn=med.max(-1),med.min(-1)
hsv=cv2.cvtColor(med.astype(np.uint8),cv2.COLOR_BGR2HSV)
whiteish=mn>200; darkish=mx<100; flagc=(hsv[...,1]>90)&(hsv[...,2]>90)
textcol=whiteish|darkish|flagc
seed=(textcol)&(mad<12)
m=ndimage.binary_closing(seed,iterations=2)&textcol
m=ndimage.binary_opening(m,iterations=1)
# keep components touching the white/flag core (drops stray static dark bits of the background)
core=(whiteish|flagc)&(mad<8)
lab,n=ndimage.label(ndimage.binary_dilation(m,iterations=1))
keep=np.unique(lab[core&(lab>0)])
m=np.isin(lab,keep)&m
# flag: fill its interior fully
red=((hsv[...,0]<8)|(hsv[...,0]>172))&(hsv[...,1]>150)&(mad<15)
lr,nr=ndimage.label(ndimage.binary_closing(red,iterations=2)); sz=ndimage.sum(red,lr,range(1,nr+1))
yy,xx=np.where(lr==1+sz.argmax()); print("flag bbox",xx.min(),xx.max(),yy.min(),yy.max())
box=np.zeros_like(red); box[yy.min():yy.max()+1,xx.min():xx.max()+1]=True
fl=ndimage.binary_fill_holes(ndimage.binary_closing(flagc&(mad<20)&box,iterations=3))&box
m=(m & ~(flagc & ~box)) | fl
lab2,n2=ndimage.label(m); sz2=ndimage.sum(m,lab2,range(1,n2+1))
m=np.isin(lab2,1+np.where(sz2>=25)[0])
a=cv2.GaussianBlur(m.astype(np.float32),(3,3),0.7)
col=med.copy(); col[whiteish&m]=255
cv2.imwrite(OUTP,np.dstack([col.astype(np.uint8),(a*255).astype(np.uint8)]))
for name,bgc in [("mag",(255,0,255)),("blk",(30,30,30))]:
    bg=np.full((h,w,3),bgc,np.float32); aa=a[...,None]
    cv2.imwrite(OUTP.replace(".png",f"_prev_{name}.png"),(col*aa+bg*(1-aa)).astype(np.uint8))
