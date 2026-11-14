# Render every text style onto real frames so you can compare with reference/style_frames.jpg BEFORE a full render.
# usage (from project dir): python3 -I <skill>/scripts/stylecheck.py out/stylecheck.jpg [video_or_image ...]
# With no inputs it uses frames from src/ clips named in edl.py. Uses edl.TITLE / LABELS / PILLS text when present.
import sys, os, subprocess, io
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.getcwd())
import gfx
from gfx import W, H
out = sys.argv[1] if len(sys.argv) > 1 else 'stylecheck.jpg'
try:
    import edl; title = edl.TITLE[:3]; labels = [l[2] for l in edl.LABELS] or ['silo rooftop']; pills = edl.PILLS[0][2] if edl.PILLS else ['Metro Line 11', 'Longyao Rd · Exit 4']
    srcs = [f"src/{e[1]}.mp4@{e[2]+0.3}" for e in edl.EDL[:1]] + [f"src/{e[1]}.mp4@{e[2]+0.3}" for e in edl.EDL[len(edl.EDL)//3:len(edl.EDL)//3+1]] + [f"src/{e[1]}.mp4@{e[2]+0.3}" for e in edl.EDL[-1:]]
except Exception:
    title = ('GATE M', 'West Bund Dream Center', 'in  Shanghai'); labels = ['silo rooftop']; pills = ['Metro Line 11', 'Longyao Rd · Exit 4']; srcs = []
srcs = sys.argv[2:] or srcs

def frame(spec):
    if spec and spec.lower().endswith(('.jpg', '.png')): return Image.open(spec).convert('RGBA').resize((W, H))
    if spec:
        p, _, t = spec.partition('@')
        r = subprocess.run(['ffmpeg', '-v', 'error', '-ss', t or '1', '-i', p, '-frames:v', '1', '-vf',
                            f'scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}', '-f', 'image2pipe', '-vcodec', 'png', '-'], capture_output=True)
        if r.stdout: return Image.open(io.BytesIO(r.stdout)).convert('RGBA')
    return Image.new('RGBA', (W, H), (90, 110, 130, 255))

f1, f2, f3 = (frame(s) for s in (srcs + [None] * 3)[:3])
t = gfx.title_img(*title); f1.alpha_composite(t, ((W - t.width) // 2, -42))
c = gfx.word_img('biggest'); f1.alpha_composite(c, ((W - c.width) // 2, gfx.CAPTION_Y - c.height // 2))
l = gfx.label_img(labels[0], -4); f2.alpha_composite(l, (540 - l.width // 2, 560 - l.height // 2))
c = gfx.word_img('rooftop'); f2.alpha_composite(c, ((W - c.width) // 2, gfx.CAPTION_Y - c.height // 2))
p = gfx.pill_img(pills); f3.alpha_composite(p, ((W - p.width) // 2, 520))
fo = gfx.follow_img(); f3.alpha_composite(fo, ((W - fo.width) // 2, gfx.FOLLOW_Y))
sheet = Image.new('RGB', (W * 3 // 2, H // 2))
for i, fr in enumerate((f1, f2, f3)): sheet.paste(fr.convert('RGB').resize((W // 2, H // 2)), (i * W // 2, 0))
d = ImageDraw.Draw(sheet)
for i, n in enumerate(['title + caption', 'label + caption', 'info pill + follow']): d.text((i * W // 2 + 8, 8), n, fill='yellow')
sheet.save(out, quality=88); print(out)
