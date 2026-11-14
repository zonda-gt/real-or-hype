import sys,os,glob,subprocess,json
from PIL import Image,ImageDraw,ImageFont
src,out,step,TW,per=sys.argv[1],sys.argv[2],float(sys.argv[3]),int(sys.argv[4]),int(sys.argv[5])
os.makedirs(out,exist_ok=True)
font=ImageFont.truetype(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','fonts','Montserrat-ExtraBold.ttf'),14)
files=sorted(glob.glob(src+'/*.mp4')) if os.path.isdir(src) else [src]
COLS=12
rows_all=[]
for f in files:
    d=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f],capture_output=True,text=True).stdout)
    import tempfile; tmp=tempfile.mkdtemp(); os.makedirs(tmp,exist_ok=True)
    for x in glob.glob(tmp+'/*'): os.remove(x)
    subprocess.run(['ffmpeg','-loglevel','error','-i',f,'-vf',f'fps=1/{step},scale={TW}:-2','-q:v','4',tmp+'/%04d.jpg'])
    fr=sorted(glob.glob(tmp+'/*.jpg'))
    ims=[Image.open(x).convert('RGB') for x in fr]
    if not ims: continue
    H=max(i.height for i in ims)
    nrow=(len(ims)+COLS-1)//COLS
    blk=Image.new('RGB',(TW*COLS,22+nrow*(H+16)),(30,30,30)); dr=ImageDraw.Draw(blk)
    dr.text((4,3),f'{os.path.basename(f)[:-4]}  {d:.0f}s',fill='yellow',font=font)
    for k,im in enumerate(ims):
        x=(k%COLS)*TW; y=22+(k//COLS)*(H+16); blk.paste(im,(x,y)); dr.text((x+3,y+H),f'{k*step:.0f}',fill='white',font=font)
    rows_all.append(blk)
sheet=[];n=0
for i in range(0,len(rows_all),per):
    grp=rows_all[i:i+per]; W=max(g.width for g in grp); Ht=sum(g.height for g in grp)
    s=Image.new('RGB',(W,Ht)); y=0
    for g in grp: s.paste(g,(0,y)); y+=g.height
    n+=1; s.save(f'{out}/sheet{n:02d}.jpg',quality=80)
print(n)
