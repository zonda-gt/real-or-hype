# usage: mpmatte.py in.mp4 out_alpha.mkv [start dur]
import sys,subprocess,numpy as np,cv2,time,mediapipe as mp
from mediapipe.tasks.python import vision,BaseOptions
src,out=sys.argv[1],sys.argv[2]; ss=sys.argv[3] if len(sys.argv)>3 else '0'; dur=sys.argv[4] if len(sys.argv)>4 else None
M=sys.argv[0].rsplit('/',2)[0]+'/models/selfie_multiclass_256x256.tflite'
W,H=1080,1920
seg=vision.ImageSegmenter.create_from_options(vision.ImageSegmenterOptions(base_options=BaseOptions(model_asset_path=M),output_confidence_masks=True,running_mode=vision.RunningMode.VIDEO))
rd=subprocess.Popen(['ffmpeg','-loglevel','error','-ss',ss,'-i',src]+(['-t',dur] if dur else [])+['-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
wr=subprocess.Popen(['ffmpeg','-loglevel','error','-y','-f','rawvideo','-pix_fmt','gray','-s',f'{W}x{H}','-r','30','-i','-','-c:v','ffv1',out],stdin=subprocess.PIPE)
n=0;t=time.time();prev=None
while True:
    b=rd.stdout.read(W*H*3)
    if len(b)<W*H*3:break
    f=np.frombuffer(b,np.uint8).reshape(H,W,3)
    # segment on a 540x960 copy (model is 256 internally), upscale its soft mask
    small=cv2.resize(f,(540,960),interpolation=cv2.INTER_AREA)
    r=seg.segment_for_video(mp.Image(image_format=mp.ImageFormat.SRGB,data=np.ascontiguousarray(small)),int(n*1000/30))
    bg=r.confidence_masks[0].numpy_view().astype(np.float32)
    a=cv2.resize(1-bg,(W,H),interpolation=cv2.INTER_LINEAR)
    # edge refinement guided by the full-res frame (keeps hair strands, glasses edges)
    g=cv2.cvtColor(f,cv2.COLOR_RGB2GRAY).astype(np.float32)/255
    a=cv2.ximgproc.guidedFilter(guide=g,src=a,radius=6,eps=1e-3)
    a=np.clip((a-0.08)/0.84,0,1)
    if prev is not None: a=0.6*a+0.4*prev   # light temporal smoothing against flicker
    prev=a
    wr.stdin.write((a*255).astype(np.uint8).tobytes()); n+=1
    if n%300==0: print(n,f'{n/(time.time()-t):.1f} fps',flush=True)
wr.stdin.close();wr.wait();print('done',n,f'{n/(time.time()-t):.1f} fps')
