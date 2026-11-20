# Local copy of render_cut.py with a band crop: SRC[id]['top'] (fraction dropped at the top) and an optional 5th shot element
# {'top':..,'cut':..} overriding the source's band per shot (burned-in subtitles in the MIDDLE of many vlogs). usage: render_band.py <workdir>
# plan.py: SRC={id:{'cut':frac_of_height_to_drop_at_bottom}}, CUES=[(word_idx,[(src,t_in,max_src_secs,x_centre),...]),...],
#          COLLAGE=[4 x (src,t_in,max_src_secs,x)] (TL,TR,BL,BR) for the hook until the first cue, TAIL=secs after last word.
#          or HERO=(src,t_in,max_src_secs,x): one full-screen shot for the hook instead of the collage.
# Each cut lands LEAD s before its cue word. Shots fill their slot in order; a slot longer than the shots slows them
# (flagged if below 0.72x for 50/60 fps sources or 0.9x for 24-30 fps). Frame-exact: total frames == round(T*30).
import json,subprocess,os,sys
W=sys.argv[1]; sys.path.insert(0,W); import plan as P; os.chdir(W)
FPS=30; LEAD=getattr(P,'LEAD',0.10); words=json.load(open('words.json')); os.makedirs('seg',exist_ok=True)
def run(c): subprocess.run(c,check=True)
_pc={}
def probe(src):
    if src not in _pc:
        s=json.loads(subprocess.run(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height,r_frame_rate,color_transfer','-of','json',f'broll/{src}.mp4'],capture_output=True,text=True).stdout)['streams'][0]
        n,d=s['r_frame_rate'].split('/'); _pc[src]=(s['width'],s['height'],float(n)/float(d),s.get('color_transfer',''))
    return _pc[src]
def vf(src,x,wo,ho,ov=None):
    w,h,fps,tr=probe(src); o=dict(P.SRC.get(src,{})); o.update(ov or {}); c=o.get('cut',0.0); tp=o.get('top',0.0); ch=h*(1-c-tp); cw=ch*wo/ho
    if cw>w: cw=w; ch=cw*ho/wo
    Y=tp*h
    X=min(max(x*w-cw/2,0),w-cw)
    tm='zscale=tin=arib-std-b67:min=bt2020nc:pin=bt2020:t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p,' if tr=='arib-std-b67' else ''
    dl=''.join(f"delogo=x={int(a*w)}:y={int(b*h)}:w={int(c2*w)}:h={int(d*h)}," for a,b,c2,d in o.get('dl',[]))
    return f"{tm}{dl}crop={int(cw)//2*2}:{int(ch)//2*2}:{int(X)}:{int(Y)},scale={wo}:{ho}:flags=lanczos,setsar=1"
def shot(out,src,tin,nf,sp,x,wo=1080,ho=1920,ov=None):
    run(['ffmpeg','-y','-loglevel','error','-ss',f'{tin:.3f}','-t',f'{nf/FPS*sp+0.3:.3f}','-i',f'broll/{src}.mp4','-vf',vf(src,x,wo,ho,ov)+f',setpts=(PTS-STARTPTS)/{sp:.4f},fps={FPS}',
         '-frames:v',str(nf),'-an','-c:v','libx264','-preset','fast','-crf','16','-pix_fmt','yuv420p',out])
fr=lambda t: int(round(t*FPS))
T=words[-1][1]+P.TAIL; starts=[words[i][0]-LEAD for i,_ in P.CUES]+[T]; plan=[]
for ci,(i,shots) in enumerate(P.CUES):
    f0,f1=fr(starts[ci]),fr(starts[ci+1]); L=(f1-f0)/FPS; avail=sum(s[2] for s in shots)
    if avail>=L:
        alloc=[]; rem=L
        for s in shots:
            d=min(s[2],rem); alloc.append(d); rem-=d
            if rem<=1e-6: break
        if len(alloc)>1 and alloc[-1]<0.5: alloc[-2]+=alloc[-1]; alloc.pop()
        sp=[min(1.0,shots[k][2]/alloc[k]) for k in range(len(alloc))]
    else: s0=avail/L; alloc=[s[2]/s0 for s in shots]; sp=[s0]*len(shots)
    cur=f0
    for k,d in enumerate(alloc):
        nf=f1-cur if k==len(alloc)-1 else fr(d); src,tin,mx,x=shots[k][:4]; ov=shots[k][4] if len(shots[k])>4 else None
        flag='  <-- SLOW' if sp[k]<(0.72 if probe(src)[2]>45 else 0.9) else ''
        plan.append((cur,cur+nf,src,tin,sp[k],x,ov)); print(f'{cur/FPS:6.2f}-{(cur+nf)/FPS:6.2f}  w{i:<3d} {src[-6:]} @{tin:6.2f} x{sp[k]:.2f}{flag}'); cur+=nf
n0=fr(starts[0])
HERO=getattr(P,'HERO',None); OPEN=[HERO] if HERO else P.COLLAGE
if HERO:
    src,tin,mx,x=HERO[:4]; shot('seg/000.mp4',src,tin,n0,min(1.0,mx/(n0/FPS)),x,ov=HERO[4] if len(HERO)>4 else None)
else:
    for k,c in enumerate(P.COLLAGE): src,tin,mx,x=c[:4]; shot(f'seg/c{k}.mp4',src,tin,n0,min(1.0,mx/(n0/FPS)),x,540,960,c[4] if len(c)>4 else None)
    run(['ffmpeg','-y','-loglevel','error']+sum([['-i',f'seg/c{k}.mp4'] for k in range(4)],[])+['-filter_complex','[0:v][1:v][2:v][3:v]xstack=inputs=4:layout=0_0|540_0|0_960|540_960,format=yuv420p[v]','-map','[v]','-frames:v',str(n0),'-c:v','libx264','-preset','fast','-crf','16','seg/000.mp4'])
segs=['seg/000.mp4']
for j,(a,b,src,tin,sp,x,ov) in enumerate(plan): o=f'seg/{j+1:03d}.mp4'; shot(o,src,tin,b-a,sp,x,ov=ov); segs.append(o)
open('concat.txt','w').write(''.join(f"file '{os.path.abspath(s)}'\n" for s in segs))
run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i','concat.txt','-c','copy','video.mp4'])
shots=[{'start':round(a/FPS,3),'end':round(b/FPS,3),'src':src,'in':round(tin,3),'out':round(tin+(b-a)/FPS*sp,3)} for a,b,src,tin,sp,x,ov in plan]
collage=[{'src':c[0],'in':round(c[1],3),'out':round(c[1]+n0/FPS*min(1.0,c[2]/(n0/FPS)),3)} for c in OPEN]
json.dump({'T':T,'starts':starts,'cue_words':[i for i,_ in P.CUES],'collage_end':starts[0],'shots':shots,'collage':collage},open('timeline.json','w'))
print('video.mp4',round(T,2),'s, frames',n0+sum(p[1]-p[0] for p in plan),'expected',fr(T))
