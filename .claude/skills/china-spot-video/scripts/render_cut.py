# Cut picture to the narration. usage: render_cut.py <workdir>
# plan.py: SRC={id:{'cut':frac_of_height_to_drop_at_bottom}}, CUES=[(word_idx,[(src,t_in,max_src_secs,x_centre),...]),...],
#          COLLAGE=[4 x (src,t_in,max_src_secs,x)] (TL,TR,BL,BR) for the hook until the first cue, TAIL=secs after last word.
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
def vf(src,x,wo,ho):
    w,h,fps,tr=probe(src); c=P.SRC.get(src,{}).get('cut',0.0); ch=h*(1-c); cw=ch*wo/ho
    if cw>w: cw=w; ch=cw*ho/wo
    X=min(max(x*w-cw/2,0),w-cw)
    tm='zscale=tin=arib-std-b67:min=bt2020nc:pin=bt2020:t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p,' if tr=='arib-std-b67' else ''
    return f"{tm}crop={int(cw)//2*2}:{int(ch)//2*2}:{int(X)}:0,scale={wo}:{ho}:flags=lanczos,setsar=1"
def shot(out,src,tin,nf,sp,x,wo=1080,ho=1920):
    run(['ffmpeg','-y','-loglevel','error','-ss',f'{tin:.3f}','-t',f'{nf/FPS*sp+0.3:.3f}','-i',f'broll/{src}.mp4','-vf',vf(src,x,wo,ho)+f',setpts=(PTS-STARTPTS)/{sp:.4f},fps={FPS}',
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
        nf=f1-cur if k==len(alloc)-1 else fr(d); src,tin,mx,x=shots[k]
        flag='  <-- SLOW' if sp[k]<(0.72 if probe(src)[2]>45 else 0.9) else ''
        plan.append((cur,cur+nf,src,tin,sp[k],x)); print(f'{cur/FPS:6.2f}-{(cur+nf)/FPS:6.2f}  w{i:<3d} {src[-6:]} @{tin:6.2f} x{sp[k]:.2f}{flag}'); cur+=nf
n0=fr(starts[0])
for k,(src,tin,mx,x) in enumerate(P.COLLAGE): shot(f'seg/c{k}.mp4',src,tin,n0,min(1.0,mx/(n0/FPS)),x,540,960)
run(['ffmpeg','-y','-loglevel','error']+sum([['-i',f'seg/c{k}.mp4'] for k in range(4)],[])+['-filter_complex','[0:v][1:v][2:v][3:v]xstack=inputs=4:layout=0_0|540_0|0_960|540_960,format=yuv420p[v]','-map','[v]','-frames:v',str(n0),'-c:v','libx264','-preset','fast','-crf','16','seg/000.mp4'])
segs=['seg/000.mp4']
for j,(a,b,src,tin,sp,x) in enumerate(plan): o=f'seg/{j+1:03d}.mp4'; shot(o,src,tin,b-a,sp,x); segs.append(o)
open('concat.txt','w').write(''.join(f"file '{os.path.abspath(s)}'\n" for s in segs))
run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i','concat.txt','-c','copy','video.mp4'])
json.dump({'T':T,'starts':starts,'cue_words':[i for i,_ in P.CUES],'collage_end':starts[0]},open('timeline.json','w'))
print('video.mp4',round(T,2),'s, frames',n0+sum(b-a for a,b,*_ in plan),'expected',fr(T))
