import librosa, numpy as np, json
y, sr = librosa.load("song.wav", sr=22050); hop=128
S=np.abs(librosa.stft(y,hop_length=hop,n_fft=2048)); f=librosa.fft_frequencies(sr=sr,n_fft=2048)
def env(lo,hi):
    e=librosa.onset.onset_strength(S=librosa.amplitude_to_db(S[(f>=lo)&(f<hi)]),sr=sr,hop_length=hop); return e/np.percentile(e,99)
ek, es_ = env(30,120), env(1500,5000)
fps=sr/hop
def at(e,ts):
    i=np.round(np.asarray(ts)*fps).astype(int); i=i[(i>=2)&(i<len(e)-2)]
    return np.array([e[j-2:j+3].max() for j in i])
best=None
for P in np.arange(0.4400,0.4500,0.0001):
    for ph in np.arange(0,P,0.002):
        g=np.arange(ph,29.8,P); s=at(ek,g).mean()+at(es_,g).mean()
        if best is None or s>best[0]: best=(s,P,ph)
s,P,ph=best
off=np.arange(ph+P/2,29.8,P); soff=at(ek,off).mean()+at(es_,off).mean()
print(f"best grid: period {P:.4f}s = {60/P:.2f} BPM, phase {ph:.3f}s, on-grid score {s:.3f} vs half-beat-shifted {soff:.3f}")
g=np.arange(ph,29.8,P)
sn=at(es_,g); kk=at(ek,g)
for k in range(4):
    print(f" beat position {k}: snare {sn[k::4].mean():.3f}  kick {kk[k::4].mean():.3f}")
json.dump({"P":P,"ph":ph},open("grid135.json","w"))
