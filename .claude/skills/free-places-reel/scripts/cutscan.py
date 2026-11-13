"""Find cuts/flashes inside each chosen window: cutscan.py PLAN RAWDIR. Any line printed = fix that in-point (or slow it with speed)."""
import sys, subprocess, re
sys.path.insert(0, __import__('os').path.dirname(__file__)); from common import CUTS, load_plan
P = load_plan(sys.argv[1]); raw = sys.argv[2]; bad = 0
for i, (c, t0, l) in enumerate(P['shots']):
    d = (CUTS[i+1]-CUTS[i]) * P['speed'].get(i, 1)
    r = subprocess.run(['ffmpeg', '-hide_banner', '-ss', str(t0), '-t', f'{d:.3f}', '-i', f'{raw}/{c}.mp4', '-vf', "select='gt(scene,0.1)',metadata=print", '-an', '-f', 'null', '-'], capture_output=True, text=True).stderr
    hits = [(float(t), float(s)) for t, s in zip(re.findall(r'pts_time:([0-9.]+)', r), re.findall(r'scene_score=([0-9.]+)', r)) if float(t) > 0.06 or float(s) > 0.3]
    if hits: bad += 1; print(i+1, c, t0, [(round(t, 2), round(s, 2)) for t, s in hits])
print('scan done,', bad, 'windows to look at (steady scores ~0.1-0.25 = camera motion, a single spike >0.3 = a cut)')
