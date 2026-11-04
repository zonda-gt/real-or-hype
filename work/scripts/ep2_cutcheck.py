# Energy check for both ends of each real-voice window (noise-relative, like cutcheck.py).
# Usage: ep2_cutcheck.py <workdir> name:start:end ...   Prints voiced runs near each cut.
import sys,os,subprocess,numpy as np
os.chdir(sys.argv[1])
def src(n):
    for e in ('.MOV','.mp4'):
        if os.path.exists('orig/'+n+e): return 'orig/'+n+e
def env(f,a,d):
    x=np.frombuffer(subprocess.run(['ffmpeg','-loglevel','error','-ss',str(max(0,a)),'-t',str(d),'-i',f,'-ac','1','-ar','16000','-af','highpass=f=150,lowpass=f=4000','-f','f32le','-'],capture_output=True).stdout,dtype=np.float32)
    h=160; return np.array([20*np.log10(np.sqrt(np.mean(x[i:i+h]**2))+1e-7) for i in range(0,len(x)-h+1,h)])
bad=0
for spec in sys.argv[2:]:
    n,a,b=spec.split(':'); a,b=float(a),float(b); f=src(n); a0=max(0,a-1.0)
    e=env(f,a0,(b-a0)+1.0); floor=np.percentile(e,10); peak=np.percentile(e,98); thr=floor+0.35*(peak-floor); v=e>thr
    ia=int(round((a-a0)/0.01)); ib=int(round((b-a0)/0.01))
    pre=np.where(v[:ia])[0]; gap_before=(ia-pre[-1]-1)*0.01 if len(pre) else 9
    first=np.where(v[ia:])[0]; lead=first[0]*0.01 if len(first) else 9
    last=np.where(v[:ib])[0]; tail=(ib-last[-1]-1)*0.01 if len(last) else 9
    nxt=np.where(v[ib:])[0]; nx=nxt[0]*0.01 if len(nxt) else 9
    ok=gap_before>=0.05 and tail>=0.15 and nx>=0.05; bad+=not ok
    # voiced runs inside window for orientation
    runs=[];s=None
    for i in range(ia,min(ib+60,len(v))):
        if v[i] and s is None: s=i
        if (not v[i] or i==min(ib+60,len(v))-1) and s is not None: runs.append((round(a0+s*0.01,2),round(a0+i*0.01,2))); s=None
    print(f"{n} {a:.2f}-{b:.2f}: speech-free before start {gap_before:.2f}s, lead {lead:.2f}s | silence before end {tail:.2f}s, next speech {nx:.2f}s  {'OK' if ok else 'FAIL'}\n   runs {runs}")
print('ALL OK' if not bad else f'{bad} FAIL')
