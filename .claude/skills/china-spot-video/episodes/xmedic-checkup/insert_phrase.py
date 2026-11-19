# Add a new narration phrase (same cloned voice) after a given word in an existing narration.
# usage: insert_phrase.py <wav> <words.json> <after_word> "<context sentence ending with the new phrase>" "<new phrase>" [takes=3]
# The context sentence is synthesised so the prosody fits; only the new phrase is cut out (Whisper word times) and inserted.
# Backs up <wav>.bak / <words.json>.bak once. Processing matches vo_take.py: squeeze pauses, atempo 1.25, loudnorm -16.
import sys,os,json,re,subprocess,shutil,numpy as np
sys.path.insert(0,'/home/user/real-or-hype/.claude/skills/china-spot-video/scripts'); from eleven import tts
WAV,WJ,after,ctx,phrase=sys.argv[1:6]; N=int(sys.argv[6]) if len(sys.argv)>6 else 3
SET={"stability":0.35,"similarity_boost":0.85,"style":0.45,"use_speaker_boost":True}; VID='KdPzirZUC0HY6WhfwyeE'; SR=48000
for f in (WAV,WJ):
    if not os.path.exists(f+'.bak'): shutil.copy(f,f+'.bak')
from faster_whisper import WhisperModel
m=WhisperModel('medium',device='cpu',compute_type='int8')
n=lambda w: re.sub(r'[^a-z0-9]','',w.lower())
def pcm(f,sr=SR): return np.frombuffer(subprocess.run(['ffmpeg','-loglevel','error','-i',f,'-ac','1','-ar',str(sr),'-f','f32le','-'],capture_output=True,check=True).stdout,np.float32).copy()
def words(f): return [(w.start,w.end,w.word.strip()) for s in m.transcribe(pcm(f,16000),language='en',beam_size=5,word_timestamps=True,initial_prompt='ECG, CT scan')[0] for w in s.words]
target=[n(x) for x in phrase.split()]; best=None
for t in range(1,N+1):
    mp=f'/tmp/claude-0/ins_{t}.mp3'; tts(VID,ctx,mp,SET)
    sq='silenceremove=start_periods=1:start_threshold=-50dB,areverse,silenceremove=start_periods=1:start_threshold=-50dB,areverse,silenceremove=stop_periods=-1:stop_duration=0.2:stop_threshold=-42dB:stop_silence=0.14,atempo=1.25,loudnorm=I=-16:TP=-1.5:LRA=11'
    wv=f'/tmp/claude-0/ins_{t}.wav'; subprocess.run(['ffmpeg','-loglevel','error','-y','-i',mp,'-af',sq,'-ar',str(SR),'-ac','1',wv],check=True)
    ws=words(wv); hn=[n(w[2]) for w in ws]; print('take',t,' '.join(w[2] for w in ws))
    for k in range(len(hn)-len(target)+1):
        if hn[k:k+len(target)]==target:
            seg=(ws[k][0],ws[k+len(target)-1][1],ws[k:k+len(target)]); best=(wv,seg); break
    if best: break
if not best: raise SystemExit('new phrase never heard correctly; rephrase')
wv,(s0,s1,pw)=best; a=pcm(wv); s0=max(0,s0-0.04); s1=s1+0.06
seg=a[int(s0*SR):int(s1*SR)].copy(); f=int(0.01*SR); seg[:f]*=np.linspace(0,1,f); seg[-f:]*=np.linspace(1,0,f)
vo=pcm(WAV+'.bak'); W=json.load(open(WJ+'.bak'))
k=next(i for i,w in enumerate(W) if n(w[2])==n(after)); cut=min(W[k][1]+0.10,(W[k][1]+W[k+1][0])/2)
gap=np.zeros(int(0.10*SR),np.float32); c=int(cut*SR); ins=len(gap)/SR+len(seg)/SR
out=np.concatenate([vo[:c],gap,seg,vo[c:]])
subprocess.run(['ffmpeg','-loglevel','error','-y','-f','f32le','-ar',str(SR),'-ac','1','-i','-',WAV],input=out.tobytes(),check=True)
new=[[round(cut+0.10+(x-s0),3),round(cut+0.10+(y-s0),3),t] for x,y,t in pw]
J=[w for w in W if w[0]<cut]+new+[[round(x+ins,3),round(y+ins,3),t] for x,y,t in W if x>=cut]
json.dump(J,open(WJ,'w')); print('inserted',' '.join(w[2] for w in pw),'at',round(cut,2),'s, +',round(ins,2),'s')
