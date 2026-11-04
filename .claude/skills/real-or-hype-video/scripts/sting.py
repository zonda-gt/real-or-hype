import numpy as np, wave, sys
sr=48000; bpm=180; beat=60/bpm; dur=1.6
t_all=np.zeros(int(sr*dur))
def tone(freqs,length,decay=6.0,bright=6):
    n=int(sr*length); t=np.arange(n)/sr; s=np.zeros(n)
    for f in freqs:
        for h in range(1,bright+1):
            s+=np.sin(2*np.pi*f*h*t+0.3*h)/(h**1.15)
    env=np.minimum(1,t/0.004)*np.exp(-decay*t)
    return s*env/len(freqs)
def kick(length=0.25):
    n=int(sr*length); t=np.arange(n)/sr; f=120*np.exp(-18*t)+45
    return np.sin(2*np.pi*np.cumsum(f)/sr)*np.exp(-9*t)
def hat(length=0.05):
    n=int(sr*length); return np.random.default_rng(1).normal(0,1,n)*np.exp(-60*np.arange(n)/sr)*0.25
def add(sig,at,g=1.0):
    i=int(at*sr); j=min(len(t_all),i+len(sig)); t_all[i:j]+=g*sig[:j-i]
# hook stabs: two short stabs on "IS IT", then a held bright chord on "REAL?"
Cm=[261.6,311.1,392.0]; Ab=[207.7,261.6,311.1]; Bb=[233.1,293.7,349.2]; Ebhi=[311.1,392.0,466.2,622.3]
add(tone(Cm,0.18,14),0.0,0.9); add(kick(),0.0,0.9); add(hat(),beat*0.5,1)
add(tone(Ab,0.18,14),beat,0.9); add(kick(),beat,0.8); add(hat(),beat*1.5,1)
add(tone(Bb,0.18,14),beat*2,0.9); add(kick(),beat*2,0.8)
add(tone(Ebhi,0.9,3.2,8),beat*3,1.0); add(kick(0.35),beat*3,1.0)
# small upward sweep into the last hit
n=int(sr*beat); tt=np.arange(n)/sr; sw=np.random.default_rng(2).normal(0,1,n)*np.linspace(0,0.18,n)
add(sw,beat*2,1)
t_all/=np.max(np.abs(t_all))*1.12
fade=int(sr*0.08); t_all[-fade:]*=np.linspace(1,0,fade)
st=np.stack([t_all,np.roll(t_all,int(sr*0.008))],1)
with wave.open(sys.argv[1],'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes((st*32767).astype('<i2').tobytes())
print('beat',beat)
