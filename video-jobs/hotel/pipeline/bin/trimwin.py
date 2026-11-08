"""Shrink each named shot window so it excludes creator transitions (flash/black/blur/streak frames near cuts).
Rule: from each end, skip frames while sharpness < 0.6*window median, brightness deviates > 25 from window median,
or a histogram jump > 0.06 occurs within the next 4 frames; then add a 3-frame safety margin."""
import sys, os, json, numpy as np
sys.path.insert(0, 'specs'); sys.path.insert(0, 'bin')
from shots import S
def rows(c):
    for f in (f'score/hd_{c}.json', f'score/{c}.json'):
        if os.path.exists(f): d = json.load(open(f)); return np.array(d['rows']), d['fps']
out = {}
for name, (c, t0, t1) in S.items():
    R, fps = rows(c); a, b = int(round(t0 * fps)), int(round(t1 * fps))
    W = R[a:b]; ms = np.median(W[:, 0]); mb = np.median(W[:, 1])
    def bad(i):
        r = R[i]
        jump = R[i:i + 5, 5].max() if i + 5 <= len(R) else 1
        return r[0] < 0.6 * ms or abs(r[1] - mb) > 25 or jump > 0.06
    def badb(i):
        r = R[i]; jump = R[max(0, i - 4):i + 1, 5].max()
        return r[0] < 0.6 * ms or abs(r[1] - mb) > 25 or jump > 0.06
    i = a
    while i < b and bad(i): i += 1
    j = b - 1
    while j > i and badb(j): j -= 1
    na, nb = (i + 3) / fps, (j - 3) / fps
    out[name] = (c, round(na, 2), round(nb, 2))
    flag = '' if nb - na > 0.6 else '  <-- TOO SHORT'
    print(f'{name:14s} {t0:6.2f}-{t1:6.2f} -> {na:6.2f}-{nb:6.2f}  ({nb - na:.2f}s){flag}')
json.dump(out, open('data/shots_trimmed.json', 'w'), indent=0)
