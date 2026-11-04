import sys,subprocess,numpy as np
for f in sys.argv[1:]:
    a=np.frombuffer(subprocess.run(['ffmpeg','-loglevel','error','-i',f,'-af','silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse','-ar','16000','-ac','1','-f','f32le','-'],capture_output=True).stdout,dtype=np.float32)
    fs=16000; n=640; hop=160; f0=[]
    for i in range(0,len(a)-n,hop):
        x=a[i:i+n]
        if np.sqrt(np.mean(x**2))<0.02: continue
        x=x-x.mean(); c=np.correlate(x,x,'full')[n-1:]; lo,hi=int(fs/350),int(fs/70)
        k=lo+np.argmax(c[lo:hi])
        if c[k]>0.4*c[0]: f0.append(fs/k)
    f0=np.array(f0)
    print(f"{f.split('/')[-1]:12s} speech={len(a)/fs:4.2f}s  pitch_median={np.median(f0):5.0f}Hz  pitch_var={np.std(12*np.log2(f0/np.median(f0))):4.2f}st")
