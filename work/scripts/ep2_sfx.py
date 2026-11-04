# Same effects and gains as add_sfx.py (earshot-ranked set); events from seg/sfx.json. Usage: ep2_sfx.py <workdir> <in> <out>
import sys,os,subprocess,json,numpy as np
os.chdir(sys.argv[1]); inp_v,out=sys.argv[2:4]; ev=json.load(open('seg/sfx.json'))
def peak_db(f):
    a=np.frombuffer(subprocess.run(['ffmpeg','-loglevel','error','-i',f,'-ac','1','-f','f32le','-'],capture_output=True).stdout,dtype=np.float32)
    return 20*np.log10(np.abs(a).max()+1e-9)
inp=['-i',inp_v]; fc=''
for i,(n,po,t,v,tr) in enumerate(ev):
    f=f'sfx/{n}.wav'; inp+=['-i',f]; g=10**((-6-peak_db(f))/20)*v; ms=max(0,int((t-po)*1000))
    fc+=f'[{i+1}:a]aresample=48000,aformat=channel_layouts=stereo,volume={g:.4f},adelay={ms}|{ms}[s{i}];'
fc+='[0:a]'+''.join(f'[s{i}]' for i in range(len(ev)))+f'amix=inputs={len(ev)+1}:normalize=0:duration=first,alimiter=limit=0.84:level=false[a]'
subprocess.run(['ffmpeg','-loglevel','error','-y']+inp+['-filter_complex',fc,'-map','0:v','-map','[a]','-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart',out],check=True)
print('sfx ok')
