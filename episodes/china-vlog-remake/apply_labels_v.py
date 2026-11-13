# Burn place-name labels into the 9:16 cut; each label shows for exactly its shot (frame-accurate).
import os, sys, subprocess
here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, here)
from labels_v import LABELS, LDIR, _P
CUTS = _P.CUTS
FPS = 30
src = f"{here}/{os.environ.get('SRC', 'china_vlog_9x16_1080x1920.mp4')}"; out = f"{here}/{os.environ.get('OUT', 'china_vlog_9x16_labels_1080x1920.mp4')}"
ins = ['-i', src]; chain = []; last = '0:v'
cta_from = getattr(_P, 'CTA_FROM_SHOT', None)
T0 = round(CUTS[cta_from] * FPS) / FPS if cta_from is not None else None
if T0 is not None:
    if os.environ.get('CTA_BG', 'blur') == 'blur':   # end card: blur + dim the footage
        chain.append(f"[0:v]split[base][blr];[blr]gblur=sigma=16,format=rgba,colorchannelmixer=rr=0.6:gg=0.6:bb=0.6,eq=saturation=0.85,fade=t=in:st={T0:.4f}:d=0.35:alpha=1[blurred]")
        chain.append("[base][blurred]overlay=0:0:format=auto[vb]"); last = 'vb'
    else:                                             # footage stays sharp; soft dark shade behind the text only
        ins += ['-loop', '1', '-framerate', str(FPS), '-i', f'{here}/{LDIR}/scrim.png']; SCRIM_IN = True
        chain.append(f"[SCRIM]format=rgba,fade=t=in:st={T0:.4f}:d=0.35:alpha=1[scrim]")
        chain.append(f"[0:v][scrim]overlay=0:0:eof_action=pass:shortest=0:enable='gte(t,{T0 - 0.5 / FPS:.4f})'[vb]"); last = 'vb'
    LABELS = {k: v for k, v in LABELS.items() if k < cta_from}   # the end card replaces labels on its shots
OFF = 1 if 'SCRIM_IN' in globals() else 0
chain = [c.replace('[SCRIM]', '[1:v]') for c in chain]
for n, k in enumerate(sorted(LABELS)):
    ins += ['-loop', '1', '-framerate', str(FPS), '-i', f'{here}/{LDIR}/label{k:02d}.png']
    a, b = round(CUTS[k] * FPS), round(CUTS[k + 1] * FPS) - 1
    tag = f'v{n}'
    chain.append(f"[{last}][{n+1+OFF}:v]overlay=0:0:eof_action=pass:repeatlast=0:shortest=0:enable='between(t,{(a-0.5)/FPS:.4f},{(b+0.5)/FPS:.4f})'[{tag}]"); last = tag
if T0 is not None and os.path.exists(f'{here}/{LDIR}/cta.png'):
    n = len(LABELS) + 1 + OFF; t1 = T0 + 0.12; D = 0.45
    ins += ['-loop', '1', '-framerate', str(FPS), '-i', f'{here}/{LDIR}/cta.png']
    chain.append(f"[{n}:v]format=rgba,fade=t=in:st={t1:.4f}:d={D}:alpha=1[cta]")
    y = f"if(lt(t,{t1:.4f}),40,40*pow(max(0,1-(t-{t1:.4f})/{D}),3))"   # ease-out rise
    chain.append(f"[{last}][cta]overlay=x=0:y='{y}':eval=frame:eof_action=pass:shortest=0:enable='gte(t,{t1 - 0.5 / FPS:.4f})'[vc]"); last = 'vc'
cmd = ['ffmpeg', '-v', 'error', '-y', *ins, '-filter_complex', ';'.join(chain), '-map', f'[{last}]', '-map', '0:a',
       '-c:v', 'libx264', '-crf', '16', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-c:a', 'copy', '-movflags', '+faststart', out]
subprocess.run(cmd, check=True); print(out)
