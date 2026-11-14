# Giraffe Manor episode renderer: B-roll shots + creator-clone narration + music + subtitles.
# usage: python3 render.py <VARIANT>   (variants defined in plan.py)
import sys,os,json,subprocess,numpy as np
sys.path.insert(0,'.')
from plan import VARIANTS, SRC
from lines import LINES
V=sys.argv[1]; P=VARIANTS[V]
FPS=30; W,H=1080,1920
os.makedirs(f'out/{V}/seg',exist_ok=True)
def run(c): subprocess.run(c,check=True)
def dur(f): return float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f],capture_output=True,text=True).stdout)
def probe(f):
    s=json.loads(subprocess.run(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height,color_transfer','-of','json',f],capture_output=True,text=True).stdout)['streams'][0]
    return s['width'],s['height'],s.get('color_transfer','')
def shot_vf(src,xc,zoom,yc):
    w,h,tr=probe(src)
    tm='zscale=tin=arib-std-b67:min=bt2020nc:pin=bt2020:t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p,' if tr=='arib-std-b67' else ''
    cut=SRC[os.path.basename(src)[:-4]].get('cut',0.0)   # fraction of height to drop at the bottom (burned-in subtitles)
    ch=h*(1-cut)/zoom; cw=ch*9/16
    if cw>w: cw=w; ch=cw*16/9
    x=min(max(xc*w-cw/2,0),w-cw); y=min(max(yc*h*(1-cut)-ch/2,0),h*(1-cut)-ch)
    return f"{tm}crop={int(cw)//2*2}:{int(ch)//2*2}:{int(x)}:{int(y)},scale={W}:{H}:flags=lanczos,setsar=1"
# --- 1. shots -> segments; narration slots
segs=[]; t=0.0; vo_place=[]; cuts=[]
for si,(key,shots) in enumerate(P['slots']):
    slot0=t
    for k,sh in enumerate(shots):
        sid,tin,d=sh[0],sh[1],sh[2]; o=sh[3] if len(sh)>3 else {}
        sp=o.get('speed',1.0); src=f'broll/{sid}.mp4'
        out=f'out/{V}/seg/{si:02d}_{k}.mp4'
        vf=shot_vf(src,o.get('x',0.5),o.get('zoom',1.0),o.get('y',0.5))+f",setpts=(PTS-STARTPTS)/{sp},fps={FPS}"
        if not os.path.exists(out):
            run(['ffmpeg','-y','-loglevel','error','-ss',str(tin),'-t',str(d*sp+0.2),'-i',src,'-vf',vf,'-t',str(d),'-an','-c:v','libx264','-preset','fast','-crf','17','-pix_fmt','yuv420p',out])
        segs.append(out); cuts.append(t); t+=dur(out)
    if key:
        vo_place.append((key,slot0+P.get('lead',{}).get(key,0.12)))
    if key and P.get('check',True):
        vd=dur(f'vo/{key}.wav'); end=vo_place[-1][1]+vd
        print(f'{key:3s} slot {slot0:5.2f}-{t:5.2f}  vo ends {end:5.2f}  spare {t-end:+.2f}')
total=t
for i,(k,s) in enumerate(vo_place):
    e=s+dur(f'vo/{k}.wav'); nxt=vo_place[i+1][1] if i+1<len(vo_place) else total-0.3
    assert e<=nxt-0.05, f'overlap {k}: ends {e:.2f} next {nxt:.2f}'
open(f'out/{V}/concat.txt','w').write(''.join(f"file '{os.path.abspath(s)}'\n" for s in segs))
run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',f'out/{V}/concat.txt','-c','copy',f'out/{V}/video.mp4'])
json.dump({'total':total,'vo':vo_place,'cuts':cuts},open(f'out/{V}/timeline.json','w'),indent=1)
print('total',round(total,2))
