import librosa, numpy as np, json, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
y, sr = librosa.load("song.wav", sr=22050); hop=128
S=np.abs(librosa.stft(y,hop_length=hop,n_fft=2048)); f=librosa.fft_frequencies(sr=sr,n_fft=2048)
bands={"kick 30-120Hz":(30,120),"snare/clap 1.5-5kHz":(1500,5000),"hat 7k+":(7000,11000)}
ess=json.load(open("ess_beats.json"))
fig,axs=plt.subplots(6,1,figsize=(22,16),sharex=False)
for row,(a,b) in enumerate([(0,10),(10,20),(20,29.84)]):
    for j,(name,(lo,hi)) in enumerate(bands.items()):
        if j==2: continue
        env=librosa.onset.onset_strength(S=librosa.amplitude_to_db(S[(f>=lo)&(f<hi)]),sr=sr,hop_length=hop)
        t=np.arange(len(env))*hop/sr; m=(t>=a)&(t<b)
        ax=axs[row*2+j]; ax.plot(t[m],env[m]/env[m].max(),lw=1,color="k")
        for bt in ess["beats"]:
            if a<=bt<b: ax.axvline(bt,color="tab:blue",lw=0.8,alpha=0.6)
        ax.set_xlim(a,b); ax.set_xticks(np.arange(a,b,0.5)); ax.set_ylabel(name,fontsize=9); ax.grid(axis="x",alpha=0.2)
plt.tight_layout(); plt.savefig("chk/drums.png",dpi=70)
