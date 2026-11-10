# Composite "CHINA VLOG" behind the skyline on seg00 (text pops in at 0.567 s like the reference).
import sys, os, subprocess, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image
here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(here, '..', 'tools'))
import title
from skymask import sky_prob
FPS = 30; START = round(0.567 * FPS)
import importlib; P = importlib.import_module(os.environ.get('PLAN', 'plan_v')); SEG = os.environ.get('SEGDIR', 'segs_v')
src = f'{here}/{SEG}/seg00.mp4'; fdir = f'{here}/title_frames_{SEG}'; os.makedirs(fdir, exist_ok=True)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src, f'{fdir}/f%03d.png'], check=True)
files = sorted(f for f in os.listdir(fdir) if f.startswith('f'))
Y0, Y1, SQ, XC, XV = getattr(P, 'TITLE', (230, 590, 0.48, 565, 1055))
wc = title.word_width('CHINA', Y1 - Y0, SQ); wv = title.word_width('VLOG', Y1 - Y0, SQ)
al, col = title.words_layer(1080, 1920, ['CHINA', 'VLOG'], Y0, Y1, [XC - wc, XV - wv], SQ)
# sky probability per frame, then temporal smoothing (3-frame average) to avoid flicker
probs = {}
for n, f in enumerate(files):
    if n < START - 1: continue
    probs[n] = np.asarray(sky_prob(Image.open(f'{fdir}/{f}').convert('RGB'), title.MODEL), np.float32) / 255
    print('mask', n, flush=True)
for n, f in enumerate(files):
    fr = np.asarray(Image.open(f'{fdir}/{f}').convert('RGB'))
    if n >= START:
        ks = [m for m in (n - 1, n, n + 1) if m in probs]
        sky = sum(probs[m] for m in ks) / len(ks)
        fr, _ = title.composite(fr, al, col, sky=sky)
    Image.fromarray(fr).save(f'{fdir}/o{n+1:03d}.png')
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', str(FPS), '-i', f'{fdir}/o%03d.png', '-c:v', 'libx264', '-crf', '14',
                '-pix_fmt', 'yuv420p', f'{here}/{SEG}/seg00_title.mp4'], check=True)
print('done')
