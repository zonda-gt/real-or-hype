"""OCR EVERY frame of a video. usage: qa_ocr.py video.mp4 out.json [width]
Writes per-frame detections; prints a summary (frames with text, unique strings)."""
import sys, json, subprocess, numpy as np, collections
from rapidocr_onnxruntime import RapidOCR
src, out = sys.argv[1], sys.argv[2]; tw = int(sys.argv[3]) if len(sys.argv) > 3 else 720
w, h = map(int, subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height',
                               '-of', 'csv=p=0', src], capture_output=True, text=True).stdout.strip().split(',')[:2])
th = int(h * tw / w) // 2 * 2; sc = w / tw
p = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', src, '-an', '-vf', f'scale={tw}:{th}', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-'],
                     stdout=subprocess.PIPE)
eng = RapidOCR(); res = []; i = 0; fsz = tw * th * 3
while True:
    buf = p.stdout.read(fsz)
    if len(buf) < fsz: break
    f = np.frombuffer(buf, np.uint8).reshape(th, tw, 3)
    r, _ = eng(f)
    boxes = []
    for b, t, s in (r or []):
        xs = [q[0] for q in b]; ys = [q[1] for q in b]
        boxes.append([round(min(xs) * sc), round(min(ys) * sc), round(max(xs) * sc), round(max(ys) * sc), t, round(float(s), 2)])
    res.append(boxes); i += 1
json.dump({'w': w, 'h': h, 'frames': res}, open(out, 'w'), ensure_ascii=False)
withtext = sum(1 for b in res if b)
c = collections.Counter(t for b in res for (_, _, _, _, t, _) in b)
print(f'{src}: {i} frames OCR\'d, {withtext} with text, {len(c)} unique strings')
for t, n in c.most_common(400): print(f'  {n:4d}  {t}')
