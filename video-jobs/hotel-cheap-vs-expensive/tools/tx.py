# transformed preview frames: tx.py aid scale oy t1 t2 ...
import sys,subprocess
from PIL import Image,ImageDraw
aid,s,oy=sys.argv[1],float(sys.argv[2]),int(sys.argv[3]); ts=sys.argv[4:]
ims=[]
for t in ts:
    p=f"work/check/{aid}_{t}.png"
    W=int(round(1080*s/2)*2); H=int(round(1920*s/2)*2)
    subprocess.run(["ffmpeg","-v","error","-y","-ss",t,"-i",f"raw/best/{aid}.mp4","-frames:v","1","-vf",f"scale={W}:{H},crop=1080:1920:{(W-1080)//2}:{oy}",p],check=True)
    im=Image.open(p).convert("RGB"); d=ImageDraw.Draw(im)
    d.rectangle([24,1328,936,1538],outline="red",width=6); d.line([(0,220),(1080,220)],fill="cyan",width=4); d.line([(0,1540),(1080,1540)],fill="cyan",width=4); d.line([(940,0),(940,1920)],fill="cyan",width=4)
    d.text((30,240),t,fill="yellow")
    ims.append(im.resize((270,480)))
sheet=Image.new("RGB",(270*len(ims),480))
for i,im in enumerate(ims): sheet.paste(im,(270*i,0))
sheet.save(f"work/check/{aid}_tx.jpg")
