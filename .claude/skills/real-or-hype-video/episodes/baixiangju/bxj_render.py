# Render the Baixiangju recreation from bxj_segs.py -> out/bxj_1080.mp4 (+ 540p preview).
import sys, os, subprocess, json, re, difflib
os.chdir(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, '.')
import bxj_segs as G
os.makedirs('seg', exist_ok=True); os.makedirs('out', exist_ok=True)
FONTS = '/home/user/real-or-hype/.claude/skills/real-or-hype-video/scripts'
FULL = 'scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,fps=30,setsar=1'
TM = ('zscale=tin=arib-std-b67:min=bt2020nc:pin=bt2020:t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,'
      'tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p,')
ENC = ['-c:v', 'libx264', '-preset', 'veryfast', '-crf', '17', '-pix_fmt', 'yuv420p', '-color_primaries', 'bt709',
       '-color_trc', 'bt709', '-colorspace', 'bt709', '-c:a', 'pcm_s16le', '-ar', '48000', '-ac', '2']
AF = 'aresample=48000,aformat=channel_layouts=stereo'
def src(n):
    if n.startswith('B:'): return f'broll/{n[2:]}_hq.mp4'
    for e in ('.MOV', '.mp4'):
        if os.path.exists('src/' + n + e): return 'src/' + n + e
    raise SystemExit('missing ' + n)
_h = {}
def vf(p):
    if p not in _h:
        _h[p] = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=color_transfer',
                                '-of', 'csv=p=0', p], capture_output=True, text=True).stdout.strip().startswith('arib-std-b67')
    return (TM if _h[p] else '') + FULL
def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: print(' '.join(cmd)[:600]); print(r.stderr[-2000:]); sys.exit(1)
def dur(p, s='v'):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-select_streams', s, '-show_entries', 'stream=duration', '-of', 'csv=p=0', p],
                                capture_output=True, text=True).stdout)
def talk_af(sp, d):
    return f'{AF},atempo={sp},highpass=f=80,loudnorm=I=-16:TP=-1.5:LRA=11,{AF},afade=t=in:d=0.02,afade=t=out:st={d-0.05:.3f}:d=0.05,apad'

starts, t, segs = {}, 0.0, []
for sid, shots, au in G.S:
    out = f'seg/{sid}.mp4'; inp = []; fc = ''; d = 0.0
    for i, (n, a, b, sp) in enumerate(shots):
        sd = (b - a) / sp; d += sd
        inp += ['-ss', f'{a:.3f}', '-t', f'{b - a + 0.1:.3f}', '-i', src(n)]
        fc += f'[{i}:v]setpts=(PTS-STARTPTS)/{sp},{vf(src(n))},trim=duration={sd:.3f},setpts=PTS-STARTPTS[v{i}];'
    k = len(shots)
    fc += ''.join(f'[v{i}]' for i in range(k)) + f'concat=n={k}:v=1:a=0[v];'
    if au == 'talk':
        fc += f'[0:a]{talk_af(shots[0][3], d)}[a]'
    elif au[0] == 'vo':
        _, n, a, b, sp = au
        inp += ['-ss', f'{a:.3f}', '-t', f'{b - a:.3f}', '-i', src(n)]
        vd = (b - a) / sp
        if vd > d + 0.01: raise SystemExit(f'{sid}: voice {vd:.2f}s longer than shots {d:.2f}s')
        fc += f'[{k}:a]{talk_af(sp, vd)}[a]'
    else:
        vol = au[1]
        for i, (n, a, b, sp) in enumerate(shots):
            fc += f'[{i}:a]{AF},atempo={sp},volume={vol},atrim=duration={(b - a) / sp:.3f},asetpts=PTS-STARTPTS[a{i}];'
        fc += ''.join(f'[a{i}]' for i in range(k)) + f'concat=n={k}:v=0:a=1,afade=t=in:d=0.03,afade=t=out:st={d-0.04:.3f}:d=0.04,apad[a]'
    run(['ffmpeg', '-loglevel', 'error', '-y'] + inp + ['-filter_complex', fc, '-map', '[v]', '-map', '[a]', '-t', f'{d:.3f}'] + ENC + [out])
    starts[sid] = t; t += dur(out); segs.append(out)
total = t
open('seg/list.txt', 'w').write(''.join(f"file '{os.path.abspath(p)}'\n" for p in segs))
run(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', 'seg/list.txt', '-c:v', 'copy',
     '-af', 'aresample=async=1:first_pts=0', '-c:a', 'pcm_s16le', 'seg/concat.mov'])
SEG = {sid: (shots, au) for sid, shots, au in G.S}
def otime(sid, src_t):        # source time inside a talk/vo segment -> output time
    shots, au = SEG[sid]
    a, sp = (shots[0][1], shots[0][3]) if au == 'talk' else (au[2], au[4])
    return starts[sid] + (src_t - a) / sp

# ---- subtitles: exact script text, timed from Whisper word stamps (medium model) on the same source audio
WJ = json.load(open('words.json'))
allw = [tuple(w) for v in WJ.values() for w in v]
norm = lambda s: re.sub(r"[^a-z0-9]", '', s.lower().replace('10th', 'tenth').replace('15th', 'fifteenth')
                        .replace('14th', 'fourteenth').replace('12th', 'twelfth'))
def words_for(sid):
    shots, au = SEG[sid]
    a, b = (shots[0][1], shots[0][2]) if au == 'talk' else (au[2], au[3])
    ww = sorted({w for w in allw if w[0] >= a - 0.05 and w[1] <= b + 0.3})
    return ww, a, b
SUBW = []
for sid, text in G.LINES:
    tw = text.split(); ww, a, b = words_for(sid)
    sm = difflib.SequenceMatcher(None, [norm(x) for x in tw], [norm(x[2]) for x in ww], autojunk=False)
    tm = [None] * len(tw)
    for blk in sm.get_matching_blocks():
        for j in range(blk.size): tm[blk.a + j] = (ww[blk.b + j][0], ww[blk.b + j][1])
    # interpolate unmatched words between matched neighbours
    known = [i for i, x in enumerate(tm) if x]
    s0 = tm[known[0]][0] if known else a; s1 = tm[known[-1]][1] if known else b
    for i in range(len(tw)):
        if tm[i]: continue
        p = max([j for j in known if j < i], default=None); q = min([j for j in known if j > i], default=None)
        lo = tm[p][1] if p is not None else max(a, s0 - 0.3); hi = tm[q][0] if q is not None else min(b, s1 + 0.3)
        gap = [j for j in range(len(tw)) if (p is None or j > p) and (q is None or j < q)]
        n = len(gap); r = gap.index(i)
        tm[i] = (lo + (hi - lo) * r / n, lo + (hi - lo) * (r + 1) / n)
    seg_end = starts[sid] + dur(f'seg/{sid}.mp4') - 0.02
    SUBW.append([(min(otime(sid, x[0]), seg_end), min(otime(sid, x[1]), seg_end), w) for x, w in zip(tm, tw)])
def ts(x): return f'{int(x // 3600)}:{int(x % 3600 // 60):02d}:{x % 60:05.2f}'
ass = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 1

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: main,Montserrat ExtraBold,66,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,6,0,2,90,90,430,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
for ws in SUBW:
    chunks, cur = [], []
    for w in ws:
        cur.append(w)
        if len(cur) == 3 or w[2][-1] in '.,?!:': chunks.append(cur); cur = []
    if cur: chunks.append(cur)
    for ci, ch in enumerate(chunks):
        endc = chunks[ci + 1][0][0] if ci + 1 < len(chunks) else ch[-1][1] + 0.25
        for wi, (a, b, w) in enumerate(ch):
            e = ch[wi + 1][0] if wi + 1 < len(ch) else endc
            txt = ' '.join(('{\\c&H1AE2FF&}' + x[2] + '{\\c&HFFFFFF&}') if j == wi else x[2] for j, x in enumerate(ch))
            ass += f'Dialogue: 0,{ts(a)},{ts(max(e, a + 0.05))},main,,0,0,0,,{txt}\n'
open('out/subs.ass', 'w').write(ass)

# ---- overlays: hook title, floor badge (changes 2 frames before the word), end card
end_of = lambda sid: starts[sid] + dur(f'seg/{sid}.mp4')
ovs = [('title.png', starts[G.TITLE[0]], end_of(G.TITLE[1]))]
bt = [(otime(sid, x) - 2 / 30, png) for sid, x, png in G.BADGES]
for i, (a, png) in enumerate(bt):
    ovs.append((png, a, bt[i + 1][0] if i + 1 < len(bt) else starts[G.ENDCARD]))
ovs.append(('endcard.png', starts[G.ENDCARD] + 0.2, total))
inputs = ['-i', 'seg/concat.mov']; fc = '[0:v]null[v0];'; last = 'v0'
for i, (png, a, b) in enumerate(ovs):
    inputs += ['-loop', '1', '-t', f'{total:.3f}', '-i', 'ov/' + png]
    fc += f"[{last}][{i + 1}:v]overlay=enable='between(t,{a:.3f},{b - 0.001:.3f})'[v{i + 1}];"; last = f'v{i + 1}'
fc += f"[{last}]subtitles=out/subs.ass:fontsdir={FONTS}[v];[0:a]alimiter=limit=0.84:level=false[a]"
run(['ffmpeg', '-loglevel', 'error', '-y'] + inputs + ['-filter_complex', fc, '-map', '[v]', '-map', '[a]', '-t', f'{total:.3f}',
     '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', '-color_primaries', 'bt709', '-color_trc', 'bt709',
     '-colorspace', 'bt709', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', 'out/bxj_1080.mp4'])
run(['ffmpeg', '-loglevel', 'error', '-y', '-i', 'out/bxj_1080.mp4', '-vf', 'scale=540:960', '-c:v', 'libx264', '-crf', '24',
     '-preset', 'veryfast', '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', 'out/bxj_540.mp4'])
json.dump(starts, open('out/starts.json', 'w'), indent=0)
print('TOTAL', round(total, 2)); print({k: round(v, 2) for k, v in starts.items()})
