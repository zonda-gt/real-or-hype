# per-segment word timing: Whisper each cut segment on its own, map onto the script words by position (falls back to
# character-proportional timing inside the segment's voiced span when counts differ)
import sys,json,subprocess,numpy as np,re
from faster_whisper import WhisperModel
E=sys.argv[1]; m=WhisperModel("medium",device="cpu",compute_type="int8")
out=[]
for s in json.load(open(f'{E}/timeline.json')):
    a=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',f'{E}/seg/{s["k"]}.wav','-ac','1','-ar','16000','-f','f32le','-'],capture_output=True).stdout,np.float32)
    ws=[(w.start,w.end) for g in m.transcribe(a,language='en',beam_size=5,word_timestamps=True)[0] for w in g.words if re.sub(r'\W','',w.word)]
    tw=s['text'].split()
    if len(ws)!=len(tw):
        s0,s1=(ws[0][0],ws[-1][1]) if ws else (0.05,s['dur']-0.1); L=sum(len(w) for w in tw); acc=0; ws=[]
        for w in tw: a0=s0+(s1-s0)*acc/L; acc+=len(w); ws.append((a0,s0+(s1-s0)*acc/L))
        print('proportional timing for',s['k'])
    out+= [[round(s['start']+a,3),round(s['start']+b,3),w] for (a,b),w in zip(ws,tw)]
json.dump(out,open(f'{E}/words.json','w')); print(len(out)); print(' '.join(f'{i}:{w[2]}@{w[0]:.2f}' for i,w in enumerate(out)))
