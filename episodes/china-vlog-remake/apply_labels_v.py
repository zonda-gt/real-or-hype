# Burn place-name labels into the 9:16 cut; each label shows for exactly its shot (frame-accurate).
import os, sys, subprocess
here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, here)
from plan_v import CUTS
from labels_v import LABELS
FPS = 30
src = f'{here}/china_vlog_9x16_1080x1920.mp4'; out = f'{here}/china_vlog_9x16_labels_1080x1920.mp4'
ins = ['-i', src]; chain = []; last = '0:v'
for n, k in enumerate(sorted(LABELS)):
    ins += ['-loop', '1', '-framerate', str(FPS), '-i', f'{here}/labels_v/label{k:02d}.png']
    a, b = round(CUTS[k] * FPS), round(CUTS[k + 1] * FPS) - 1
    tag = f'v{n}'
    chain.append(f"[{last}][{n+1}:v]overlay=0:0:eof_action=pass:repeatlast=0:shortest=0:enable='between(t,{(a-0.5)/FPS:.4f},{(b+0.5)/FPS:.4f})'[{tag}]"); last = tag
cmd = ['ffmpeg', '-v', 'error', '-y', *ins, '-filter_complex', ';'.join(chain), '-map', f'[{last}]', '-map', '0:a',
       '-c:v', 'libx264', '-crf', '16', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-c:a', 'copy', '-movflags', '+faststart', out]
subprocess.run(cmd, check=True); print(out)
