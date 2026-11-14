import sys,os,glob,subprocess,json,io
from PIL import Image,ImageDraw,ImageFont
W=sys.argv[1]; os.chdir(W); os.makedirs('cat',exist_ok=True)
font=ImageFont.truetype(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','fonts','Montserrat-ExtraBold.ttf'),15)
def dur(f): return float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f],capture_output=True,text=True).stdout)
def frame(f,t,w):
    r=subprocess.run(['ffmpeg','-loglevel','error','-ss',f'{t:.2f}','-i',f,'-frames:v','1','-vf',f'scale={w}:-2','-f','image2pipe','-vcodec','png','-'],capture_output=True)
    return Image.open(io.BytesIO(r.stdout)).convert('RGB')
allshots={}
for f in sorted(glob.glob('src/*.mp4')):
    n=os.path.basename(f)[:-4]; d=dur(f)
    r=subprocess.run(['ffmpeg','-hide_banner','-i',f,'-vf',"select='gt(scene,0.3)',showinfo",'-an','-f','null','-'],capture_output=True,text=True).stderr
    cuts=[float(x.split(':')[1]) for x in r.split() if x.startswith('pts_time:')]
    b=[0]+[c for c in cuts if c>0.3]+[d]
    shots=[(b[i],b[i+1]) for i in range(len(b)-1) if b[i+1]-b[i]>0.6]
    allshots[n]=shots
json.dump(allshots,open('shots.json','w'),indent=0)
TW=120
for n,shots in allshots.items():
    f=f'src/{n}.mp4'; tiles=[]
    for k,(a,b) in enumerate(shots):
        ts=[a+0.15, (a+b)/2, b-0.2] if b-a>1.5 else [(a+b)/2]
        tiles.append((k,a,b,[frame(f,t,TW) for t in ts]))
    H=tiles[0][3][0].height
    cols=9; # tiles of variable width -> pack into rows
    rows=[];cur=[];wcur=0
    for t in tiles:
        tw=TW*len(t[3])+6
        if wcur+tw>TW*9+60 and cur: rows.append(cur); cur=[]; wcur=0
        cur.append(t); wcur+=tw
    if cur: rows.append(cur)
    img=Image.new('RGB',(TW*9+60,24+len(rows)*(H+20)),(25,25,25)); dr=ImageDraw.Draw(img)
    dr.text((4,3),n,fill='yellow',font=font)
    for ri,row in enumerate(rows):
        x=0;y=24+ri*(H+20)
        for k,a,b,ims in row:
            for im in ims: img.paste(im,(x,y)); x+=TW
            dr.text((x-TW*len(ims)+3,y+H+1),f'#{k} {a:.1f}-{b:.1f}',fill='white',font=font); x+=6
    img.save(f'cat/{n}.jpg',quality=82)
print({k:len(v) for k,v in allshots.items()})
