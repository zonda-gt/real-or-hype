"""Per-frame aesthetic metrics at full frame rate. usage: scorefr.py video.mp4 out.json
sharp = Laplacian variance (360px wide), bright = mean luma, clip = % pixels <8 or >248,
dx,dy = global motion (phase correlation, px/frame @360w), cut = histogram jump."""
import sys, json, subprocess, numpy as np, cv2
src, out = sys.argv[1], sys.argv[2]
w, h = map(int, subprocess.run(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height','-of','csv=p=0',src],capture_output=True,text=True).stdout.strip().split(',')[:2])
fps = eval(subprocess.run(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=r_frame_rate','-of','csv=p=0',src],capture_output=True,text=True).stdout.strip())
W = 360; H = int(h * W / w) // 2 * 2
p = subprocess.Popen(['ffmpeg','-v','error','-i',src,'-an','-vf',f'scale={W}:{H}','-f','rawvideo','-pix_fmt','gray','-'], stdout=subprocess.PIPE)
prev = None; prevh = None; rows = []; win = np.outer(cv2.createHanningWindow((W, H), cv2.CV_32F).T.T, 1) if False else cv2.createHanningWindow((W, H), cv2.CV_32F)
while True:
    b = p.stdout.read(W * H)
    if len(b) < W * H: break
    g = np.frombuffer(b, np.uint8).reshape(H, W)
    f = g.astype(np.float32)
    sharp = float(cv2.Laplacian(g, cv2.CV_64F).var())
    bright = float(g.mean()); clip = float(((g < 8) | (g > 248)).mean() * 100)
    hist = cv2.calcHist([g], [0], None, [32], [0, 256]).ravel(); hist /= hist.sum()
    if prev is not None:
        (dx, dy), _ = cv2.phaseCorrelate(prev, f, win)
        cut = float(0.5 * np.abs(hist - prevh).sum())
    else:
        dx = dy = 0.0; cut = 1.0
    rows.append([round(sharp, 1), round(bright, 1), round(clip, 2), round(dx, 2), round(dy, 2), round(cut, 3)])
    prev = f; prevh = hist
json.dump({'fps': fps, 'w': w, 'h': h, 'cols': ['sharp', 'bright', 'clip', 'dx', 'dy', 'cut'], 'rows': rows}, open(out, 'w'))
print(src, len(rows), 'frames')
