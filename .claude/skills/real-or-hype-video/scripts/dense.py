import os,sys,glob,subprocess,json,io
from PIL import Image,ImageDraw,ImageFont
os.chdir(sys.argv[1]); font=ImageFont.load_default(size=18); TW=170; COLS=7; STEP=2.0
def dur(f): return float(json.loads(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','json',f],capture_output=True,text=True).stdout)['format']['duration'])
rows=[]
for f in sorted(glob.glob('prev/*.mp4')):
    d=dur(f)
    if d<20: continue
    name=os.path.basename(f)[:-4].replace('VID_20260910_','')
    tmp='dense/_'+name; os.makedirs(tmp,exist_ok=True)
    subprocess.run(['ffmpeg','-loglevel','error','-y','-i',f,'-vf',f'fps=1/{STEP},scale={TW}:-2',f'{tmp}/%04d.jpg'])
    fr=sorted(glob.glob(tmp+'/*.jpg'))
    for k in range(0,len(fr),COLS):
        rows.append((name,k,fr[k:k+COLS]))
# pages of 5 rows
pg=0
for p in range(0,len(rows),5):
    chunk=rows[p:p+5]; h=Image.open(chunk[0][2][0]).height
    page=Image.new('RGB',(TW*COLS,(h+22)*len(chunk)),'black'); d=ImageDraw.Draw(page)
    for r,(name,k,fr) in enumerate(chunk):
        y=r*(h+22); d.text((3,y+1),name,fill='yellow',font=font)
        for c,x in enumerate(fr):
            page.paste(Image.open(x),(c*TW,y+22)); d.text((c*TW+3,y+22+h-20),f'{(k+c)*STEP+1:.0f}s',fill='white',font=font)
    pg+=1; page.save(f'dense/d{pg:02d}.jpg',quality=80)
print(len(rows),pg)
