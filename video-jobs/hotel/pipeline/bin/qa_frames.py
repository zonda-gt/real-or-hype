"""Every-frame visual QA of a final video + 4 fps review pages.
usage: qa_frames.py video.mp4 outdir
- per frame (30 fps): sharpness (Laplacian var), brightness, flash/black detection, cut detection
- flags: BLACK (mean<12), FLASH (brightness jumps >35 and back within 3 frames), BLUR_DIP (sharpness <45% of the
  median of its own shot), MICRO_SHOT (shot shorter than 0.4 s)
- writes outdir/qa.json and review pages outdir/page_XX.jpg (4 fps, 8x5 per page, time-stamped)"""
import sys, os, json, subprocess, numpy as np, cv2
src, od = sys.argv[1], sys.argv[2]; os.makedirs(od, exist_ok=True)
W, H = 270, 480
p = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', src, '-an', '-vf', f'scale={W}:{H}', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-'], stdout=subprocess.PIPE)
frames = []; sharp = []; bright = []; hd = []; prevh = None
while True:
    b = p.stdout.read(W * H * 3)
    if len(b) < W * H * 3: break
    f = np.frombuffer(b, np.uint8).reshape(H, W, 3); g = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
    sharp.append(float(cv2.Laplacian(g, cv2.CV_64F).var())); bright.append(float(g.mean()))
    h = cv2.calcHist([g], [0], None, [32], [0, 256]).ravel(); h /= h.sum()
    hd.append(0.0 if prevh is None else float(0.5 * np.abs(h - prevh).sum())); prevh = h
    frames.append(f)
n = len(frames); fps = 30.0
sharp = np.array(sharp); bright = np.array(bright); hd = np.array(hd)
cuts = [0] + [i for i in range(1, n) if hd[i] > 0.22] + [n]
flags = []
for i in range(n):
    if bright[i] < 12: flags.append((round(i / fps, 3), 'BLACK', round(bright[i], 1)))
for i in range(1, n - 3):
    if bright[i] - bright[i - 1] > 35 and any(abs(bright[i + k] - bright[i - 1]) < 10 for k in (1, 2, 3)):
        flags.append((round(i / fps, 3), 'FLASH', round(bright[i] - bright[i - 1], 1)))
shots = []
for a, b in zip(cuts[:-1], cuts[1:]):
    if b - a < 1: continue
    med = float(np.median(sharp[a:b])); shots.append((round(a / fps, 2), round((b - a) / fps, 2), round(med)))
    if (b - a) / fps < 0.4 and a > 0: flags.append((round(a / fps, 3), 'MICRO_SHOT', round((b - a) / fps, 2)))
    for i in range(a, b):
        if sharp[i] < 0.45 * med: flags.append((round(i / fps, 3), 'BLUR_DIP', round(sharp[i] / med, 2)))
# collapse consecutive flags of same type
col = []
for t, k, v in flags:
    if col and col[-1][1] == k and t - col[-1][0] - col[-1][3] <= 1 / fps + 1e-6:
        col[-1][3] = round(t - col[-1][0], 3)
    else: col.append([t, k, v, 0.0])
json.dump({'frames': n, 'shots': shots, 'flags': col}, open(f'{od}/qa.json', 'w'), indent=0)
# 4 fps review pages
idx = list(range(0, n, int(fps / 4)))
per = 40; pg = 0
for s in range(0, len(idx), per):
    tiles = []
    for i in idx[s:s + per]:
        t = frames[i].copy(); cv2.putText(t, f'{i / fps:.2f}', (6, 26), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2); tiles.append(t)
    while len(tiles) % 8: tiles.append(np.zeros_like(frames[0]))
    rows = [np.hstack(tiles[k:k + 8]) for k in range(0, len(tiles), 8)]
    cv2.imwrite(f'{od}/page_{pg:02d}.jpg', np.vstack(rows), [cv2.IMWRITE_JPEG_QUALITY, 82]); pg += 1
print(f'{src}: {n} frames, {len(shots)} shots, {len(col)} flags, {pg} review pages')
for f in col: print('  ', f)
