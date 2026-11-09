# Energy check (noise-relative, like cutcheck.py) for every in/out point carrying his voice.
# OUT: ≥0.15 s silence before the cut and no speech within 0.05 s after. IN: no speech in the 0.05 s before the in-point.
import sys, os, subprocess, numpy as np
os.chdir(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, '.')
from bxj_segs import S
def src(n):
    for e in ('.MOV', '.mp4'):
        if os.path.exists('src/' + n + e): return 'src/' + n + e
def env(f, a, d):
    x = np.frombuffer(subprocess.run(['ffmpeg', '-loglevel', 'error', '-ss', str(max(0, a)), '-t', str(d), '-i', f, '-ac', '1', '-ar', '16000',
        '-af', 'highpass=f=150,lowpass=f=4000', '-f', 'f32le', '-'], capture_output=True).stdout, dtype=np.float32)
    h = 160; return np.array([20 * np.log10(np.sqrt(np.mean(x[i:i + h] ** 2)) + 1e-7) for i in range(0, len(x) - h + 1, h)])
bad = 0
for sid, shots, au in S:
    if au == 'talk': n, a, b, _ = shots[0]
    elif au[0] == 'vo': _, n, a, b, _ = au
    else: continue
    f = src(n); e = env(f, a - 1.0, b - a + 2.0)
    floor = np.percentile(e, 10); peak = np.percentile(e, 98); thr = floor + 0.35 * (peak - floor); v = e > thr
    ci = 100; co = int(round((b - a + 1.0) / 0.01))
    pre = np.where(v[ci - 5:ci])[0]                       # speech just before the in-point?
    before = np.where(v[:co])[0]; after = np.where(v[co:])[0]
    tail = (co - before[-1] - 1) * 0.01 if len(before) else 9; nxt = after[0] * 0.01 if len(after) else 9
    ok_out = tail >= 0.15 and nxt >= 0.05; ok_in = len(pre) == 0
    bad += (not ok_out) + (not ok_in)
    print(f"{sid:3s} {n:26s} in@{a:7.2f} {'ok' if ok_in else 'SPEECH BEFORE IN'}  out@{b:7.2f} tail {tail:4.2f}s next {nxt:4.2f}s "
          f"floor {floor:5.1f}  {'OK' if ok_out and ok_in else 'FAIL'}")
print('ALL OK' if not bad else f'{bad} FAIL'); sys.exit(1 if bad else 0)
