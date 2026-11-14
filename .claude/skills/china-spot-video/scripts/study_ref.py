# Study a reference reel: transcript, pace, pauses, cut rhythm, what is on screen while each word is said, voice pitch range.
# usage: study_ref.py <video.mp4>   -> prints stats + transcript, writes <video>_an.json and <video>_shots*.jpg
import sys,subprocess,json,io,numpy as np
from faster_whisper import WhisperModel
from PIL import Image,ImageDraw,ImageFont
f=sys.argv[1]; base=f.rsplit('.',1)[0]
m=WhisperModel("medium",device="cpu",compute_type="int8")
a=np.frombuffer(subprocess.run(['ffmpeg','-loglevel','error','-i',f,'-ar','16000','-ac','1','-f','f32le','-'],capture_output=True).stdout,dtype=np.float32)
segs=list(m.transcribe(a,language='en',word_timestamps=True,beam_size=5)[0])
words=[(w.start,w.end,w.word.strip()) for s in segs for w in s.words]; sents=[(s.start,s.end,s.text.strip()) for s in segs]
dur=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f],capture_output=True,text=True).stdout)
cuts=[float(x) for x in subprocess.run(f"ffmpeg -hide_banner -i '{f}' -vf \"select='gt(scene,0.22)',showinfo\" -an -f null - 2>&1 | grep -o 'pts_time:[0-9.]*' | cut -d: -f2",shell=True,capture_output=True,text=True).stdout.split()]
b=[0.0]+[x for x in cuts if x>0.15]+[dur]; shots=[(b[i],b[i+1]) for i in range(len(b)-1) if b[i+1]-b[i]>0.08]
out=[{'s':round(s,2),'e':round(e,2),'d':round(e-s,2),'words':' '.join(w for a0,a1,w in words if a0<e and a1>s)} for s,e in shots]
def f0(x):
    N=640; r_=[]
    for i in range(0,len(x)-N,320):
        y=x[i:i+N]-x[i:i+N].mean()
        if np.sqrt(np.mean(y**2))<0.02: continue
        r=np.correlate(y,y,'full')[N-1:]; lo,hi=16000//400,16000//65; k=lo+np.argmax(r[lo:hi])
        if r[k]>0.5*r[0]: r_.append(16000/k)
    return np.array(r_)
p=f0(a); gaps=[words[i+1][0]-words[i][1] for i in range(len(words)-1)]
spoken=sum(e-s for s,e,_ in sents)
print(f'dur {dur:.1f}s | words {len(words)} | {len(words)/spoken*60:.0f} wpm while speaking | gaps>0.25s: {sum(g>0.25 for g in gaps)} | shots {len(out)}, mean {dur/len(out):.2f}s, median {np.median([o["d"] for o in out]):.2f}s')
print(f'voice F0 median {np.median(p):.0f} Hz, pitch range (10-90%) {12*np.log2(np.percentile(p,90)/np.percentile(p,10)):.1f} semitones  (music under the voice inflates this a little)')
for s,e,t in sents: print(f'  [{s:5.1f}-{e:5.1f}] {t}')
json.dump({'sents':sents,'words':words,'shots':out,'dur':dur},open(base+'_an.json','w'),indent=1)
font=ImageFont.load_default(size=15); TW=180; rows=[]
for o in out:
    r=subprocess.run(['ffmpeg','-loglevel','error','-ss',f"{(o['s']+o['e'])/2:.2f}",'-i',f,'-frames:v','1','-vf',f'scale={TW}:-2','-f','image2pipe','-vcodec','png','-'],capture_output=True)
    rows.append((o,Image.open(io.BytesIO(r.stdout)).convert('RGB')))
C=8; H=rows[0][1].height+70
for pg in range(0,len(rows),32):
    ch=rows[pg:pg+32]; page=Image.new('RGB',(TW*C,H*((len(ch)+C-1)//C)),'black'); d=ImageDraw.Draw(page)
    for k,(o,im) in enumerate(ch):
        x,y=(k%C)*TW,(k//C)*H; page.paste(im,(x,y)); d.text((x+3,y+3),f"{o['s']:.1f}s ({o['d']:.1f})",fill='yellow',font=font,stroke_width=2,stroke_fill='black')
        for li,l in enumerate([o['words'][i:i+24] for i in range(0,min(len(o['words']),96),24)]): d.text((x+3,y+im.height+2+li*16),l,fill='white',font=font)
    page.save(f'{base}_shots{pg//32}.jpg',quality=82); print('sheet',f'{base}_shots{pg//32}.jpg')
