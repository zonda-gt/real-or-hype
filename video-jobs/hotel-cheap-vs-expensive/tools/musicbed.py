# Procedural, licence-free music bed: soft pad + plucked arpeggio + light shaker, 96 bpm, C-G-Am-F.
import numpy as np, wave, sys
sr=48000; bpm=96; beat=60/bpm; dur=float(sys.argv[2]) if len(sys.argv)>2 else 32
t_total=int(sr*dur); out=np.zeros(t_total)
def note(f): return 440*2**((f-69)/12)
chords=[[48,55,60,64,67],[43,55,59,62,67],[45,57,60,64,69],[41,53,57,60,65]]
bar=4*beat; rng=np.random.default_rng(7)
for i in range(int(dur/bar)+1):
    ch=chords[i%4]; s0=int(i*bar*sr); n=int(bar*sr)
    t=np.arange(n)/sr; env=np.minimum(1,t/0.6)*np.minimum(1,(bar-t)/0.5)
    pad=sum(np.sin(2*np.pi*note(m)*t*(1+d))*0.05 for m in ch[1:] for d in(-0.002,0.002))
    bass=np.sin(2*np.pi*note(ch[0]-12)*t)*0.12*np.exp(-t*0.8)
    seg=(pad*env+bass); e=min(t_total,s0+n); out[s0:e]+=seg[:e-s0]
    arp=[ch[2]+12,ch[3]+12,ch[4]+12,ch[3]+12]*2
    for k,m in enumerate(arp):
        a0=s0+int(k*beat/2*sr); ln=int(0.45*sr)
        if a0>=t_total: break
        tt=np.arange(ln)/sr; pl=(np.sin(2*np.pi*note(m)*tt)+0.3*np.sin(4*np.pi*note(m)*tt))*np.exp(-tt*7)*0.07
        e=min(t_total,a0+ln); out[a0:e]+=pl[:e-a0]
    for k in range(8):
        a0=s0+int((k*beat/2+beat/4)*sr); ln=int(0.06*sr)
        if a0+ln>=t_total: break
        out[a0:a0+ln]+=rng.normal(0,1,ln)*np.exp(-np.arange(ln)/sr*60)*0.025
fade=int(1.5*sr); out[-fade:]*=np.linspace(1,0,fade); out[:int(0.3*sr)]*=np.linspace(0,1,int(0.3*sr))
out=out/np.max(np.abs(out))*0.8
st=np.stack([out,np.roll(out,int(0.011*sr))],1)
w=wave.open(sys.argv[1],"wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes((st*32767).astype(np.int16).tobytes()); w.close()
