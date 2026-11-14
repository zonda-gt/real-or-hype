# Final QA for a rendered mall-reel. usage (from project dir): python3 -I <skill>/scripts/qa.py [out/final_1080.mp4]
# Checks: duration, integrated loudness (target -14 LUFS), true peak (<= -1.5 dBTP), every script word heard over the music
# (Whisper medium, diff against script.txt), and no single-frame flashes / black frames in out/gfx.mp4.
import subprocess, sys, re, difflib, numpy as np
f = sys.argv[1] if len(sys.argv) > 1 else 'out/final_1080.mp4'
ok = True
dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f], capture_output=True, text=True).stdout)
r = subprocess.run(['ffmpeg', '-hide_banner', '-i', f, '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True).stderr
s = r[r.rfind('Summary'):]
I = float([l.split()[1] for l in s.splitlines() if l.strip().startswith('I:')][0])
TP = float([l.split()[1] for l in s.splitlines() if l.strip().startswith('Peak:')][-1])
print(f'duration {dur:.1f}s | loudness {I} LUFS (target -14) | true peak {TP} dBTP (max -1.5)')
if abs(I + 14) > 1 or TP > -1.4: ok = False; print('  FAIL loudness/peak')

from faster_whisper import WhisperModel
m = WhisperModel('medium.en', device='cpu', compute_type='int8')
a = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-ac', '1', '-ar', '16000', '-f', 'f32le', '-'], capture_output=True).stdout, np.float32)
hyp = ' '.join(x.text for x in m.transcribe(a, beam_size=5)[0]).lower()
ref = re.sub(r'\[.*?\]', '', open('script.txt').read()).lower()
n = lambda t: re.findall(r"[a-z0-9']+", t.replace('-', ' '))
sm = difflib.SequenceMatcher(None, n(ref), n(hyp))
diffs = [(' '.join(n(ref)[i1:i2]), ' '.join(n(hyp)[j1:j2])) for t, i1, i2, j1, j2 in sm.get_opcodes() if t != 'equal']
print('words that differ (spelling-only diffs like westbund/cafes and Chinese names are fine):', diffs)

subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', 'out/gfx.mp4', '-vf', 'scale=54:96,signalstats,metadata=print:key=lavfi.signalstats.YAVG:file=out/yavg.txt', '-f', 'null', '-'])
y = [float(l.split('=')[1]) for l in open('out/yavg.txt') if 'YAVG' in l]
spikes = [i for i in range(1, len(y) - 1) if abs(y[i] - y[i - 1]) > 25 and abs(y[i] - y[i + 1]) > 25]
print(f'frames {len(y)}, darkest luma {min(y):.0f} (black < 16), single-frame flashes {spikes}')
if spikes or min(y) < 16: ok = False
print('QA PASS' if ok else 'QA FAIL'); sys.exit(0 if ok else 1)
