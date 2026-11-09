import librosa, numpy as np, sys
y, sr = librosa.load(sys.argv[1], sr=22050)
hop=256
for name, (lo, hi) in {"kick": (30, 150), "snare/clap": (1500, 5000), "full": (0, 11025)}.items():
    yb = librosa.effects.preemphasis(y) if name=="snare/clap" else y
    S = np.abs(librosa.stft(y, hop_length=hop))
    f = librosa.fft_frequencies(sr=sr)
    band = S[(f>=lo)&(f<hi)]
    env = librosa.onset.onset_strength(S=librosa.amplitude_to_db(band), sr=sr, hop_length=hop)
    ac = librosa.autocorrelate(env - env.mean())
    lags = np.arange(len(ac))*hop/sr
    m = (lags>0.25)&(lags<2.5)
    top = np.argsort(ac[m])[::-1]
    picked=[]
    for t in top:
        L = lags[m][t]
        if all(abs(L-p)>0.05 for p in picked): picked.append(L)
        if len(picked)==6: break
    print(name, "autocorr lags(s):", [round(p,3) for p in picked], "-> bpm", [round(60/p,1) for p in picked])
    on = librosa.onset.onset_detect(onset_envelope=env, sr=sr, hop_length=hop, units="time", delta=0.3 if name!="full" else 0.2)
    print("  onsets first 10s:", np.round(on[on<10],2).tolist())
