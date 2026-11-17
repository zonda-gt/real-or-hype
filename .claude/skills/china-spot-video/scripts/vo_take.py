# One continuous narration take, chosen by Whisper, tightened to reference pace.
# usage: vo_take.py <workdir> <voice_id> [takes=3] [target_wpm=200]
# Reads <workdir>/script.txt. Writes take*.mp3, vo.wav (loudnorm -16) and words.json [(start,end,word),...], then prints
# every word with its index: those indices are the cue points in plan.py.
import sys,os,subprocess,re,json,numpy as np
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); from eleven import tts
W,vid=sys.argv[1],sys.argv[2]; N=int(sys.argv[3]) if len(sys.argv)>3 else 3; WPM=float(sys.argv[4]) if len(sys.argv)>4 else 200
os.chdir(W); text=open('script.txt').read().strip()
from faster_whisper import WhisperModel
m=WhisperModel("medium",device="cpu",compute_type="int8")
def pcm(f,sr): return np.frombuffer(subprocess.run(['ffmpeg','-loglevel','error','-i',f,'-ac','1','-ar',str(sr),'-f','f32le','-'],capture_output=True).stdout,dtype=np.float32)
def words(f): return [(round(w.start,3),round(w.end,3),w.word.strip()) for s in m.transcribe(pcm(f,16000),language='en',beam_size=5,word_timestamps=True)[0] for w in s.words]
ref=re.sub(r"[^a-z0-9 ]","",text.lower().replace('-',' ')).split()
NUM={'a','one','two','three','four','five','six','seven','eight','nine','ten','twenty','thirty','forty','fifty','hundred','thousand','fourteen','dollars'}
res=[]
for t in range(1,N+1):
    if not os.path.exists(f'take{t}.mp3'): tts(vid,text,f'take{t}.mp3')
    sq='silenceremove=start_periods=1:start_threshold=-50dB,areverse,silenceremove=start_periods=1:start_threshold=-50dB,areverse,silenceremove=stop_periods=-1:stop_duration=0.2:stop_threshold=-42dB:stop_silence=0.14'
    subprocess.run(['ffmpeg','-loglevel','error','-y','-i',f'take{t}.mp3','-af',sq,'-ar','44100','-ac','1',f'take{t}_sq.wav'],check=True)
    ws=words(f'take{t}_sq.wav'); wpm=len(ws)/(ws[-1][1]-ws[0][0])*60; sp=min(1.25,max(1.0,WPM/wpm))
    subprocess.run(['ffmpeg','-loglevel','error','-y','-i',f'take{t}_sq.wav','-af',f'atempo={sp:.3f}',f'take{t}_fast.wav'],check=True)
    h=re.sub(r"[^a-z0-9 ]","",' '.join(w[2] for w in words(f'take{t}_fast.wav')).lower().replace('-',' ')).split()
    miss=[w for w in ref if w not in h and w not in NUM]
    res.append((len(miss),t,miss,sp)); print(f'take{t}: speed x{sp:.2f}, missing {miss}')
res.sort(); _,best,miss,sp=res[0]; print('using take',best, '(WARNING: still missing '+str(miss)+')' if miss else '')
SR=44100; a=pcm(f'take{best}_fast.wav',SR); ws=words(f'take{best}_fast.wav')
keep=[]; cur=0.0
for i in range(len(ws)-1):   # shrink any gap > 0.35 s to 0.30 s
    g0,g1=ws[i][1],ws[i+1][0]
    if g1-g0>0.35: mid=(g0+g1)/2; c=(g1-g0)-0.30; keep.append((cur,mid-c/2)); cur=mid+c/2
keep.append((cur,len(a)/SR)); f=int(0.01*SR); parts=[]
for s,e in keep:
    seg=a[int(s*SR):int(e*SR)].copy()
    if len(seg)>2*f: seg[:f]*=np.linspace(0,1,f); seg[-f:]*=np.linspace(1,0,f)
    parts.append(seg)
subprocess.run(['ffmpeg','-loglevel','error','-y','-f','f32le','-ar',str(SR),'-ac','1','-i','-','-af','loudnorm=I=-16:TP=-1.5:LRA=11','-ar','48000','vo.wav'],input=np.concatenate(parts).tobytes(),check=True)
ws=words('vo.wav'); json.dump(ws,open('words.json','w'))
h=re.sub(r"[^a-z0-9 ]","",' '.join(w[2] for w in ws).lower().replace('-',' ')).split()
fm=[w for w in ref if w not in h and w not in NUM]
print('FINAL vo.wav check:', 'word-perfect' if not fm else f'MISHEARD {fm}: rephrase (a leading word helps, e.g. "Outside, capybaras...") and re-run with new takes, or add CAPTION_FIX')
print(f'vo.wav {ws[-1][1]:.1f}s, {len(ws)/ws[-1][1]*60:.0f} wpm\n'+' '.join(f'{i}:{w[2]}@{w[0]:.2f}' for i,w in enumerate(ws)))
