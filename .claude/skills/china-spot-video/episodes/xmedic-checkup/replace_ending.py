# Replace everything after the last "<word>" in a narration with a new ending in the same cloned voice.
# usage: replace_ending.py <workdir> <word> "<context sentence>" "<new ending phrase>"   (keeps vo_preend.wav / words_preend.json)
import sys,os,json,re,subprocess,shutil,numpy as np
sys.path.insert(0,'/home/user/real-or-hype/.claude/skills/china-spot-video/scripts'); from eleven import tts
W,word,ctx,phrase=sys.argv[1:5]; os.chdir(W); SR=48000
SET={"stability":0.35,"similarity_boost":0.85,"style":0.45,"use_speaker_boost":True}; VID='KdPzirZUC0HY6WhfwyeE'
if not os.path.exists('vo_preend.wav'): shutil.copy('vo.wav','vo_preend.wav'); shutil.copy('words.json','words_preend.json')
from faster_whisper import WhisperModel
m=WhisperModel('medium',device='cpu',compute_type='int8'); n=lambda w: re.sub(r'[^a-z0-9]','',w.lower())
def pcm(f,sr=SR): return np.frombuffer(subprocess.run(['ffmpeg','-loglevel','error','-i',f,'-ac','1','-ar',str(sr),'-f','f32le','-'],capture_output=True,check=True).stdout,np.float32).copy()
def words(f): return [(w.start,w.end,w.word.strip()) for s in m.transcribe(pcm(f,16000),language='en',beam_size=5,word_timestamps=True)[0] for w in s.words]
ws=json.load(open('words_preend.json')); vo=pcm('vo_preend.wav')
k=max(i for i,w in enumerate(ws) if n(w[2]).startswith(n(word)))
if k+1<len(ws) and ws[k+1][2].startswith('-'): k+=1      # "check" "-up"
target=[n(x) for x in phrase.split()]; best=None
for t in range(1,4):
    mp=f'/tmp/claude-0/end_{t}.mp3'; tts(VID,ctx,mp,SET); wv=f'/tmp/claude-0/end_{t}.wav'
    sq='silenceremove=start_periods=1:start_threshold=-50dB,areverse,silenceremove=start_periods=1:start_threshold=-50dB,areverse,silenceremove=stop_periods=-1:stop_duration=0.2:stop_threshold=-42dB:stop_silence=0.14,atempo=1.25,loudnorm=I=-16:TP=-1.5:LRA=11'
    subprocess.run(['ffmpeg','-loglevel','error','-y','-i',mp,'-af',sq,'-ar',str(SR),'-ac','1',wv],check=True)
    h=words(wv); hn=[n(x[2]) for x in h]; print('take',t,' '.join(x[2] for x in h))
    for j in range(len(hn)-len(target)+1):
        if hn[j:j+len(target)]==target: best=(wv,h[j:j+len(target)]); break
    if best: break
if not best: raise SystemExit('new ending never heard correctly')
wv,pw=best; a=pcm(wv); s0=max(0,pw[0][0]-0.04); s1=min(len(a)/SR,pw[-1][1]+0.15)
seg=a[int(s0*SR):int(s1*SR)].copy(); f=int(0.01*SR); seg[:f]*=np.linspace(0,1,f); seg[-f:]*=np.linspace(1,0,f)
cut=ws[k][1]+0.06; head=vo[:int(cut*SR)].copy(); head[-f:]*=np.linspace(1,0,f); gap=np.zeros(int(0.12*SR),np.float32)
subprocess.run(['ffmpeg','-loglevel','error','-y','-f','f32le','-ar',str(SR),'-ac','1','-i','-','vo.wav'],input=np.concatenate([head,gap,seg]).tobytes(),check=True)
st=cut+0.12; J=ws[:k+1]+[[round(st+(x-s0),3),round(st+(y-s0),3),tk] for x,y,tk in pw]
json.dump(J,open('words.json','w')); print('new ending:',' '.join(x[2] for x in pw),'| total',round(st+s1-s0,2),'s')
