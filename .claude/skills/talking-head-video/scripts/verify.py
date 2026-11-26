import sys,json,subprocess,numpy as np
from faster_whisper import WhisperModel
f,tlf,out=sys.argv[1:4]
m=WhisperModel("medium",device="cpu",compute_type="int8")
a=np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",f,"-f","f32le","-ac","1","-ar","16000","-"],capture_output=True).stdout,np.float32)
ws=[(w.start,w.end,w.word.strip()) for s in m.transcribe(a,language="en",word_timestamps=True,beam_size=5)[0] for w in s.words]
json.dump(ws,open(out,"w"))
print("HEARD:"," ".join(w for _,_,w in ws))
tl=json.load(open(tlf)); print("SCRIPT:"," ".join(s["text"] for s in tl))
# energy at each join: speech must not straddle a cut
r=np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",sys.argv[4],"-f","f32le","-ac","1","-ar","16000","-"],capture_output=True).stdout,np.float32)
H=160; a=r; e=20*np.log10(np.array([np.sqrt(np.mean(a[i:i+H]**2))+1e-9 for i in range(0,len(a)-H,H)]))
floor=np.percentile(e,10); peak=np.percentile(e,97); thr=floor+0.25*(peak-floor)
for s in tl[1:]:
    c=int(s["start"]*100); l=e[c-8:c]; r=e[c:c+5]
    print(f"join before {s['k']} @{s['start']:6.2f}: last 80ms max {l.max():5.1f} dB, first 50ms max {r.max():5.1f} dB, thr {thr:5.1f}  {'OK' if l.max()<thr and r.max()<thr else 'CHECK'}")
