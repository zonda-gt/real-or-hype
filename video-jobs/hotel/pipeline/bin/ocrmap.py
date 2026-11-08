"""OCR a video at N fps -> ocr/<name>.json: [{t, boxes:[[x0,y0,x1,y1,text,score]]}] in source pixel coords.
usage: ocrmap.py video.mp4 fps [maxw]"""
import sys,os,json,subprocess,numpy as np
from rapidocr_onnxruntime import RapidOCR
src=sys.argv[1]; fps=float(sys.argv[2]); maxw=int(sys.argv[3]) if len(sys.argv)>3 else 720
w,h=map(int,subprocess.run(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height','-of','csv=p=0',src],capture_output=True,text=True).stdout.strip().split(',')[:2])
sc=min(1.0,maxw/max(w,h)); W,H=int(w*sc)//2*2,int(h*sc)//2*2
raw=subprocess.run(['ffmpeg','-v','error','-i',src,'-an','-vf',f'fps={fps},scale={W}:{H}','-f','rawvideo','-pix_fmt','bgr24','-'],capture_output=True).stdout
fr=np.frombuffer(raw,np.uint8).reshape(-1,H,W,3)
eng=RapidOCR()
out=[]
for i,f in enumerate(fr):
    res,_=eng(f)
    boxes=[]
    for b,txt,s in (res or []):
        xs=[p[0] for p in b]; ys=[p[1] for p in b]
        boxes.append([min(xs)/sc,min(ys)/sc,max(xs)/sc,max(ys)/sc,txt,round(float(s),2)])
    out.append({'t':round(i/fps,3),'boxes':boxes})
os.makedirs('ocr',exist_ok=True)
name=os.path.splitext(os.path.basename(src))[0]
json.dump({'w':w,'h':h,'fps':fps,'frames':out},open(f'ocr/{name}.json','w'),ensure_ascii=False)
print(name,w,h,len(out),'frames', sum(1 for o in out if o['boxes']),'with text')
