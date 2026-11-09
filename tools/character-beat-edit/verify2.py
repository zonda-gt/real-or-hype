import subprocess, numpy as np, librosa, json, sys, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
def cuts_of(path):
    raw=subprocess.run(["ffmpeg","-v","error","-i",path,"-vf","scale=90:160,format=gray","-f","rawvideo","-"],capture_output=True).stdout
    fr=np.frombuffer(raw,np.uint8).reshape(-1,160,90).astype(np.float32)
    # compare only the top band (above character/subtitles; skip label at y~250/1920 -> rows 15-30)
    d=np.array([np.abs(fr[i,32:75]-fr[i-1,32:75]).mean() for i in range(1,len(fr))])
    thr=max(18,np.percentile(d,90)*1.8)
    idx=[i+1 for i in range(len(d)) if d[i]>thr and d[i]==d[max(0,i-3):i+4].max()]
    return np.array(idx)/30.0
y,sr=librosa.load("song2.wav",sr=22050); hop=128; fps=sr/hop
S=np.abs(librosa.stft(y,hop_length=hop,n_fft=2048)); f=librosa.fft_frequencies(sr=sr,n_fft=2048)
def env(lo,hi):
    e=librosa.onset.onset_strength(S=librosa.amplitude_to_db(S[(f>=lo)&(f<hi)]),sr=sr,hop_length=hop); return e/np.percentile(e,99)
drum=np.maximum(env(30,120),env(1500,5000))
def strength(ts):  # strongest drum onset within +-40 ms
    return np.array([drum[max(0,int(t*fps)-4):int(t*fps)+5].max() for t in ts])
rng=np.random.default_rng(0); rnd=strength(rng.uniform(0.3,29.2,2000))
g=json.load(open("grid2.json")); P,ph=g["P"],g["ph"]
res={}
for name in sys.argv[1:]:
    c=cuts_of(name); c=c[c>0.2]
    off=((c-ph+P/2)%P-P/2)*1000
    st=strength(c)
    res[name]=c
    print(f"{name}: {len(c)} cuts | offset from 135-BPM beat: median {np.median(np.abs(off)):.0f} ms, max {np.abs(off).max():.0f} ms | drum hit at cut: {st.mean():.2f} (random moments {rnd.mean():.2f}); cuts with a clear drum hit: {(st>np.percentile(rnd,75)).mean()*100:.0f}% (random 25%)")
# picture: drum envelope + cuts of each version
t=np.arange(len(drum))/fps
fig,axs=plt.subplots(len(res),1,figsize=(22,3.2*len(res)))
axs=np.atleast_1d(axs)
for ax,(name,c) in zip(axs,res.items()):
    ax.plot(t,drum,color="0.35",lw=0.7,label="drums (kick + snare onsets)")
    for k in np.arange(ph,29.42,P): ax.axvline(k,color="0.85",lw=0.6,zorder=0)
    for x in c: ax.axvline(x,color="crimson",lw=2)
    ax.set_xlim(0,29.424); ax.set_ylim(0,1.6); ax.set_title(f"{name}: red = scene cuts, grey lines = 135 BPM beats",fontsize=12,loc="left")
    ax.set_xticks(range(0,30))
plt.tight_layout(); plt.savefig("chk/beat_check.png",dpi=60)
