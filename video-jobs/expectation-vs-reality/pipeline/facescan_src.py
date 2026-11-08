import sys,cv2,os
S=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
det=None
for i in sys.argv[1:]:
    cap=cv2.VideoCapture(f'{S}/media/dy/{i}.mp4'); fps=cap.get(cv2.CAP_PROP_FPS); k=0; per={}
    while True:
        ok,fr=cap.read()
        if not ok: break
        # emulate final crop to 9:16 cover
        h,w=fr.shape[:2]
        if w/h>9/16: nw=int(h*9/16); fr=fr[:, (w-nw)//2:(w-nw)//2+nw]
        else: nh=int(w*16/9); fr=fr[(h-nh)//2:(h-nh)//2+nh]
        sm=cv2.resize(fr,(540,960))
        if det is None: det=cv2.FaceDetectorYN.create(f'{S}/face_yunet.onnx','',(540,960),0.6,0.3,5000)
        _,f=det.detect(sm); m=0 if f is None else max(x[3] for x in f)/960
        s=int(k/fps*2)/2; per[s]=max(per.get(s,0),m); k+=1
    print(i,' '.join(f"{s:.1f}:{'#' if v>0.06 else ('+' if v>0.04 else '.')}" for s,v in sorted(per.items())))
