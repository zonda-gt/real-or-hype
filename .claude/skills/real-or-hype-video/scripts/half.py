import os,sys,glob,subprocess,io
from PIL import Image,ImageDraw,ImageFont
os.chdir(sys.argv[1]); font=ImageFont.load_default(size=15); TW=120; COLS=12
specs=sys.argv[3:]; out=sys.argv[2]; rows=[]
for sp in specs:
    n,a,b=sp.split(':'); a=float(a); b=float(b)
    f='prev/'+n+'.mp4'; tmp=f'half/_{n}'; os.makedirs(tmp,exist_ok=True)
    subprocess.run(['ffmpeg','-loglevel','error','-y','-ss',str(a),'-t',str(b-a),'-i',f,'-vf',f'fps=2,scale={TW}:-2',f'{tmp}/%04d.jpg'])
    fr=sorted(glob.glob(tmp+'/*.jpg'))
    for k in range(0,len(fr),COLS): rows.append((n.replace('VID_20260910_',''),a,k,fr[k:k+COLS]))
h=Image.open(rows[0][3][0]).height
pg=Image.new('RGB',(TW*COLS,(h+16)*len(rows)),'black'); d=ImageDraw.Draw(pg)
for r,(n,a,k,fr) in enumerate(rows):
    y=r*(h+16); d.text((2,y),n,fill='yellow',font=font)
    for c,x in enumerate(fr):
        pg.paste(Image.open(x),(c*TW,y+16)); d.text((c*TW+2,y+16+h-16),f'{a+(k+c)*0.5:.1f}',fill='white',font=font)
pg.save(out,quality=82); print(len(rows))
