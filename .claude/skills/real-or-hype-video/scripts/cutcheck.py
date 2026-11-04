# For every segment carrying the creator's real voice: does the cut land in a real pause?
# Thresholds are relative to the clip's own noise floor (mall noise ~-38 dB defeats a fixed threshold).
import sys,os,subprocess,numpy as np
os.chdir(sys.argv[1])
if sys.argv[2].endswith('variants.py'):     # cutcheck.py <dir> scripts/variants.py <VAR>
    sys.path.insert(0,os.path.dirname(os.path.abspath(sys.argv[2]))); import variants; S=variants.S[sys.argv[3]]
else:
    txt=open(sys.argv[2]).read(); S=eval(txt[txt.index('S=[')+2:txt.index(']\nREACT=')+1],{'V':'VID_20260910_'})
def src(n):
    for e in ('.MOV','.mp4'):
        if os.path.exists('orig/'+n+e): return 'orig/'+n+e
def env(f,a,d):
    x=np.frombuffer(subprocess.run(['ffmpeg','-loglevel','error','-ss',str(max(0,a)),'-t',str(d),'-i',f,'-ac','1','-ar','16000','-af','highpass=f=150,lowpass=f=4000','-f','f32le','-'],capture_output=True).stdout,dtype=np.float32)
    h=160; return np.array([20*np.log10(np.sqrt(np.mean(x[i:i+h]**2))+1e-7) for i in range(0,len(x)-h+1,h)])
bad=0
for sid,kind,args,d,narr in S:
    if kind=='talk': n,a,vol,sp=args; span=d*sp
    elif kind=='price': n,_,a=args; sp=1.15; span=(d-0.15)*sp
    elif kind=='clip' and args[2]>=0.9: n,a,vol=args; span=d
    else: continue
    f=src(n); e=env(f,a-1.0,span+2.5)            # 10 ms frames, index 0 = a-1.0
    floor=np.percentile(e,10); peak=np.percentile(e,98); thr=floor+0.35*(peak-floor)   # speech if above 35% of floor->peak
    c=int(round((span+1.0)/0.01))
    voiced=e>thr
    # last voiced frame before the cut, first voiced frame after it
    before=np.where(voiced[:c])[0]; after=np.where(voiced[c:])[0]
    tail=(c-before[-1]-1)*0.01 if len(before) else 9; nxt=after[0]*0.01 if len(after) else 9
    ok=tail>=0.15 and nxt>=0.05
    bad+= not ok
    print(f"{sid:4s} {n:28s} cut@{a+span:6.2f}s  silence before cut {tail:4.2f}s (need ≥0.15)  next speech in {nxt:4.2f}s  floor {floor:5.1f} dB  {'OK' if ok else 'FAIL'}")
print('ALL OK' if not bad else f'{bad} FAIL')
sys.exit(1 if bad else 0)
