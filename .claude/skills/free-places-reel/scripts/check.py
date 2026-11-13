"""0.2 s frame sheet of chosen shot windows: check.py PLAN RAWDIR OUT.jpg [i,j,k (0-based)]"""
import sys, subprocess, io
sys.path.insert(0, __import__('os').path.dirname(__file__)); from common import CUTS, load_plan
from PIL import Image, ImageDraw, ImageFont
P = load_plan(sys.argv[1]); RAW = sys.argv[2]; out = sys.argv[3]
sel = [int(x) for x in sys.argv[4].split(',')] if len(sys.argv) > 4 else range(22)
TW, TH = 144, 256; font = ImageFont.load_default(size=16); rows = []
for i in sel:
    clip, t0, lab = P['shots'][i]; d = (CUTS[i+1]-CUTS[i]) * P['speed'].get(i, 1)
    r = subprocess.run(['ffmpeg', '-loglevel', 'error', '-ss', str(t0), '-t', f'{d:.3f}', '-i', f'{RAW}/{clip}.mp4', '-vf',
        f'fps=5,scale={TW}:{TH}:force_original_aspect_ratio=decrease,pad={TW}:{TH}:(ow-iw)/2:(oh-ih)/2', '-f', 'image2pipe', '-vcodec', 'png', '-'], capture_output=True)
    data = r.stdout; ims = []
    while data:
        e = data.find(b'IEND') + 8; ims.append(Image.open(io.BytesIO(data[:e])).convert('RGB')); data = data[e:]
    rows.append((i, clip, t0, d, ims))
N = max(len(r[4]) for r in rows)
sh = Image.new('RGB', (TW*N, (TH+20)*len(rows)), 'black'); dr = ImageDraw.Draw(sh)
for k, (i, clip, t0, d, ims) in enumerate(rows):
    y = k*(TH+20); dr.text((2, y+1), f'#{i+1} {clip} @{t0} {d:.2f}s', fill='yellow', font=font)
    for j, im in enumerate(ims): sh.paste(im, (j*TW, y+20))
sh.save(out, quality=82); print(sh.size)
