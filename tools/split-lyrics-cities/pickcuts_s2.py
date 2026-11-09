import librosa, numpy as np, json
y,sr=librosa.load("song.wav",sr=22050); hop=128; fps=sr/hop
S=np.abs(librosa.stft(y,hop_length=hop,n_fft=2048)); f=librosa.fft_frequencies(sr=sr,n_fft=2048)
def env(lo,hi):
    e=librosa.onset.onset_strength(S=librosa.amplitude_to_db(S[(f>=lo)&(f<hi)]),sr=sr,hop_length=hop); return e/np.percentile(e,99)
drum=np.maximum(env(30,120),env(1500,5000))
g=json.load(open("grid.json")); P,ph=g["P"],g["ph"]
P=P/2; K=int((17.342-ph)/P)
bt=ph+np.arange(K+1)*P
# strength = peak drum onset within +-35 ms of the beat, and where exactly it peaks
st=[];pk=[]
for t in bt:
    i0,i1=max(0,int((t-0.035)*fps)),int((t+0.035)*fps)+1
    j=i0+np.argmax(drum[i0:i1]); st.append(drum[j]); pk.append(j/fps)
st=np.array(st); pk=np.array(pk)
# DP over beats: cuts at beats, segment 2..5 beats, first cut >= beat 2, last segment ends at song end (>=3 beats)
best={0:(0.0,[])}
for k in range(1,K+1):
    cand=[]
    for L in range(4,9):
        if k-L in best:
            sc,path=best[k-L]
            cand.append((sc+(st[k]-1.0),path+[k]))
    if cand: best[k]=max(cand)
end=[k for k in best if 4<=K-k<=8]
k_last=max(end,key=lambda k:best[k][0])
cuts=best[k_last][1]
print("chosen cut beats:",cuts)
print("cut times:",[round(bt[k],3) for k in cuts])
print("lengths(beats):",np.diff([0]+cuts).tolist(), "+ tail", K-k_last)
print("strength at cuts: mean %.2f  min %.2f  | all beats mean %.2f"%(st[cuts].mean(),st[cuts].min(),st.mean()))
print("actual hit offset vs grid (ms):",[round((pk[k]-bt[k])*1000) for k in cuts])
json.dump({"cuts":[float(round(pk[k]*30)/30) for k in cuts],"grid":[float(bt[k]) for k in cuts],"strength":[float(st[k]) for k in cuts],"beats":cuts,"P":P,"ph":ph},open("cuts.json","w"))
