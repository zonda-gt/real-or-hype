#!/usr/bin/env python3
# qa.py video.mp4 out.json [--ocr] [--faces]  : checks EVERY frame. faces: YuNet; OCR: RapidOCR (zh+en)
import sys,json,cv2,numpy as np,os
v=sys.argv[1]; out=sys.argv[2]; do_ocr='--ocr' in sys.argv; do_face='--faces' in sys.argv
S=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cap=cv2.VideoCapture(v); fps=cap.get(cv2.CAP_PROP_FPS); n=int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
det=cv2.FaceDetectorYN.create(f'{S}/face_yunet.onnx','',(540,960),0.6,0.3,5000) if do_face else None
if do_ocr:
    from rapidocr_onnxruntime import RapidOCR
    ocr=RapidOCR()
res=[];i=0
while True:
    ok,fr=cap.read()
    if not ok: break
    r={'f':i,'t':round(i/fps,3)}
    if do_face:
        sm=cv2.resize(fr,(540,960)); _,faces=det.detect(sm)
        fs=[] if faces is None else [[round(float(x),1) for x in f[:4]]+[round(float(f[-1]),2)] for f in faces]
        r['faces']=fs; r['maxface']=max([f[3]/960 for f in fs],default=0)
    if do_ocr:
        sm=cv2.resize(fr,(720,1280)); o,_=ocr(sm)
        r['text']=[(t,round(float(c),2),[int(min(p[0] for p in b)),int(min(p[1] for p in b)),int(max(p[0] for p in b)),int(max(p[1] for p in b))]) for b,t,c in (o or [])]
    res.append(r); i+=1
json.dump({'video':v,'fps':fps,'frames':i,'res':res},open(out,'w'),ensure_ascii=False)
print(v,'frames checked',i)
if do_face:
    big=[r for r in res if r['maxface']>0.06]
    print('frames with face >6% of frame height:',len(big))
    import itertools
    for k,g in itertools.groupby(big,key=lambda r:int(r['t'])): g=list(g); print(f"  t~{k}s: {len(g)} frames, max {max(x['maxface'] for x in g):.3f}")
if do_ocr:
    tx=[r for r in res if r['text']]
    print('frames with any detected text:',len(tx))
