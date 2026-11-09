import librosa, numpy as np
sr=22050; hop=512
reel,_=librosa.load("song.wav",sr=sr); dj,_=librosa.load("yt/orig.wav",sr=sr)
Cd=librosa.feature.chroma_cens(y=dj,sr=sr,hop_length=hop)
# reel line A ("我真的特别爱你", reel 0.2-2.2) as a short query, two speeds
for speed in (0.95,1.0):
    q=librosa.effects.time_stretch(reel[int(0.2*sr):int(7.4*sr)],rate=speed)   # A + B B B
    Cq=librosa.feature.chroma_cens(y=q,sr=sr,hop_length=hop); L=Cq.shape[1]
    sims=np.array([(Cd[:,i:i+L]*Cq).sum()/L for i in range(Cd.shape[1]-L)])
    pk=[i for i in range(1,len(sims)-1) if sims[i]>=sims[max(0,i-40):i+40].max() and sims[i]>0.78]
    print("speed",speed,"line-A matches (s, sim):",[(round(i*hop/sr,2),round(sims[i],3)) for i in pk])
# bass pumping level per 2 s
S=np.abs(librosa.stft(dj,hop_length=hop)); f=librosa.fft_frequencies(sr=sr)
bass=librosa.amplitude_to_db(S[(f>30)&(f<120)].mean(0),ref=np.max); t=np.arange(len(bass))*hop/sr
print("bass level (dB) per 4 s:")
print(" ".join(f"{int(a)}s:{bass[(t>=a)&(t<a+4)].mean():.0f}" for a in range(0,196,4)))
