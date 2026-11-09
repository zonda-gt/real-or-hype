import librosa, numpy as np, matplotlib, essentia.standard as es, json
matplotlib.use("Agg"); import matplotlib.pyplot as plt
sr=22050; y,_=librosa.load("yt/orig.wav",sr=sr,duration=70); hop=256
S=np.abs(librosa.stft(y,hop_length=hop,n_fft=2048)); f=librosa.fft_frequencies(sr=sr,n_fft=2048)
t=np.arange(S.shape[1])*hop/sr
def band(lo,hi): return librosa.amplitude_to_db(S[(f>=lo)&(f<hi)].mean(0),ref=np.max)
kick=librosa.onset.onset_strength(S=librosa.amplitude_to_db(S[(f>=30)&(f<120)]),sr=sr,hop_length=hop)
a=es.MonoLoader(filename="yt/orig.wav",sampleRate=44100)()
bpm,beats,conf,_,_=es.RhythmExtractor2013(method="multifeature")(a)
json.dump({"bpm":float(bpm),"beats":beats.tolist()},open("yt/orig_beats.json","w"))
fig,ax=plt.subplots(4,1,figsize=(24,13),sharex=True)
ax[0].imshow(librosa.amplitude_to_db(S[:400],ref=np.max),origin="lower",aspect="auto",extent=[0,t[-1],0,f[399]],cmap="magma",vmin=-60)
ax[0].set_ylabel("spectrogram 0-4.3kHz")
ax[1].plot(t,band(300,3000),lw=0.7); ax[1].set_ylabel("vocal band 300-3k dB")
ax[2].plot(t[:len(kick)],kick/np.percentile(kick,99),lw=0.7,color="k"); ax[2].set_ylabel("kick onsets")
ax[3].plot(t,band(30,120),lw=0.7,color="tab:red"); ax[3].set_ylabel("bass level dB")
for b in beats[beats<70]:
    ax[2].axvline(b,color="tab:blue",lw=0.5,alpha=0.4)
for a_ in ax: a_.set_xticks(np.arange(0,70,2)); a_.grid(axis="x",alpha=0.3)
plt.tight_layout(); plt.savefig("chk/orig_struct.png",dpi=55)
print("bpm",bpm,"first beats",np.round(beats[:40],3).tolist())
