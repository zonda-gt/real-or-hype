import librosa, numpy as np
sr=22050; hop=512
reel,_=librosa.load("song.wav",sr=sr)
dj,_=librosa.load("yt/dj_kangxi.wav",sr=sr,duration=120)
Cd=librosa.feature.chroma_cens(y=dj,sr=sr,hop_length=hop)
res=[]
for speed in np.arange(0.90,1.36,0.025):
    q=librosa.effects.time_stretch(reel[:int(15.1*sr)],rate=speed)   # play reel at 'speed' -> compare to dj
    for shift in range(-3,4):
        qq=librosa.effects.pitch_shift(q,sr=sr,n_steps=shift) if shift else q
        Cq=librosa.feature.chroma_cens(y=qq,sr=sr,hop_length=hop)
        L=Cq.shape[1]
        sims=np.array([(Cd[:,i:i+L]*Cq).sum()/L for i in range(Cd.shape[1]-L)])
        i=sims.argmax(); res.append((sims[i],speed,shift,i*hop/sr))
res.sort(reverse=True)
for r in res[:8]: print("sim %.3f  reel-tempo x%.3f  pitch %+d st  -> reel 0:00 = dj %.2fs"%r)
