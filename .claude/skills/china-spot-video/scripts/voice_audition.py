# Audition voices on the same lines so the creator can pick by ear.
# usage: voice_audition.py <lines.txt> <outdir> <target_seconds|0> Name:voice_id [Name:voice_id ...]
# Per voice: TTS (lively preset) -> trim edges, squeeze pauses -> speed up to target length (never slow down)
# -> Whisper check -> one loudness-matched reel <outdir>/audition.mp3 in the given order.  EARSHOT=<python of earshot venv> adds a liveliness rank.
import sys,os,subprocess,re,numpy as np
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); from eleven import tts
lines,out,target=sys.argv[1],sys.argv[2],float(sys.argv[3]); voices=[a.split(':',1) for a in sys.argv[4:]]
os.makedirs(out,exist_ok=True); text=open(lines).read().strip()
def dur(f): return float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f],capture_output=True,text=True).stdout)
fit=[]
for n,vid in voices:
    raw=f'{out}/{n}_raw.mp3'
    if not os.path.exists(raw) and not tts(vid,text,raw): continue
    tmp=f'{out}/_{n}.wav'
    subprocess.run(['ffmpeg','-loglevel','error','-y','-i',raw,'-af','silenceremove=start_periods=1:start_threshold=-50dB,areverse,silenceremove=start_periods=1:start_threshold=-50dB,areverse,silenceremove=stop_periods=-1:stop_duration=0.25:stop_threshold=-45dB:stop_silence=0.18',tmp],check=True)
    sp=max(1.0,dur(tmp)/target) if target>0 else 1.0
    subprocess.run(['ffmpeg','-loglevel','error','-y','-i',tmp,'-af',f'atempo={sp:.3f},loudnorm=I=-16:TP=-1.5','-ar','44100','-b:a','160k',f'{out}/{n}.mp3'],check=True); os.remove(tmp)
    fit.append((n,sp))
from faster_whisper import WhisperModel
m=WhisperModel("small",device="cpu",compute_type="int8")
ref=re.sub(r"[^a-z0-9 ]","",text.lower().replace('-',' ')).split()
NUM={'a','one','two','three','four','five','six','seven','eight','nine','ten','twenty','thirty','forty','fifty','hundred','thousand','fourteen','dollars','okay'}
for n,sp in fit:
    a=np.frombuffer(subprocess.run(['ffmpeg','-loglevel','error','-i',f'{out}/{n}.mp3','-ac','1','-ar','16000','-f','f32le','-'],capture_output=True).stdout,dtype=np.float32)
    h=re.sub(r"[^a-z0-9 ]","",' '.join(s.text for s in m.transcribe(a,language='en',beam_size=5)[0]).lower().replace('-',' ')).split()
    miss=[w for w in ref if w not in h and w not in NUM]
    print(f'{n:16s} speed x{sp:.2f}  {"OK" if not miss else "check: "+" ".join(miss)}')
E=os.environ.get('EARSHOT')
if E: print(subprocess.run([E,'-m','earshot','rank','a lively, energetic, enthusiastic narrator for a fun travel video']+[f'{out}/{n}.mp3' for n,_ in fit],capture_output=True,text=True).stdout)
L=sum([['-i',f'{out}/{n}.mp3'] for n,_ in fit],[]); k=len(fit)
fc=''.join(f'[{i}:a]aresample=44100,aformat=channel_layouts=mono,apad=pad_dur=1.0[a{i}];' for i in range(k))+''.join(f'[a{i}]' for i in range(k))+f'concat=n={k}:v=0:a=1'
subprocess.run(['ffmpeg','-loglevel','error','-y']+L+['-filter_complex',fc,'-b:a','160k',f'{out}/audition.mp3'],check=True)
print('reel:',f'{out}/audition.mp3','order:',' -> '.join(n for n,_ in fit))
