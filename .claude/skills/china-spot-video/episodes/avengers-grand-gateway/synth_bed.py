# Original synth "trailer" bed: D minor, 120 bpm, low ostinato + taiko-ish hits + string pad + final boom.
import numpy as np,soundfile as sf,sys
SR=48000; BPM=120; beat=60/BPM; L=float(sys.argv[2]) if len(sys.argv)>2 else 32
n=int(L*SR); out=np.zeros((n,2))
t_all=np.arange(n)/SR
def note(f): return 440*2**((f-69)/12)
def saw(fr,t,det=(0,)):
    s=0
    for d in det: ph=(fr*(1+d)*t)%1; s=s+(2*ph-1)
    return s/len(det)
def lp(x,a):  # one-pole lowpass, a in (0,1)
    y=np.zeros_like(x); acc=0
    for i in range(len(x)): acc+=a*(x[i]-acc); y[i]=acc
    return y
from scipy.signal import butter,sosfilt
def LP(x,fc,o=4): return sosfilt(butter(o,fc/(SR/2),output='sos'),x)
def HP(x,fc,o=2): return sosfilt(butter(o,fc/(SR/2),'high',output='sos'),x)
def add(sig,start,pan=0.0,g=1.0):
    i=int(start*SR)
    if i>=n or i<0: return
    e=min(n,i+len(sig)); s=sig[:e-i]*g
    out[i:e,0]+=s*(1-pan)/1.0; out[i:e,1]+=s*(1+pan)/1.0
chords=[(50,53,57),(46,50,53),(41,45,48),(48,52,55)]   # Dm Bb F C (MIDI roots low)
bars=int(L/(4*beat))+1
# pad: detuned saws, slow attack, per bar
for b in range(bars):
    ch=chords[b%4]; dur=4*beat+0.3; t=np.arange(int(dur*SR))/SR
    sig=sum(saw(note(m+12),t,(-0.004,0,0.005)) for m in ch)/3
    env=np.minimum(1,t/0.6)*np.minimum(1,(dur-t)/0.4)
    sig=LP(sig*env,1800 if b>=bars//2 else 1100)
    add(sig,b*4*beat,0,0.16)
# ostinato: 8th notes on the root, low saw, plucky
pat=[0,0,0,3,0,0,-2,0]
for b in range(bars):
    root=chords[b%4][0]-12
    for k in range(8):
        st=b*4*beat+k*beat/2; d=beat/2*0.9; t=np.arange(int(d*SR))/SR
        fr=note(root+(pat[k] if b%4==0 else 0)); sig=saw(fr,t,(-0.003,0.003))+0.5*np.sin(2*np.pi*fr/2*t)
        env=np.exp(-t*7); sig=LP(sig*env,900)
        add(sig,st,0,0.30 if b>0 else 0.18)
# taiko-ish hits: beats 1 and 3 (+ an and-of-4 pickup) from bar 1
rng=np.random.default_rng(1)
for b in range(1,bars):
    for pos,g in [(0,1.0),(2,0.8),(3.5,0.55)]:
        st=b*4*beat+pos*beat; t=np.arange(int(0.7*SR))/SR
        f=60+90*np.exp(-t*25); body=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*6)
        slap=LP(rng.standard_normal(len(t)),2500)*np.exp(-t*40)*0.5
        add(body+slap,st,0,0.55*g)
# hi ticks (16ths), faint, from bar 2
for b in range(2,bars):
    for k in range(16):
        st=b*4*beat+k*beat/4; t=np.arange(int(0.05*SR))/SR
        s=HP(rng.standard_normal(len(t)),7000)*np.exp(-t*90)
        add(s,st,0.3 if k%2 else -0.3,0.05 if k%4 else 0.09)
# riser into the end + final boom
rl=3.0; t=np.arange(int(rl*SR))/SR
riser=HP(rng.standard_normal(len(t)),1500)*(t/rl)**2*0.25
add(riser,L-rl-1.6,0,1)
t=np.arange(int(2.5*SR))/SR; f=45+80*np.exp(-t*12)
boom=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*1.6)+LP(rng.standard_normal(len(t)),800)*np.exp(-t*5)*0.4
add(boom,L-1.6,0,0.9)
# gentle reverb-ish smear via short delays
for d,g in [(0.031,0.25),(0.047,0.2),(0.089,0.15),(0.13,0.1)]:
    k=int(d*SR); out[k:,0]+=out[:-k,1]*g; out[k:,1]+=out[:-k,0]*g
out/=np.max(np.abs(out))*1.12
sf.write(sys.argv[1],out,SR)
