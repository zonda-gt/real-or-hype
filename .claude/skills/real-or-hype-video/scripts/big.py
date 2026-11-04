import os,sys,subprocess,io
from PIL import Image,ImageDraw,ImageFont
os.chdir(sys.argv[1]); out=sys.argv[2]; TW=int(sys.argv[3]); COLS=int(sys.argv[4]); font=ImageFont.load_default(size=20); tiles=[]
for sp in sys.argv[5:]:
    n,a,b,st=sp.split(':'); a,b,st=float(a),float(b),float(st); t=a
    src='orig/'+n+'.MOV' if os.path.exists('orig/'+n+'.MOV') else ('orig/'+n+'.mp4' if os.path.exists('orig/'+n+'.mp4') else 'prev/'+n+'.mp4')
    while t<=b+1e-6:
        r=subprocess.run(['ffmpeg','-loglevel','error','-ss',f'{t:.2f}','-i',src,'-frames:v','1','-vf',f'scale={TW}:-2','-f','image2pipe','-vcodec','png','-'],capture_output=True)
        if r.stdout:
            im=Image.open(io.BytesIO(r.stdout)).convert('RGB'); ImageDraw.Draw(im).text((4,4),f"{n.replace('VID_20260910_','')} {t:.1f}",fill='yellow',font=font,stroke_width=2,stroke_fill='black'); tiles.append(im)
        t+=st
h=max(i.height for i in tiles); rows=(len(tiles)+COLS-1)//COLS; pg=Image.new('RGB',(TW*COLS,h*rows),'black')
for i,im in enumerate(tiles): pg.paste(im,((i%COLS)*TW,(i//COLS)*h))
pg.save(out,quality=85); print(len(tiles))
