import sys,subprocess,numpy as np
f,a,b=sys.argv[1],float(sys.argv[2]),float(sys.argv[3])
x=np.frombuffer(subprocess.run(['ffmpeg','-loglevel','error','-ss',str(a),'-t',str(b-a),'-i',f,'-ac','1','-ar','16000','-af','highpass=f=150,lowpass=f=4000','-f','f32le','-'],capture_output=True).stdout,dtype=np.float32)
e=np.array([20*np.log10(np.sqrt(np.mean(x[i:i+160]**2))+1e-7) for i in range(0,len(x)-159,160)])
fl=np.percentile(e,10);pk=np.percentile(e,98);v=e>fl+0.35*(pk-fl)
runs=[];s=None
for i,t in enumerate(v):
    if t and s is None:s=i
    if not t and s is not None: runs.append((s,i));s=None
if s is not None: runs.append((s,len(v)))
print(' '.join(f'{a+r0*0.01:.2f}-{a+r1*0.01:.2f}' for r0,r1 in runs))
