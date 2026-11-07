# trimmed base clips (mp4) + presenter cut-out (VP9 alpha webm) for Remotion; same in/out as v1
import subprocess,sys,numpy as np,cv2
from PIL import Image,ImageFilter
from rembg import remove,new_session
SES=new_session('u2net_human_seg'); W,H=720,1280
SEGS=[('01','sd/shots/01_couchwall.mp4',0.0,4.5,1),('02','sd/shots/02_orbit.mp4',0.9,3.95,1),('03','sd/shots/03_vertigo.mp4',0.0,3.4,1),
('04','sd/shots/04_uiworld.mp4',1.4,2.45,0),('05','sd/shots/05_checklist.mp4',1.85,3.15,0),('06','sd/shots/06_pullback.mp4',0.0,4.75,0),
('07','sd/shots/07_route.mp4',0.0,4.6,1),('08','sd/shots/08_cafe.mp4',0.3,2.0,0),('09','sd/shots/09_cover.mp4',1.55,2.05,1),('10','sd/shots/10_framebreak.mp4',0.0,5.85,1)]
VF='scale=-2:1280,crop=720:1280,fps=24'
for n,src,tin,dur,needm in SEGS:
    subprocess.run(['ffmpeg','-loglevel','error','-y','-ss',str(tin),'-t',str(dur),'-i',src,'-vf',VF,'-an','-c:v','libx264','-crf','16','-pix_fmt','yuv420p',f'rm/public/base_{n}.mp4'],check=True)
    if not needm: continue
    p=subprocess.Popen(['ffmpeg','-loglevel','error','-ss',str(tin),'-t',str(dur),'-i',src,'-vf',VF,'-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
    w=subprocess.Popen(['ffmpeg','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgba','-s',f'{W}x{H}','-r','24','-i','-','-c:v','libvpx-vp9','-pix_fmt','yuva420p','-b:v','4M','-auto-alt-ref','0',f'rm/public/cut_{n}.webm'],stdin=subprocess.PIPE)
    prev=None; k=0
    while True:
        b=p.stdout.read(W*H*3)
        if len(b)<W*H*3: break
        fr=Image.frombytes('RGB',(W,H),b); m=np.asarray(remove(fr,session=SES,only_mask=True)).astype(np.float32)
        prev=m if prev is None else 0.55*m+0.45*prev
        mk=Image.fromarray(np.clip(prev,0,255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))
        if n=='03' and k==0:
            mm=(np.asarray(mk)>40).astype(np.uint8)*255; mm=cv2.dilate(mm,np.ones((41,41),np.uint8))
            Image.fromarray(cv2.inpaint(np.asarray(fr),mm,12,cv2.INPAINT_TELEA)).filter(ImageFilter.GaussianBlur(3)).save('rm/public/plate_03.jpg',quality=92)
        rgba=fr.copy(); rgba.putalpha(mk); w.stdin.write(rgba.tobytes()); k+=1
    w.stdin.close(); w.wait(); print(n,k,flush=True)
