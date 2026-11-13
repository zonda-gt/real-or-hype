import sys,os,glob,subprocess,io,json
from PIL import Image,ImageDraw,ImageFont
# usage: sheet1.py rawdir outdir fps  -> one sheet per video
rd,od,fps=sys.argv[1],sys.argv[2],float(sys.argv[3]); os.makedirs(od,exist_ok=True)
font=ImageFont.load_default(size=22); TW,TH=160,284; C=12
for f in sorted(glob.glob(f'{rd}/*.mp4')):
    name=os.path.basename(f)[:-4]; out=f'{od}/{name}.jpg'
    if os.path.exists(out): continue
    tmp=f'{od}/_t'; os.makedirs(tmp,exist_ok=True)
    for x in glob.glob(tmp+'/*'): os.remove(x)
    subprocess.run(['ffmpeg','-loglevel','error','-i',f,'-vf',f'fps={fps},scale={TW}:{TH}:force_original_aspect_ratio=decrease,pad={TW}:{TH}:(ow-iw)/2:(oh-ih)/2',f'{tmp}/%04d.jpg'])
    fr=sorted(glob.glob(tmp+'/*.jpg'))
    if not fr: print('nofr',name); continue
    R=(len(fr)+C-1)//C
    sh=Image.new('RGB',(TW*C,TH*R+30),'black'); d=ImageDraw.Draw(sh)
    d.text((4,2),name,fill='yellow',font=font)
    for j,p in enumerate(fr):
        x,y=(j%C)*TW,30+(j//C)*TH; sh.paste(Image.open(p),(x,y))
        d.rectangle([x,y,x+44,y+22],fill='black'); d.text((x+2,y),f'{j/fps:.0f}' if fps<=1 else f'{j/fps:.1f}',fill='yellow',font=font)
    sh.save(out,quality=78)
print('done')
