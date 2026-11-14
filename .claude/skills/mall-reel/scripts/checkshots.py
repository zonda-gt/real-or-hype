# First / middle / last frame of every shot in edl.py, WITH the shot's crop applied, so you see exactly what will be on screen.
# Look for: burned-in subtitles or watermarks, letterbox bars, a different shot sneaking in, faces you must not show.
# usage (from project dir): python3 -I <skill>/scripts/checkshots.py [out.jpg]
import subprocess, io, sys, os
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.getcwd()); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from edl import shots
import gfx
out = sys.argv[1] if len(sys.argv) > 1 else 'shotcheck.jpg'
font = ImageFont.truetype(gfx.MONT, 16)
TW = 150; TH = int(TW * 16 / 9)
tiles = []
for s in shots():
    z, ay, ax = s['z'], s['ay'], s['ax']; cw, ch = TW / z, TH / z
    vf = f"scale={TW}:{TH}:force_original_aspect_ratio=increase,crop={TW}:{TH},crop={cw:.1f}:{ch:.1f}:{ax*(TW-cw):.1f}:{ay*(TH-ch):.1f},scale={TW}:{TH}"
    fr = []
    for t in [s['inn'] + 0.03, s['inn'] + s['dur'] / 2, s['inn'] + s['dur'] - 0.06]:
        r = subprocess.run(['ffmpeg', '-loglevel', 'error', '-ss', f'{t:.2f}', '-i', f"src/{s['src']}.mp4", '-frames:v', '1', '-vf', vf,
                            '-f', 'image2pipe', '-vcodec', 'png', '-'], capture_output=True)
        fr.append(Image.open(io.BytesIO(r.stdout)).convert('RGB') if r.stdout else Image.new('RGB', (TW, TH), 'red'))
    tiles.append((s, fr))
cols = 4; rows = (len(tiles) + cols - 1) // cols
img = Image.new('RGB', (cols * (TW * 3 + 8), rows * (TH + 22)), (20, 20, 20)); d = ImageDraw.Draw(img)
for k, (s, fr) in enumerate(tiles):
    x = (k % cols) * (TW * 3 + 8); y = (k // cols) * (TH + 22)
    for j, f in enumerate(fr): img.paste(f, (x + j * TW, y))
    d.text((x + 2, y + TH + 2), f"#{s['i']} {s['t0']:.2f} {s['src']}@{s['inn']} ({s['dur']:.2f})", fill='yellow', font=font)
img.save(out, quality=80); print(out, img.size)
