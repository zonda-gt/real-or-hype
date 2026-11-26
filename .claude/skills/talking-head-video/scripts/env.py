import sys,subprocess,numpy as np
f=sys.argv[1]
for rng in sys.argv[2:]:
    a,b=map(float,rng.split(':'))
    x=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-ss',str(a),'-t',str(b-a),'-i',f,'-ac','1','-ar','16000','-af','highpass=f=120,lowpass=f=6000','-f','f32le','-'],capture_output=True).stdout,np.float32)
    e=[20*np.log10(np.sqrt(np.mean(x[i:i+320]**2))+1e-9) for i in range(0,len(x)-320,320)]
    print(f"{a:.2f}: "+' '.join(f"{int(v)}" for v in e))   # 20 ms per value
