# Version E renderer: picture cut to the narration's word timings.
import json,subprocess,os,sys
sys.path.insert(0,'.'); from e_plan import *
W,H,FPS=1080,1920,30
words=json.load(open('words.json')); os.makedirs('seg',exist_ok=True)
def run(c): subprocess.run(c,check=True)
def probe(f):
    s=json.loads(subprocess.run(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height','-of','json',f],capture_output=True,text=True).stdout)['streams'][0]; return s['width'],s['height']
def crop(src,x,w_out,h_out):
    w,h=probe(f'../broll/{src}.mp4'); c=CUT[src]; ch=h*(1-c); cw=ch*w_out/h_out
    if cw>w: cw=w; ch=cw*h_out/w_out
    X=min(max(x*w-cw/2,0),w-cw)
    return f"crop={int(cw)//2*2}:{int(ch)//2*2}:{int(X)}:0,scale={w_out}:{h_out}:flags=lanczos,setsar=1"
def shot(out,src,tin,nframes,speed,x,w_out=W,h_out=H):
    need=nframes/FPS*speed+0.3
    run(['ffmpeg','-y','-loglevel','error','-ss',f'{tin:.3f}','-t',f'{need:.3f}','-i',f'../broll/{src}.mp4','-vf',
         crop(src,x,w_out,h_out)+f',setpts=(PTS-STARTPTS)/{speed:.4f},fps={FPS}','-frames:v',str(nframes),'-an','-c:v','libx264','-preset','fast','-crf','16','-pix_fmt','yuv420p',out])
fr=lambda t: int(round(t*FPS))
T=words[-1][1]+TAIL
starts=[words[i][0]-0.10 for i,_ in CUES]+[T]
plan=[]   # (frame0, frame1, src, tin, speed, x)
# collage
plan_c=fr(starts[0])
for ci,(i,shots) in enumerate(CUES):
    f0,f1=fr(starts[ci]),fr(starts[ci+1]); L=(f1-f0)/FPS
    avail=sum(s[2] for s in shots)
    if avail>=L:   # give shots their natural length; drop/merge a tiny remainder
        alloc=[]; rem=L
        for s in shots:
            d=min(s[2],rem); alloc.append(d); rem-=d
            if rem<=1e-6: break
        if len(alloc)>1 and alloc[-1]<0.5: alloc[-2]+=alloc[-1]; alloc.pop()
        sp=[min(1.0,shots[k][2]/alloc[k]) for k in range(len(alloc))]
    else:
        sp0=avail/L; alloc=[s[2]/sp0 for s in shots]; sp=[sp0]*len(shots)
    cur=f0
    for k,d in enumerate(alloc):
        nf=f1-cur if k==len(alloc)-1 else fr(d); src,tin,mx,x=shots[k]
        minsp=0.72 if src in FPS60 else 0.9
        flag='  <-- SLOW' if sp[k]<minsp else ''
        plan.append((cur,cur+nf,src,tin,sp[k],x)); print(f'{cur/FPS:6.2f}-{(cur+nf)/FPS:6.2f} {src[-4:]} @{tin:6.2f} x{sp[k]:.2f}{flag}'); cur+=nf
segs=[]
# collage: 4 panels 540x960, each slowed to fill
n0=plan_c
for k,(src,tin,mx,x) in enumerate(COLLAGE):
    sp=min(1.0,mx/(n0/FPS)); shot(f'seg/c{k}.mp4',src,tin,n0,sp,x,540,960)
run(['ffmpeg','-y','-loglevel','error']+sum([['-i',f'seg/c{k}.mp4'] for k in range(4)],[])+['-filter_complex',
     '[0:v][1:v][2:v][3:v]xstack=inputs=4:layout=0_0|540_0|0_960|540_960,format=yuv420p[v]','-map','[v]','-frames:v',str(n0),'-c:v','libx264','-preset','fast','-crf','16','seg/000_collage.mp4'])
segs.append('seg/000_collage.mp4')
for j,(a,b,src,tin,sp,x) in enumerate(plan):
    o=f'seg/{j+1:03d}.mp4'; shot(o,src,tin,b-a,sp,x); segs.append(o)
open('concat.txt','w').write(''.join(f"file '{os.path.abspath(s)}'\n" for s in segs))
run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i','concat.txt','-c','copy','video.mp4'])
json.dump({'T':T,'starts':starts,'collage_end':starts[0]},open('timeline.json','w'))
print('frames',sum(b-a for a,b,*_ in plan)+n0,'expected',fr(T),'T',round(T,2))
