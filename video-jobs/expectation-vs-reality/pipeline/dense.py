#!/usr/bin/env python3
# dense.py id step [start end] [H] -> media/dense/<id>_<step>.jpg ; frames every step s, 12 per row, labelled
import sys,os,subprocess,io
from PIL import Image,ImageDraw
i=sys.argv[1]; step=float(sys.argv[2]); f=f'media/dy/{i}.mp4'
dur=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f],capture_output=True,text=True).stdout)
s=float(sys.argv[3]) if len(sys.argv)>3 else 0; e=float(sys.argv[4]) if len(sys.argv)>4 else dur
H=int(sys.argv[5]) if len(sys.argv)>5 else 220
os.makedirs('media/dense',exist_ok=True)
tmp=f'/tmp/dense_{i}'; os.makedirs(tmp,exist_ok=True)
subprocess.run(['ffmpeg','-v','error','-y','-ss',str(s),'-to',str(e),'-i',f,'-vf',f'fps=1/{step},scale=-2:{H}',f'{tmp}/%04d.png'])
fs=sorted(os.listdir(tmp)); ims=[Image.open(f'{tmp}/{x}').convert('RGB') for x in fs]
for x in fs: os.remove(f'{tmp}/{x}')
if not ims: sys.exit('no frames')
w=ims[0].width; per=12 if w<H else 6
rows=(len(ims)+per-1)//per
sh=Image.new('RGB',(per*(w+2),rows*(H+2)),(0,0,0)); d=ImageDraw.Draw(sh)
for k,im in enumerate(ims):
    x=(k%per)*(w+2); y=(k//per)*(H+2); sh.paste(im,(x,y)); d.rectangle((x,y,x+34,y+12),fill=(0,0,0)); d.text((x+2,y),f'{s+k*step:.1f}',fill=(255,255,0))
out=f'media/dense/{i}_{step}.jpg'; sh.save(out,quality=82); print(out,sh.size)
