# usage: add_sfx.py <workdir> <in.mp4> <starts.txt> <out.mp4>
# Effects chosen by earshot ranking (whoosh_fast/tight, pop/0, mallet/up4 "success chime"); each is peak-normalised
# to -6 dBFS, then given a role volume. Times put each effect's PEAK on its moment.
import sys,os,subprocess,ast,numpy as np
os.chdir(sys.argv[1]); inp_v,stf,out=sys.argv[2:5]; st=ast.literal_eval(open(stf).read())
def peak_db(f):
    a=np.frombuffer(subprocess.run(['ffmpeg','-loglevel','error','-i',f,'-ac','1','-f','f32le','-'],capture_output=True).stdout,dtype=np.float32)
    return 20*np.log10(np.abs(a).max()+1e-9)
# (file, peak offset in file, moment, role volume, trim)
ev=[('whoosh_es',0.310,st['O1'],0.45,None),('whoosh_es',0.310,st['A1'],0.45,None),('whoosh_es',0.310,st['R1'],0.45,None),
    ('pop_es',0.0,st['O5']+0.03,0.40,None),
    ('real_es',0.335,st['V1']+1.1,0.45,None),
    ('buzz_el',0.345,st['V1']+2.0,0.40,None)]
dk='I4' if 'I4' in st else ('B1' if 'B1' in st else None)
if dk: ev.append(('ding',0.05,st[dk]+0.13,0.55,(0,0.45)))
inp=['-i',inp_v]; fc=''
for i,(n,po,t,v,tr) in enumerate(ev):
    f=f'sfx/{n}.wav'; inp+=['-i',f]; g=10**((-6-peak_db(f))/20)*v; ms=max(0,int((t-po)*1000))
    trim=f'atrim={tr[0]}:{tr[1]},asetpts=PTS-STARTPTS,afade=t=out:st={tr[1]-tr[0]-0.08:.2f}:d=0.08,' if tr else ''
    fc+=f'[{i+1}:a]{trim}aresample=48000,aformat=channel_layouts=stereo,volume={g:.4f},adelay={ms}|{ms}[s{i}];'
fc+='[0:a]'+''.join(f'[s{i}]' for i in range(len(ev)))+f'amix=inputs={len(ev)+1}:normalize=0:duration=first,alimiter=limit=0.84:level=false[a]'
subprocess.run(['ffmpeg','-loglevel','error','-y']+inp+['-filter_complex',fc,'-map','0:v','-map','[a]','-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart',out],check=True)
print('sfx ok')
