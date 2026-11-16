# usage: render.py A|B  -> out/<V>_1080.mp4 and out/<V>_540.mp4
import sys, os, json, subprocess, numpy as np
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from variants import VARIANTS
V = sys.argv[1]; BEATS = VARIANTS[V]
os.makedirs(f'seg{V}', exist_ok=True); os.makedirs('out', exist_ok=True)
SK = '/home/user/real-or-hype/.claude/skills/real-or-hype-video'
FONTS = SK + '/scripts'
SFX = {'whoosh': SK + '/sfx/whoosh_es.wav', 'pop': SK + '/sfx/pop_es.wav', 'ding': SK + '/sfx/ding.wav'}
SFXVOL = {'whoosh': 0.45, 'pop': 0.5, 'ding': 0.35}
AMB = 0.35; MUSIC = 'music/pop1.mp3'; MDB = -6.0
FULL = 'scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,fps=30,setsar=1,format=yuv420p'
ENC = ['-c:v', 'libx264', '-preset', 'veryfast', '-crf', '17', '-pix_fmt', 'yuv420p', '-color_primaries', 'bt709',
       '-color_trc', 'bt709', '-colorspace', 'bt709', '-c:a', 'pcm_s16le', '-ar', '48000', '-ac', '2']
AF = 'aresample=48000,aformat=channel_layouts=stereo'
def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: print(' '.join(cmd)[:800]); print(r.stderr[-2000:]); sys.exit(1)
def dur(p, s='v'):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-select_streams', s, '-show_entries', 'stream=duration',
                                 '-of', 'csv=p=0', p], capture_output=True, text=True).stdout)
def pcm(f, sr=16000):
    return np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-ac', '1', '-ar', str(sr), '-f', 'f32le', '-'],
                                        capture_output=True).stdout, np.float32)

# ---- 1. shots
segs, t, beat_t = [], 0.0, []
for bi, (vo, shots, ex) in enumerate(BEATS):
    beat_t.append(t)
    for si, (n, a, b, sp) in enumerate(shots):
        out = f'seg{V}/{bi:02d}_{si}.mp4'; d = (b - a) / sp
        if vo == 'TALK':
            af = f'{AF},atempo={sp},highpass=f=80,loudnorm=I=-16:TP=-1.5:LRA=11,{AF},afade=t=in:d=0.02,afade=t=out:st={d-0.05:.3f}:d=0.05,apad'
        else:
            af = f'{AF},atempo={sp},volume={AMB},afade=t=in:d=0.03,afade=t=out:st={d-0.04:.3f}:d=0.04,apad'
        run(['ffmpeg', '-loglevel', 'error', '-y', '-ss', f'{a:.3f}', '-t', f'{b - a + 0.1:.3f}', '-i', f'src/{n}.mp4',
             '-filter_complex', f'[0:v]setpts=(PTS-STARTPTS)/{sp},{FULL},trim=duration={d:.3f},setpts=PTS-STARTPTS[v];[0:a]{af}[a]',
             '-map', '[v]', '-map', '[a]', '-t', f'{d:.3f}'] + ENC + [out])
        segs.append(out); t += dur(out)
total = t; beat_t.append(total)
open(f'seg{V}/list.txt', 'w').write(''.join(f"file '{os.path.abspath(p)}'\n" for p in segs))
run(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', f'seg{V}/list.txt', '-c:v', 'copy',
     '-af', 'aresample=async=1:first_pts=0', '-c:a', 'pcm_s16le', f'seg{V}/concat.mov'])

# ---- 2. narration placement + fit check
from faster_whisper import WhisperModel
wm = WhisperModel('small', compute_type='int8')
LINES = json.load(open('lines.json')); TALKTXT = "Guys, check out this phone. I'm going to turn the camera on now."
WJ = json.load(open('words.json'))
vo_ev, caps, bad = [], [], []
for bi, (vo, shots, ex) in enumerate(BEATS):
    b0, b1 = beat_t[bi], beat_t[bi + 1]
    if vo == 'TALK':
        n, a, bb, sp = shots[0]
        ww = [(b0 + (x - a) / sp, b0 + (y - a) / sp, w) for x, y, w in WJ[n] if x >= a and y <= bb + 0.05]
    elif vo:
        f = f'vo/{vo}.wav'; d = len(pcm(f)) / 16000; st = b0 + 0.06
        if st + d > b1 - 0.1: bad.append(f'{vo}: ends {st + d:.2f} > beat end {b1:.2f}-0.1')
        vo_ev.append((f, st))
        segw = [w for s in wm.transcribe(pcm(f), language='en', word_timestamps=True)[0] for w in s.words]
        tw = LINES[vo].split()
        if len(segw) == len(tw): ww = [(st + w.start, st + w.end, x) for w, x in zip(segw, tw)]
        else:   # proportional to word length within the voiced span
            s0, s1 = segw[0].start, segw[-1].end; Lc = sum(len(x) for x in tw); acc = 0; ww = []
            for x in tw:
                a0 = s0 + (s1 - s0) * acc / Lc; acc += len(x); ww.append((st + a0, st + s0 + (s1 - s0) * acc / Lc, x))
    else:
        ww = []
    if ex.get('nocap'): ww = []
    ww = ww[ex.get('capfrom', 0):]
    caps.append(ww)
if bad: print('FIT FAIL', bad); sys.exit(1)

# ---- 3. word-by-word captions (her style: one word at a time, chunky caps, centre-right)
def ts(x): return f'{int(x // 3600)}:{int(x % 3600 // 60):02d}:{x % 60:05.2f}'
ass = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: w,Montserrat ExtraBold,108,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,0,0,0,0,100,100,1,0,1,5,4,5,60,60,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
for ww in caps:
    for i, (a, b, w) in enumerate(ww):
        e = ww[i + 1][0] if i + 1 < len(ww) else b + 0.3
        e = min(max(e, a + 0.12), total - 0.02)
        txt = w.upper().replace('FOURTEEN', '14').replace('HUNDRED', '00') if False else w.upper()
        ass += f'Dialogue: 0,{ts(a - 2/30)},{ts(e - 2/30)},w,,0,0,0,,{{\\pos(640,1180)}}{txt}\n'
open(f'out/{V}.ass', 'w').write(ass)

# ---- 4. overlays
ovs = []
for bi, (vo, shots, ex) in enumerate(BEATS):
    for png, r0, r1 in ex.get('ov', []):
        ovs.append((png, beat_t[bi] + r0, beat_t[bi + 1] if r1 is None else beat_t[bi] + r1))
inputs = ['-i', f'seg{V}/concat.mov']; fc = '[0:v]null[v0];'; last = 'v0'
for i, (png, a, b) in enumerate(ovs):
    inputs += ['-loop', '1', '-t', f'{total:.3f}', '-i', f'ov/{png}.png']
    fc += f"[{last}][{i + 1}:v]overlay=enable='between(t,{a:.3f},{b - 0.001:.3f})'[v{i + 1}];"; last = f'v{i + 1}'
fc += f"[{last}]subtitles=out/{V}.ass:fontsdir={FONTS}[v]"
run(['ffmpeg', '-loglevel', 'error', '-y'] + inputs + ['-filter_complex', fc, '-map', '[v]', '-t', f'{total:.3f}',
     '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', '-color_primaries', 'bt709',
     '-color_trc', 'bt709', '-colorspace', 'bt709', f'seg{V}/video.mp4'])

# ---- 5. audio: shot audio (ambience + his line) + narration + ducked music + effects
def peak(f):
    a = pcm(f, 48000); return 20 * np.log10(np.abs(a).max() + 1e-9), np.abs(a).argmax() / 48000
sfx_ev = []
for bi, (vo, shots, ex) in enumerate(BEATS):
    for name, r in ex.get('sfx', []):
        sfx_ev.append((SFX[name], beat_t[bi] + r, SFXVOL[name]))
SR = 48000; N = int(round(total * SR))
def st2(f, extra=''):
    x = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-af', f'aresample={SR}' + extra, '-ac', '2', '-ar', str(SR),
                                      '-f', 'f32le', '-'], capture_output=True).stdout, np.float32).reshape(-1, 2).copy()
    return x
def place(buf, x, t0, g=1.0):
    i = int(round(t0 * SR)); x = x[:max(0, N - i)]; buf[i:i + len(x)] += x * g
voice = np.zeros((N, 2), np.float32); fx = np.zeros((N, 2), np.float32)
base = st2(f'seg{V}/concat.mov'); voice[:min(N, len(base))] += base[:N]
narr = np.zeros((N, 2), np.float32)
for f, t0 in vo_ev: place(narr, st2(f, ',loudnorm=I=-16:TP=-1.5:LRA=11'), t0)
voice += narr
mus = st2(MUSIC, ',loudnorm=I=-16:TP=-2:LRA=11')[:N]
if len(mus) < N: mus = np.pad(mus, ((0, N - len(mus)), (0, 0)))
# ducking: envelope of narration + his talk segment
talk = np.zeros(N, np.float32)
for bi, (vo, shots, ex) in enumerate(BEATS):
    if vo == 'TALK': talk[int(beat_t[bi] * SR):int(beat_t[bi + 1] * SR)] = 1
hop = 480; env = np.sqrt(np.convolve((narr ** 2).mean(1), np.ones(hop) / hop, 'same'))
act = np.maximum((env > 0.01).astype(np.float32), talk)
# hold 250 ms, smooth 80 ms
k = int(0.25 * SR); act = np.convolve(act, np.ones(k), 'same') > 0
sm = int(0.08 * SR); gain_db = np.where(act, MDB - 9, MDB).astype(np.float32)
gain_db = np.convolve(gain_db, np.ones(sm) / sm, 'same')
g = 10 ** (gain_db / 20); fade = np.ones(N, np.float32)
fi = int(0.3 * SR); fade[:fi] = np.linspace(0, 1, fi); fo = int(1.2 * SR); fade[-fo:] = np.linspace(1, 0, fo)
mus = mus * (g * fade)[:, None]
for f, t0, v in sfx_ev:
    x = st2(f); pk = np.abs(x).max(); pt = np.abs(x).max(1).argmax() / SR
    gg = 10 ** (-6 / 20) / pk * v; start = t0 - pt if 'whoosh' in f else t0
    place(fx, x, max(0, start), gg)
mix = (voice + mus + fx) * 10 ** (1 / 20)
mix.astype(np.float32).tofile(f'seg{V}/mix.f32')
run(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', f'seg{V}/mix.f32',
     '-af', 'alimiter=limit=0.84:level=false', '-c:a', 'pcm_s16le', f'seg{V}/mix.wav'])
run(['ffmpeg', '-loglevel', 'error', '-y', '-i', f'seg{V}/video.mp4', '-i', f'seg{V}/mix.wav', '-map', '0:v', '-map', '1:a',
     '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', f'out/{V}_1080.mp4'])
run(['ffmpeg', '-loglevel', 'error', '-y', '-i', f'out/{V}_1080.mp4', '-vf', 'scale=540:960', '-c:v', 'libx264', '-crf', '24',
     '-preset', 'veryfast', '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', f'out/{V}_540.mp4'])
json.dump({'beats': beat_t, 'vo': [(os.path.basename(f), round(s, 2)) for f, s in vo_ev]}, open(f'out/{V}_times.json', 'w'))
print(V, 'TOTAL', round(total, 2), 'beats', [round(x, 2) for x in beat_t])
