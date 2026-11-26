# snap rough segment bounds to real silence; fail if a handle would include other speech or clip this one
import sys,json,subprocess,numpy as np
src,segf,out=sys.argv[1:4]
x=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',src,'-ac','1','-ar','16000','-af','highpass=f=120,lowpass=f=6000','-f','f32le','-'],capture_output=True).stdout,np.float32)
H=160; e=20*np.log10(np.array([np.sqrt(np.mean(x[i:i+H]**2))+1e-9 for i in range(0,len(x)-H,H)]))
floor=np.percentile(e,10); peak=np.percentile(e,97); lo=floor+0.18*(peak-floor)   # sensitive: breaths/soft tails
print(f"floor {floor:.1f}  peak {peak:.1f}  sensitive thr {lo:.1f} dB")
v=e>lo; res=[]
for k,a,b,t in json.load(open(segf)):
    ia,ib=int(a*100),int(b*100)
    while ia>0 and v[ia-1:ia+1].any() or (ia>3 and v[ia-4:ia].sum()>=2): ia-=1   # walk back to silence
    while ib<len(v)-1 and v[ib:ib+2].any() or v[ib:ib+5].sum()>=2: ib+=1        # walk forward to silence
    on,off=ia*0.01,ib*0.01
    pre=np.where(v[max(0,ia-30):ia])[0]; post=np.where(v[ib:ib+30])[0]
    i0=on-min(0.10,(len(pre) and (30-pre[-1]-1)*0.01 or 0.3)-0.02 if len(pre) else 0.10)
    i1=off+min(0.18,(post[0]*0.01-0.03) if len(post) else 0.18)
    flag='' if (i0<a-0.02 and i1>b) else '  <-- CHECK (bounds tighter than whisper)'
    print(f"{k}: rough {a:6.2f}-{b:6.2f} -> voice {on:6.2f}-{off:6.2f}  cut {i0:6.2f}-{i1:6.2f}  clear before {(len(pre) and (30-pre[-1]-1)*0.01) if len(pre) else '>0.3'} after {post[0]*0.01 if len(post) else '>0.3'}{flag}")
    res.append([k,round(i0,3),round(i1,3),t])
json.dump(res,open(out,'w'),indent=0)
