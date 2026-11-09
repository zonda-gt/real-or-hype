import librosa, numpy as np
y, sr = librosa.load("song.wav", sr=22050); hop=128
S=np.abs(librosa.stft(y,hop_length=hop)); f=librosa.fft_frequencies(sr=sr)
env_k=librosa.onset.onset_strength(S=librosa.amplitude_to_db(S[(f>30)&(f<160)]),sr=sr,hop_length=hop)
env_f=librosa.onset.onset_strength(S=librosa.amplitude_to_db(S),sr=sr,hop_length=hop)
env = env_k/env_k.max() + env_f/env_f.max()
t = np.arange(len(env))*hop/sr
def score(P,ph,a,b):
    g=np.arange(ph,b,P); g=g[(g>=a)&(g<b)]
    idx=np.clip(np.round(g*sr/hop).astype(int),0,len(env)-1)
    # small window max
    return np.mean([env[max(0,i-2):i+3].max() for i in idx])
for a,b in [(0,14),(14,29.8),(0,29.8)]:
    best=max(((score(P,ph,a,b),P,ph) for P in np.arange(0.650,0.690,0.0005) for ph in np.arange(0,P,0.005)))
    print(a,b,"period %.4f bpm %.2f phase %.3f score %.3f"%(best[1],60/best[1],best[2],best[0]))
