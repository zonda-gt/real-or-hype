# usage: render.py <workdir> [VAR]  (VAR -> segs_VAR.py, vo_VAR/, out_VAR/)   (workdir has raw/, vo/L*.wav, title.png)  -> out/cut.mp4 + out/starts.json
import os,sys,json,subprocess
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import importlib
VAR=sys.argv[2] if len(sys.argv)>2 else ''
_m=importlib.import_module('segs'+('_'+VAR if VAR else '')); globals().update({k:v for k,v in vars(_m).items() if not k.startswith('__')})
OUT='out'+('_'+VAR if VAR else '')+os.environ.get('OUTSUF',''); VOD='vo'+('_'+VAR if VAR else ''); HK='hook'+('_'+VAR if VAR else '')
OVL=globals().get('OVL',[])
W=sys.argv[1]; os.chdir(W); os.makedirs(OUT+'/seg',exist_ok=True)
# HDR (HLG) -> SDR: BT.2446 Method A tone mapping baked into a 3D LUT (hlg2sdr_lut.py, exposure 1.5); the old zscale+hable
# chain tone-mapped each channel separately and left a yellow/orange cast.
LUT=os.environ.get('LUT') or os.path.join(os.path.dirname(os.path.abspath(__file__)),'hlg2sdr_bt2446a_exp1.5.cube')
POSTVF=os.environ.get('POSTVF','')   # e.g. vignette + grain for the cinematic grade
TM=f'scale=in_color_matrix=bt2020:in_range=tv:out_range=pc,format=gbrpf32le,lut3d={LUT}:interp=tetrahedral,scale=out_color_matrix=bt709:out_range=tv,format=yuv420p'
FULL='scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1'
ENC=['-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-c:a','pcm_s16le','-ar','48000','-ac','2']
AF='aresample=48000,aformat=channel_layouts=stereo'
AMB=float(os.environ.get('AMBVOL','0.35'))   # room sound under narration (0.06 = mostly gone; creator: too much background noise)
def run(c):
    r=subprocess.run(c,capture_output=True,text=True)
    if r.returncode: print(r.stderr[-1500:]); sys.exit(1)
def dur(f): return float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f],capture_output=True,text=True).stdout)
st={}; t=0.0; parts=[]
for seg in SEGS:
    sid,clip,a,ln,sp,au=seg[:6]; z=seg[6:]
    o=f'{OUT}/seg/{sid}.mov'; d=ln/sp
    zc=f',scale=iw*{z[0]}:ih*{z[0]},crop=1080:1920:(iw-1080)*{z[1]}:(ih-1920)*{z[2]}' if z else ''
    if au=='real': af=f'{AF},atempo={sp},highpass=f=80,loudnorm=I=-16:TP=-1.5:LRA=11,{AF},afade=t=in:d=0.03,afade=t=out:st={d-0.05:.3f}:d=0.05'
    else: af=f'{AF},atempo={sp},highpass=f=100,volume={AMB}' if sp<=2 else f'{AF},atempo=2.0,atempo={sp/2},highpass=f=100,volume={AMB}'
    fc=f'[0:v]setpts=(PTS-STARTPTS)/{sp},{TM},{FULL}{zc}{(","+POSTVF) if POSTVF else ""}[v];[0:a]{af},apad[a]'
    run(['ffmpeg','-loglevel','error','-y','-ss',f'{a:.3f}','-t',f'{ln+0.1:.3f}','-i',f'raw/20261115_{clip}.mp4','-filter_complex',fc,'-map','[v]','-map','[a]','-t',f'{d:.3f}']+ENC+[o])
    st[sid]=t; md=dur(o); t+=md; parts.append(o); print(f'{sid:4s} {st[sid]:6.2f} +{md:.2f}')
open(OUT+'/list.txt','w').write(''.join(f"file 'seg/{os.path.basename(p)}'\n" for p in parts))
run(['ffmpeg','-loglevel','error','-y','-f','concat','-safe','0','-i',OUT+'/list.txt','-c:v','copy','-af','aresample=async=1','-c:a','pcm_s16le',OUT+'/base.mov'])
total=dur(OUT+'/base.mov'); st['_end']=total
# narration placement + gap check
vo=[]; ok=True
for k,sid,off in VO:
    s=st[sid]+off; vo.append((k,s,s+dur(f'{VOD}/{k}.wav')))
reals=[(sid,st[sid]+(SPEECH[sid][0]-a)/sp,st[sid]+(SPEECH[sid][1]-a)/sp) for sid,c,a,ln,sp,au,*_ in SEGS if au=='real']
ev=sorted([(s,e,k) for k,s,e in vo]+[(s,e,k) for k,s,e in reals])
for (s1,e1,k1),(s2,e2,k2) in zip(ev,ev[1:]):
    if e1+0.05>s2: print(f'OVERLAP {k1} ends {e1:.2f} > {k2} starts {s2:.2f}'); ok=False
if ev[-1][1]>total-0.3: print('last line ends too late',ev[-1]); ok=False
json.dump({'starts':st,'vo':vo},open(OUT+'/starts.json','w'),indent=1)
print(f'total {total:.2f}s  gaps', 'OK' if ok else 'FAIL'); sys.exit(0 if ok else 1)
