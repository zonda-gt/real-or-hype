import numpy as np,wave,sys
sr=48000; rng=np.random.default_rng(7)
def save(name,x):
    x=x/np.max(np.abs(x))*0.5; st=np.stack([x,x],1)
    with wave.open(name,'wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes((st*32767).astype('<i2').tobytes())
# whoosh: noise through a resonant band-pass sweeping up then down, swelling to a peak at 0.30 s
n=int(sr*0.55); t=np.arange(n)/sr; noise=rng.normal(0,1,n)
fc=400+2600*np.exp(-((t-0.30)/0.13)**2); y=np.zeros(n); lp=bp=0.0
for i in range(n):
    f=2*np.sin(np.pi*fc[i]/sr); q=0.35
    lp+=f*bp; hp=noise[i]-lp-q*bp; bp+=f*hp; y[i]=bp
env=np.exp(-((t-0.30)/0.11)**2); save('sfx/whoosh.wav',y*env)
# pop: short sine with fast pitch drop
n=int(sr*0.09); t=np.arange(n)/sr; f=900*np.exp(-30*t)+250
save('sfx/pop.wav',np.sin(2*np.pi*np.cumsum(f)/sr)*np.exp(-45*t)*np.minimum(1,t/0.002))
print('ok')
# buzz: short low "wrong answer" double buzz (square-ish, 150/140 Hz)
n=int(sr*0.16); t=np.arange(n)/sr
def bz(f): x=np.tanh(4*np.sin(2*np.pi*f*t)); return x*np.minimum(1,t/0.005)*np.minimum(1,(0.16-t)/0.02)
gap=np.zeros(int(sr*0.04)); save('sfx/buzz.wav',np.concatenate([bz(150),gap,bz(140)]))
print('buzz ok')
