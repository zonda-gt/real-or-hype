# One continuous Kokoro take (ElevenLabs out of credits), Whisper-checked, gaps tidied. Same outputs as vo_take.py.
# usage: vo_kokoro.py <workdir> <voice> [target_wpm=180] [max_gap=0.45]
import sys,os,subprocess,re,json,numpy as np,soundfile as sf
from kokoro_onnx import Kokoro
W,voice=sys.argv[1],sys.argv[2]; WPM=float(sys.argv[3]) if len(sys.argv)>3 else 180; MAXG=float(sys.argv[4]) if len(sys.argv)>4 else 0.45
os.chdir(W); text=open('script.txt').read().strip()
k=Kokoro('/home/user/real-or-hype/work/tts/kokoro-v1.0.onnx','/home/user/real-or-hype/work/tts/voices-v1.0.bin')
from faster_whisper import WhisperModel
m=WhisperModel("medium",device="cpu",compute_type="int8")
def pcm(f,sr): return np.frombuffer(subprocess.run(['ffmpeg','-loglevel','error','-i',f,'-ac','1','-ar',str(sr),'-f','f32le','-'],capture_output=True).stdout,dtype=np.float32)
def words(f): return [(round(w.start,3),round(w.end,3),w.word.strip()) for s in list(m.transcribe(pcm(f,16000),language='en',beam_size=5,word_timestamps=True)[0]) for w in s.words]
norm=lambda s: re.sub(r"[^a-z0-9 ]","",s.lower().replace('-',' ').replace(':',' ')).split()
ref=norm(text)
s,sr=k.create(text,voice=voice,speed=1.0,lang='en-us'); sf.write('take_raw.wav',s,sr)
ws=words('take_raw.wav'); wpm=len(ws)/(ws[-1][1]-ws[0][0])*60; sp=WPM/wpm
s,sr=k.create(text,voice=voice,speed=sp,lang='en-us'); sf.write('take.wav',s,sr)
SR=44100; subprocess.run(['ffmpeg','-loglevel','error','-y','-i','take.wav','-ar',str(SR),'-ac','1','take44.wav'],check=True)
a=pcm('take44.wav',SR); ws=words('take44.wav')
# trim lead/tail, shrink gaps > MAXG to MAXG
keep=[]; cur=max(0,ws[0][0]-0.05)
for i in range(len(ws)-1):
    g0,g1=ws[i][1],ws[i+1][0]
    if g1-g0>MAXG+0.05: mid=(g0+g1)/2; c=(g1-g0)-MAXG; keep.append((cur,mid-c/2)); cur=mid+c/2
keep.append((cur,min(len(a)/SR,ws[-1][1]+0.25))); f=int(0.01*SR); parts=[]
for s0,e in keep:
    seg=a[int(s0*SR):int(e*SR)].copy()
    if len(seg)>2*f: seg[:f]*=np.linspace(0,1,f); seg[-f:]*=np.linspace(1,0,f)
    parts.append(seg)
subprocess.run(['ffmpeg','-loglevel','error','-y','-f','f32le','-ar',str(SR),'-ac','1','-i','-','-af','loudnorm=I=-16:TP=-1.5:LRA=11','-ar','48000','vo.wav'],input=np.concatenate(parts).tobytes(),check=True)
ws=words('vo.wav'); json.dump(ws,open('words.json','w'))
h=norm(' '.join(w[2] for w in ws)); NUM={'one','two','three','sixth','tenth','sixteenth','eleven','nine','december'}
fm=[w for w in ref if w not in h and w not in NUM]
print(f'speed x{sp:.2f}; FINAL check:', 'word-perfect' if not fm else f'MISHEARD {fm}')
print(f'vo.wav {ws[-1][1]:.1f}s, {len(ws)/ws[-1][1]*60:.0f} wpm\n'+' '.join(f'{i}:{w[2]}@{w[0]:.2f}' for i,w in enumerate(ws)))
