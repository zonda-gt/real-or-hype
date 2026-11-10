# Add effects to out/bxj_1080.mp4 -> out/bxj_final_1080.mp4 (+540p). Each effect peak-normalised to -6 dBFS, then role volume;
# its PEAK lands on the moment. usage: bxj_sfx.py <ding.wav> <whoosh.wav>
import sys, os, json, subprocess, numpy as np
os.chdir(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, '.')
import bxj_segs as G
DING, WHOOSH = sys.argv[1], sys.argv[2]
st = json.load(open('out/starts.json'))
SEG = {sid: (shots, au) for sid, shots, au in G.S}
def otime(sid, t):
    shots, au = SEG[sid]; a, sp = (shots[0][1], shots[0][3]) if au == 'talk' else (au[2], au[4]); return st[sid] + (t - a) / sp
def load(f):
    return np.frombuffer(subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', f, '-ac', '1', '-ar', '48000', '-f', 'f32le', '-'],
                                        capture_output=True).stdout, dtype=np.float32)
def peak(f):
    a = load(f); return 20 * np.log10(np.abs(a).max() + 1e-9), np.abs(a).argmax() / 48000
ev = [(WHOOSH, st['V1'], 0.45), (WHOOSH, st['D1'], 0.40), (WHOOSH, st['E1'], 0.40)]
DOFF = float(sys.argv[3]) if len(sys.argv) > 3 else 0.30; DVOL = float(sys.argv[4]) if len(sys.argv) > 4 else 0.35
ev += [(DING, otime(sid, t) - DOFF, DVOL) for sid, t, _ in G.BADGES]
inp = ['-i', 'out/bxj_1080.mp4']; fc = ''
for i, (f, t, v) in enumerate(ev):
    pdb, pt = peak(f); g = 10 ** ((-6 - pdb) / 20) * v; ms = max(0, int((t - pt) * 1000))
    inp += ['-i', f]; fc += f'[{i + 1}:a]aresample=48000,aformat=channel_layouts=stereo,volume={g:.4f},adelay={ms}|{ms}[s{i}];'
fc += '[0:a]' + ''.join(f'[s{i}]' for i in range(len(ev))) + f'amix=inputs={len(ev) + 1}:normalize=0:duration=first,alimiter=limit=0.84:level=false[a]'
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y'] + inp + ['-filter_complex', fc, '-map', '0:v', '-map', '[a]', '-c:v', 'copy',
                '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', 'out/bxj_final_1080.mp4'], check=True)
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', 'out/bxj_final_1080.mp4', '-vf', 'scale=540:960', '-c:v', 'libx264', '-crf', '24',
                '-preset', 'veryfast', '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', 'out/bxj_final_540.mp4'], check=True)
print('sfx ok', [(os.path.basename(f), round(t, 2)) for f, t, _ in ev])
