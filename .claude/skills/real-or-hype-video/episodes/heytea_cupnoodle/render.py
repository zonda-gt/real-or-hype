# usage: render.py <workdir>   (workdir has raw/, vo/L*.wav, title.png)  -> out/cut.mp4 + out/starts.json
import os,sys,json,subprocess
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); from segs import *
W=sys.argv[1]; os.chdir(W); os.makedirs('out/seg',exist_ok=True)
TM='zscale=tin=arib-std-b67:min=bt2020nc:pin=bt2020:t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p'
FULL='scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1'
ENC=['-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-c:a','pcm_s16le','-ar','48000','-ac','2']
AF='aresample=48000,aformat=channel_layouts=stereo'
def run(c):
    r=subprocess.run(c,capture_output=True,text=True)
    if r.returncode: print(r.stderr[-1500:]); sys.exit(1)
def dur(f): return float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f],capture_output=True,text=True).stdout)
st={}; t=0.0; parts=[]
for sid,clip,a,ln,sp,au in SEGS:
    o=f'out/seg/{sid}.mov'; d=ln/sp
    if au=='real': af=f'{AF},atempo={sp},highpass=f=80,loudnorm=I=-16:TP=-1.5:LRA=11,{AF},afade=t=in:d=0.03,afade=t=out:st={d-0.05:.3f}:d=0.05'
    else: af=f'{AF},atempo={sp},highpass=f=100,volume=0.35' if sp<=2 else f'{AF},atempo=2.0,atempo={sp/2},highpass=f=100,volume=0.35'
    fc=f'[0:v]setpts=(PTS-STARTPTS)/{sp},{TM},{FULL}[v];[0:a]{af},apad[a]'
    run(['ffmpeg','-loglevel','error','-y','-ss',f'{a:.3f}','-t',f'{ln+0.1:.3f}','-i',f'raw/20261115_{clip}.mp4','-filter_complex',fc,'-map','[v]','-map','[a]','-t',f'{d:.3f}']+ENC+[o])
    st[sid]=t; md=dur(o); t+=md; parts.append(o); print(f'{sid:4s} {st[sid]:6.2f} +{md:.2f}')
open('out/list.txt','w').write(''.join(f"file 'seg/{os.path.basename(p)}'\n" for p in parts))
run(['ffmpeg','-loglevel','error','-y','-f','concat','-safe','0','-i','out/list.txt','-c:v','copy','-af','aresample=async=1','-c:a','pcm_s16le','out/base.mov'])
total=dur('out/base.mov'); st['_end']=total
# narration placement + gap check
vo=[]; ok=True
for k,sid,off in VO:
    s=st[sid]+off; vo.append((k,s,s+dur(f'vo/{k}.wav')))
reals=[(sid,st[sid]+(SPEECH[sid][0]-a)/sp,st[sid]+(SPEECH[sid][1]-a)/sp) for sid,c,a,ln,sp,au in SEGS if au=='real']
ev=sorted([(s,e,k) for k,s,e in vo]+[(s,e,k) for k,s,e in reals])
for (s1,e1,k1),(s2,e2,k2) in zip(ev,ev[1:]):
    if e1+0.05>s2: print(f'OVERLAP {k1} ends {e1:.2f} > {k2} starts {s2:.2f}'); ok=False
if ev[-1][1]>total-0.3: print('last line ends too late',ev[-1]); ok=False
json.dump({'starts':st,'vo':vo},open('out/starts.json','w'),indent=1)
print(f'total {total:.2f}s  gaps', 'OK' if ok else 'FAIL'); sys.exit(0 if ok else 1)
