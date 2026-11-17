# Cut his read into narration lines (jump-cut pieces in silence), light clean-up, 1.1x, check boundaries + Whisper.
import json,subprocess,numpy as np,re
from faster_whisper import WhisperModel
SEG={
 'r_hook':   ([(15.86,19.95)], "So Honor made a phone with a robot camera, and of course I had to try it."),
 'r_brand':  ([(20.33,21.10),(21.75,25.26)], "If you don't know Honor, it's one of China's biggest phone brands."),
 'r_pops':   ([(33.92,38.10)], "The camera pops out on a tiny robot arm, and it moves on its own."),
 'r_looks':  ([(38.30,39.58),(39.95,41.30)], "It's literally looking at me. Who even thought of this?"),
 'r_called': ([(42.35,44.38)], "It's called the Honor Robot Phone."),
 'r_price':  ([(50.32,52.58),(56.98,59.05)], "It's about $1,400. Honestly, I have to get one."),
 'r_crazy':  ([(62.35,65.30)], "Guys, this is not even the craziest thing in here."),
 'r_tele':   ([(65.32,73.52)], "They have a telescope lens for your phone. You clip it on and you can zoom across the whole building. Like, I can see people on the other side of the mall."),
 'r_tele2':  ([(65.32,70.35)], "They have a telescope lens for your phone. You clip it on and you can zoom across the whole building."),
 'r_cat':    ([(75.68,80.78),(82.38,84.86)], "And this is the cat massage gun. It literally punches you in the face with its little paws. It feels kind of nice. I don't hate it."),
 'r_three':  ([(85.84,89.85)], "These are the three craziest things I found in the phone store in China."),
 'r_ask':    ([(93.00,95.55),(97.90,100.15)], "Guys, would you buy a phone with the robot camera or not? Let me know, I'm curious to see."),
}
SR=48000
a=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i','rec/read.wav','-ac','1','-ar',str(SR),'-f','f32le','-'],capture_output=True).stdout,np.float32)
def db(x): return 20*np.log10(np.sqrt(np.mean(x**2))+1e-9)
h=int(0.05*SR); fl=np.percentile([db(a[i:i+h]) for i in range(0,len(a)-h,h)],10)
m=WhisperModel("medium",compute_type="int8"); bad=[]
L=json.load(open('lines.json'))
for k,(parts,text) in SEG.items():
    for s,e in parts:   # 0.1 s at each edge must be near the floor
        for nm,w in (('in',a[int(s*SR):int((s+0.08)*SR)]),('out',a[int((e-0.1)*SR):int(e*SR)])):
            if db(w)>fl+10: bad.append(f'{k} {nm}@{s if nm=="in" else e}: {db(w)-fl:.1f} dB over floor')
    fc=''.join(f"[0:a]atrim={s}:{e},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st={e-s-0.03:.3f}:d=0.03[p{i}];" for i,(s,e) in enumerate(parts))
    fc+=''.join(f'[p{i}]' for i in range(len(parts)))+f"concat=n={len(parts)}:v=0:a=1,highpass=f=80,afftdn=nf=-45,atempo=1.1[o]"
    subprocess.run(['ffmpeg','-v','error','-y','-i','rec/read.wav','-filter_complex',fc,'-map','[o]','-ar','48000','-ac','1',f'vo/{k}.wav'],check=True)
    x=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',f'vo/{k}.wav','-ac','1','-ar','16000','-f','f32le','-'],capture_output=True).stdout,np.float32)
    hyp=' '.join(s.text.strip() for s in m.transcribe(x,language='en')[0])
    print(f'{k:9s} {len(x)/16000:5.2f}s | {hyp}')
    L[k]=text
json.dump(L,open('lines.json','w'),indent=1)
print('BOUNDARY ISSUES:',bad or 'none')
