import sys,glob,os,subprocess,json,numpy as np,torch,torchaudio,soundfile as sf
from speechbrain.inference.speaker import EncoderClassifier
enc=EncoderClassifier.from_hparams(source='speechbrain/spkrec-ecapa-voxceleb',savedir=os.path.expanduser('~/.cache/ecapa'),run_opts={'device':'cpu'})
def load(f):
    w=subprocess.run(['ffmpeg','-v','error','-i',f,'-ac','1','-ar','16000','-f','f32le','-'],capture_output=True).stdout
    return np.frombuffer(w,np.float32).copy()
def emb(x):
    es=[]
    for i in range(0,max(1,len(x)-16000*6),16000*6):
        seg=x[i:i+16000*8]
        if len(seg)<16000*3: continue
        es.append(enc.encode_batch(torch.tensor(seg)[None]).squeeze().numpy())
    e=np.mean(es,0); return e/np.linalg.norm(e)
def f0stats(x,sr=16000):
    f=[]
    for k in range(0,len(x)-640,320):
        fr=x[k:k+640]-x[k:k+640].mean()
        if np.sqrt(np.mean(fr**2))<0.02: continue
        ac=np.correlate(fr,fr,'full')[639:]; lo,hi=sr//450,sr//90
        p=np.argmax(ac[lo:hi])+lo
        if ac[p]/ac[0]>0.55: f.append(sr/p)
    f=np.array(f); st=12*np.log2(np.percentile(f,90)/np.percentile(f,10))
    return np.median(f),st
ref_dir=sys.argv[1]; cand=sys.argv[2:]
refs=[load(f) for f in sorted(glob.glob(ref_dir+'/*/vocals.wav'))]
R=emb(np.concatenate(refs)); fm,fst=f0stats(np.concatenate(refs))
print(f'HER: f0 median {fm:.0f} Hz, pitch range {fst:.1f} semitones (10-90%)')
for c in cand:
    x=load(c); e=emb(x); m,st=f0stats(x)
    al=json.load(open(c[:-4]+'.align.json')); dur=al['character_end_times_seconds'][-1]
    words=len(''.join(al['characters']).split())
    print(f'{os.path.basename(c)[:-4]:14s} similarity {float(e@R):.3f} | f0 {m:.0f} Hz | range {st:.1f} st | {words/dur*60:.0f} wpm raw ({dur:.1f}s)')
