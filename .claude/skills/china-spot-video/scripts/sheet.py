# Contact sheet: one frame every STEP s, labelled. usage: sheet.py <video> <step> [start end out.jpg]
import sys,subprocess,io,os
from PIL import Image,ImageDraw,ImageFont
f,step=sys.argv[1],float(sys.argv[2]); start=float(sys.argv[3]) if len(sys.argv)>3 else 0; end=float(sys.argv[4]) if len(sys.argv)>4 else 1e9
d=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f],capture_output=True,text=True).stdout)
end=min(end,d-0.05); TW=200; font=ImageFont.load_default(size=22); ims=[]; t=start
while t<end:
    r=subprocess.run(['ffmpeg','-loglevel','error','-ss',f'{t:.2f}','-i',f,'-frames:v','1','-vf',f'scale={TW}:{TW}:force_original_aspect_ratio=decrease','-f','image2pipe','-vcodec','png','-'],capture_output=True)
    if r.stdout: ims.append((t,Image.open(io.BytesIO(r.stdout)).convert('RGB')))
    t+=step
C=8; h=max(i.height for _,i in ims)
page=Image.new('RGB',(TW*C,(h+4)*((len(ims)+C-1)//C)),'black'); dr=ImageDraw.Draw(page)
for k,(t,im) in enumerate(ims):
    x,y=(k%C)*TW,(k//C)*(h+4); page.paste(im,(x,y)); dr.text((x+4,y+4),f'{t:.1f}',fill='yellow',font=font,stroke_width=2,stroke_fill='black')
out=sys.argv[5] if len(sys.argv)>5 else os.path.splitext(f)[0]+'_sheet.jpg'; page.save(out,quality=80); print(out,len(ims))
