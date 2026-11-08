"""Still boards with per-frame stats for each shortlisted window. usage: board2.py shortlist.json outdir"""
import sys,json,subprocess,numpy as np,cv2,os
from PIL import Image,ImageDraw,ImageFont
SL=json.load(open(sys.argv[1])); od=sys.argv[2]; os.makedirs(od,exist_ok=True)
F=ImageFont.truetype('/home/user/real-or-hype/.claude/skills/real-or-hype-video/scripts/Montserrat-ExtraBold.ttf',22)
FC=ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',26)
def stats(cid,a,b):
    s=json.load(open(f'score/{cid}.json')); fps=s['fps']; R=np.array(s['rows'][int(a*fps):int(b*fps)])
    sharp=np.median(R[:,0]); bright=np.median(R[:,1]); clip=np.median(R[:,2])
    m=np.hypot(R[:,3],R[:,4]); k=np.convolve(m,np.ones(9)/9,'same'); jit=float(np.std(m-k))
    cuts=int((R[1:,5]>0.35).sum())
    return sharp,bright,clip,jit,cuts
summary=[]
for hi,(hotel,wins) in enumerate(SL.items()):
    rows=[]
    for cid,a,b,lab in wins:
        ims=[]
        for t in (a+0.1,(a+b)/2,b-0.1):
            raw=subprocess.run(['ffmpeg','-v','error','-ss',str(t),'-i',f'clips/{cid}.mp4','-frames:v','1','-vf','scale=-2:300','-f','image2pipe','-vcodec','png','-'],capture_output=True).stdout
            ims.append(Image.open(__import__('io').BytesIO(raw)).convert('RGB'))
        sh,br,cl,ji,cu=stats(cid,a,b)
        flag=[]
        if sh<60: flag.append('SOFT')
        if br<55: flag.append('DARK')
        if br>200 or cl>8: flag.append('BLOWN')
        if ji>1.2: flag.append('SHAKY')
        if cu: flag.append(f'{cu} CUT')
        txt=f"{chr(65+len(rows))}. {lab}  [{cid[-6:]} {a:.1f}-{b:.1f}s]  sharp {sh:.0f}  bright {br:.0f}  jitter {ji:.2f}  {' '.join(flag) or 'OK'}"
        summary.append((hotel.split()[0],chr(65+len(rows)),cid,a,b,lab,round(sh),round(br),round(ji,2),flag))
        rows.append((ims,txt))
    W=max(sum(i.width for i in r[0])+40 for r in rows); H=sum(340 for r in rows)+60
    bd=Image.new('RGB',(max(W,900),H),'white'); d=ImageDraw.Draw(bd); d.text((10,10),hotel,font=FC,fill='black'); y=55
    for ims,txt in rows:
        d.text((10,y),txt,font=F,fill='black'); x=10
        for im in ims: bd.paste(im,(x,y+30)); x+=im.width+10
        y+=340
    bd.save(f'{od}/board_{hotel.split()[0]}.jpg',quality=85)
json.dump(summary,open(f'{od}/summary.json','w'),ensure_ascii=False,indent=0)
for s in summary: print(s)
