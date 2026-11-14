# Render a mall-reel project. Run from the project dir:  python3 -I <skill>/scripts/render.py
# Needs: edl.py (see templates/edl_template.py), src/<clip>.mp4, vo/narr.wav, vo/words.json, the music file named in edl.MUSIC.
# Writes: segs/, out/base.mp4, out/gfx.mp4, out/mix.wav, out/final_1080.mp4, out/final_540.mp4
import subprocess, json, os, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.getcwd())
import gfx
from gfx import W, H
import edl

FPS = 30
LEAD = 0.07   # every cut lands 0.07 s (2 frames) before the word onset it belongs to
os.makedirs('segs', exist_ok=True); os.makedirs('out', exist_ok=True)
def run(cmd): subprocess.run(cmd, check=True)

# ---------- 1. one segment per shot ----------
S = edl.shots()
bounds = [0] + [round((s['t0'] - LEAD) * FPS) for s in S[1:]] + [round(edl.END * FPS)]
seglist = []
for k, s in enumerate(S):
    n = bounds[k + 1] - bounds[k]
    z, ay, ax = s['z'], s['ay'], s['ax']
    cw, ch = W / z, H / z
    # fill 9:16 (centre-crop other aspects), then the per-shot zoom crop (removes burned-in text / letterbox bars)
    vf = (f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},setsar=1,"
          f"crop={cw:.1f}:{ch:.1f}:{ax*(W-cw):.1f}:{ay*(H-ch):.1f},scale={W}:{H}:flags=lanczos,"
          f"fps={FPS},unsharp=5:5:0.4,tpad=stop_mode=clone:stop_duration=1")
    out = f"segs/s{k:02d}.mp4"
    # in-point used exactly as chosen: shifting it can expose frames of the previous source shot
    run(['ffmpeg', '-v', 'error', '-y', '-ss', f"{s['inn']:.3f}", '-i', f"src/{s['src']}.mp4", '-vf', vf,
         '-frames:v', str(n), '-an', '-c:v', 'libx264', '-preset', 'medium', '-crf', '14', '-pix_fmt', 'yuv420p', out])
    seglist.append(out)
with open('segs/list.txt', 'w') as f:
    for p in seglist: f.write(f"file '{os.path.basename(p)}'\n")
run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', 'segs/list.txt', '-c', 'copy', 'out/base.mp4'])
NF = bounds[-1]

# ---------- 2. graphics ----------
def at(t): return round((t - LEAD) * FPS)
words = json.load(open('vo/words.json'))
items = []   # (start_frame, end_frame, image, x, y, anim)
a, b, c, t0, t1 = edl.TITLE
title = gfx.title_img(a, b, c)
items.append((round(t0 * FPS), round(t1 * FPS), title, (W - title.width) // 2, -42, 'fadeout'))
REPL = getattr(edl, 'CAPTION_REPLACE', {})
for i, (w, wa, wb) in enumerate(words):          # one word on screen at a time
    s0 = max(0, round(wa * FPS) - 2)              # 2 frames before the word starts
    nxt = words[i + 1][1] if i + 1 < len(words) else wb + 0.3
    e0 = round(min(nxt, wb + 0.6) * FPS) - 2      # until the next word (max 0.6 s after this one ends)
    im = gfx.word_img(w, REPL)
    items.append((s0, max(s0 + 3, e0), im, (W - im.width) // 2, gfx.CAPTION_Y - im.height // 2, None))
for la, lb, txt, cx, cy, ang in edl.LABELS:
    im = gfx.label_img(txt, ang); items.append((at(la), at(lb), im, cx - im.width // 2, cy - im.height // 2, 'pop'))
for pa, pb, lines, py in edl.PILLS:
    im = gfx.pill_img(lines); items.append((at(pa), at(pb), im, (W - im.width) // 2, py, 'pop'))
fa, fb = edl.FOLLOW
fol = gfx.follow_img()
items.append((at(fa), NF if fb is None else at(fb), fol, (W - fol.width) // 2, gfx.FOLLOW_Y, 'pop'))

dec = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', 'out/base.mp4', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-'], stdout=subprocess.PIPE)
enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                        '-c:v', 'libx264', '-preset', 'medium', '-crf', '15', '-pix_fmt', 'yuv420p', 'out/gfx.mp4'], stdin=subprocess.PIPE)
f = 0
while True:
    buf = dec.stdout.read(W * H * 4)
    if len(buf) < W * H * 4: break
    fr = Image.frombuffer('RGBA', (W, H), buf, 'raw', 'RGBA', 0, 1).copy()
    for s0, e0, im, x, y, anim in items:
        if s0 <= f < e0: gfx.place(fr, im, x, y, anim, f, s0, e0)
    enc.stdin.write(fr.tobytes()); f += 1
enc.stdin.close(); enc.wait(); dec.wait()
print('frames', f, 'expected', NF)

# ---------- 3. mix: steady music bed (no ducking) under the voice, master -14 LUFS / -1.5 dBTP ----------
mfile, moff, mdb = edl.MUSIC
dur = NF / FPS
run(['ffmpeg', '-v', 'error', '-y', '-i', 'vo/narr.wav', '-ss', str(moff), '-i', mfile,
     '-filter_complex',
     f"[1:a]aresample=48000,loudnorm=I=-16:TP=-2,volume={mdb}dB,afade=t=in:d=0.25,afade=t=out:st={dur-1.3:.2f}:d=1.3,atrim=0:{dur:.3f}[m];"
     f"[0:a]aresample=48000,apad[v];[v][m]amix=inputs=2:normalize=0:duration=longest,atrim=0:{dur:.3f},"
     f"loudnorm=I=-14:TP=-1.5:LRA=7,aresample=48000[a]",
     '-map', '[a]', '-c:a', 'pcm_s16le', 'out/mix.wav'])
run(['ffmpeg', '-v', 'error', '-y', '-i', 'out/gfx.mp4', '-i', 'out/mix.wav', '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
     '-c:a', 'aac', '-b:a', '256k', '-shortest', '-movflags', '+faststart', 'out/final_1080.mp4'])
run(['ffmpeg', '-v', 'error', '-y', '-i', 'out/final_1080.mp4', '-vf', 'scale=540:960', '-c:v', 'libx264', '-crf', '23',
     '-c:a', 'aac', '-b:a', '128k', 'out/final_540.mp4'])
# upload copy (smaller, same look)
run(['ffmpeg', '-v', 'error', '-y', '-i', 'out/gfx.mp4', '-i', 'out/mix.wav', '-map', '0:v', '-map', '1:a', '-c:v', 'libx264',
     '-preset', 'slow', '-crf', '20', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', '-shortest', 'out/upload_ig.mp4'])
os.remove('out/base.mp4')
print('done: out/final_1080.mp4, out/upload_ig.mp4, out/final_540.mp4')
