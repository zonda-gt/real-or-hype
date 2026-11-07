# usage: prep2.py plan.json outpublic edl_out.json
# plan: [{id, src, tin, tout, speed, matte, plate}]  -> {id}_base.mp4, {id}_cut.webm, {id}_a.wav, {id}_plate.jpg + edl with word frames
import json,subprocess,sys,os,numpy as np,cv2
from PIL import Image,ImageFilter
PLAN=json.load(open(sys.argv[1])); PUB=sys.argv[2]; FPS=24; W,H=720,1280
SES=None
def ses():
    global SES
    if SES is None:
        from rembg import new_session; SES=new_session('u2net_human_seg')
    return SES
edl=[]
for s in PLAN:
    i,src,tin,tout,sp=s['id'],s['src'],s['tin'],s['tout'],s.get('speed',1.0)
    vf=f'trim={tin}:{tout},setpts=(PTS-STARTPTS)/{sp},scale=-2:1280,crop=720:1280,fps={FPS}'
    base=f'{PUB}/{i}_base.mp4'
    subprocess.run(['ffmpeg','-loglevel','error','-y','-i',src,'-vf',vf,'-an','-c:v','libx264','-crf','16','-pix_fmt','yuv420p',base],check=True)
    n=int(subprocess.run(['ffprobe','-v','error','-count_frames','-select_streams','v:0','-show_entries','stream=nb_read_frames','-of','csv=p=0',base],capture_output=True,text=True).stdout.strip())
    dur=n/FPS
    af=f'atrim={tin}:{tout},asetpts=PTS-STARTPTS,atempo={sp},highpass=f=80,loudnorm=I=-16:TP=-2:LRA=11,afade=t=in:d=0.02,areverse,afade=t=in:d=0.05,areverse,apad'
    subprocess.run(['ffmpeg','-loglevel','error','-y','-i',src,'-af',af,'-t',f'{dur:.3f}','-ar','48000','-ac','2',f'{PUB}/{i}_a.wav'],check=True)
    words=[]
    if os.path.exists(src+'.json'):
        for seg in json.load(open(src+'.json')):
            for (a,b,w) in seg['w']:
                if tin-0.05<=a<tout: words.append({'w':w.strip(),'f':max(0,round((a-tin)/sp*FPS)),'e':round((min(b,tout)-tin)/sp*FPS)})
    FIX={'roots,':'routes,','roots':'routes'}
    mw=[]
    for x in words:
        x['w']=FIX.get(x['w'],x['w'])
        if x['w'].startswith('-') and mw: mw[-1]['w']+=x['w']; mw[-1]['e']=x['e']
        else: mw.append(x)
    words=mw
    if s.get('matte'):
        p=subprocess.Popen(['ffmpeg','-loglevel','error','-i',base,'-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
        w=subprocess.Popen(['ffmpeg','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgba','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libvpx-vp9','-pix_fmt','yuva420p','-b:v','4M','-auto-alt-ref','0',f'{PUB}/{i}_cut.webm'],stdin=subprocess.PIPE)
        from rembg import remove
        prev=None; k=0
        while True:
            b=p.stdout.read(W*H*3)
            if len(b)<W*H*3: break
            fr=Image.frombytes('RGB',(W,H),b); m=np.asarray(remove(fr,session=ses(),only_mask=True)).astype(np.float32)
            prev=m if prev is None else 0.55*m+0.45*prev
            mk=Image.fromarray(np.clip(prev,0,255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))
            if s.get('plate') and k==0:
                mm=cv2.dilate((np.asarray(mk)>40).astype(np.uint8)*255,np.ones((41,41),np.uint8))
                Image.fromarray(cv2.inpaint(np.asarray(fr),mm,12,cv2.INPAINT_TELEA)).filter(ImageFilter.GaussianBlur(3)).save(f'{PUB}/{i}_plate.jpg',quality=92)
            rgba=fr.copy(); rgba.putalpha(mk); w.stdin.write(rgba.tobytes()); k+=1
        w.stdin.close(); w.wait()
    edl.append({'id':i,'frames':n,'words':words}); print(i,n,'frames',' '.join(f"{x['w']}@{x['f']}" for x in words),flush=True)
old={e['id']:e for e in (json.load(open(sys.argv[3])) if os.path.exists(sys.argv[3]) else [])}
for e in edl: old[e['id']]=e
json.dump(list(old.values()),open(sys.argv[3],'w'),indent=0)
