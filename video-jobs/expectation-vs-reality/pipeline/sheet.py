#!/usr/bin/env python3
# sheet.py out.jpg id1 id2 ... : 8 frames per video in a row, labelled
import sys,os,subprocess,json
from PIL import Image,ImageDraw,ImageFont
S=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out=sys.argv[1]; ids=sys.argv[2:]; N=int(os.environ.get('N',8)); H=int(os.environ.get('H',200))
rows=[]
for i in ids:
    f=f'{S}/media/dy/{i}.mp4'
    if not os.path.exists(f): continue
    dur=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f],capture_output=True,text=True).stdout or 0)
    fr=[]
    for k in range(N):
        t=dur*(k+0.5)/N
        p=subprocess.run(['ffmpeg','-v','error','-ss',f'{t:.2f}','-i',f,'-frames:v','1','-vf',f'scale=-2:{H}','-f','image2pipe','-vcodec','png','-'],capture_output=True).stdout
        import io
        try: im=Image.open(io.BytesIO(p)).convert('RGB')
        except Exception: im=Image.new('RGB',(H*9//16,H))
        d=ImageDraw.Draw(im); d.text((3,H-14),f'{t:.1f}',fill=(255,255,0))
        fr.append(im)
    w=sum(x.width for x in fr)+260
    row=Image.new('RGB',(w,H),(30,30,30)); x=260
    for im in fr: row.paste(im,(x,0)); x+=im.width
    d=ImageDraw.Draw(row); d.text((4,4),i,fill=(255,255,255)); d.text((4,20),f'{dur:.1f}s',fill=(200,200,200))
    rows.append(row)
W=max(r.width for r in rows); sh=Image.new('RGB',(W,sum(r.height+4 for r in rows)),(0,0,0)); y=0
for r in rows: sh.paste(r,(0,y)); y+=r.height+4
sh.save(out,quality=80); print(out, sh.size)
