# speech islands by relative energy, each transcribed on its own (catches every retake)
import sys,json,subprocess,numpy as np
from faster_whisper import WhisperModel
m=WhisperModel(sys.argv[2] if len(sys.argv)>2 else "medium",device="cpu",compute_type="int8")
f=sys.argv[1]
a=np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",f,"-f","f32le","-ac","1","-ar","16000","-"],capture_output=True).stdout,np.float32)
H=160; e=20*np.log10(np.array([np.sqrt(np.mean(a[i:i+H]**2))+1e-9 for i in range(0,len(a)-H,H)]))
floor=np.percentile(e,10); peak=np.percentile(e,95); thr=floor+0.35*(peak-floor)
v=e>thr; isl=[]; i=0
while i<len(v):
    if v[i]:
        j=i
        while j<len(v) and (v[j] or (j+35<len(v) and v[j:j+35].any())): j+=1   # bridge gaps <0.35 s
        isl.append((i*0.01,j*0.01)); i=j
    else: i+=1
isl=[(s,t) for s,t in isl if t-s>0.25]
out=[]
for s,t in isl:
    s0=max(0,s-0.15); t0=min(len(a)/16000,t+0.15)
    seg=list(m.transcribe(a[int(s0*16000):int(t0*16000)],language="en",word_timestamps=True,beam_size=5,condition_on_previous_text=False)[0])
    ws=[(s0+w.start,s0+w.end,w.word) for g in seg for w in g.words]
    out.append({"s":s,"e":t,"w":ws}); print(f"{s:6.2f}-{t:6.2f} |{''.join(x[2] for x in ws)}",flush=True)
json.dump(out,open(f[:-4]+"_isl.json","w"))
print("thr",round(floor,1),round(peak,1))
