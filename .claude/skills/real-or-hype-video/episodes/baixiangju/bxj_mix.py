# Final mix: out/bxj_1080.mp4 (voice + ambience) + effects + background music (sidechain-ducked under his voice,
# cut by a record scratch on "Wait, what?", faded on the end card) -> out/bxj_final_1080.mp4 (+540p).
# usage: bxj_mix.py <music.wav> [music_gain_db]
import sys, os, json, subprocess, numpy as np
os.chdir(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, '.')
import bxj_segs as G
MUSIC = sys.argv[1]; MDB = float(sys.argv[2]) if len(sys.argv) > 2 else -21.0
st = json.load(open('out/starts.json'))
total = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', 'out/bxj_1080.mp4'],
                             capture_output=True, text=True).stdout)
SEG = {sid: (shots, au) for sid, shots, au in G.S}
def otime(sid, t):
    shots, au = SEG[sid]; a, sp = (shots[0][1], shots[0][3]) if au == 'talk' else (au[2], au[4]); return st[sid] + (t - a) / sp
def peak(f):
    a = np.frombuffer(subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', f, '-ac', '1', '-ar', '48000', '-f', 'f32le', '-'],
                                     capture_output=True).stdout, dtype=np.float32)
    return 20 * np.log10(np.abs(a).max() + 1e-9), np.abs(a).argmax() / 48000
DING, WHOOSH, SCRATCH = 'sfx/ding_el.wav', 'sfx/whoosh_tonal.wav', 'sfx/scratch_el.wav'
WAIT = otime('T5', 154.84)                      # onset of "Wait, what?" (energy onset in the source)
ev = [(WHOOSH, st['V1'], 0.45), (WHOOSH, st['D1'], 0.40), (WHOOSH, st['E1'], 0.40),
      (SCRATCH, WAIT - 0.12, 0.55)]
ev += [(DING, otime(sid, t) - 0.30, 0.35) for sid, t, _ in G.BADGES]
# music gain envelope: silent from the scratch until after "what? what?", ramps back in; fades over the end card
m0, m1 = WAIT - 0.05, otime('T5', 156.35)
fo = st['E1'] + 0.8
env = (f"if(lt(t,{m0:.3f}),1,if(lt(t,{m1:.3f}),0,if(lt(t,{m1 + 0.5:.3f}),(t-{m1:.3f})/0.5,"
       f"if(lt(t,{fo:.3f}),1,max(0,1-(t-{fo:.3f})/{total - fo:.3f})))))")
inp = ['-i', 'out/bxj_1080.mp4', '-i', MUSIC]; fc = ''
fc += (f'[1:a]aresample=48000,aformat=channel_layouts=stereo,atrim=duration={total:.3f},loudnorm=I=-16:TP=-2:LRA=11,'
       f"aresample=48000,volume={MDB}dB,volume='{env}':eval=frame[mus];")
fc += '[0:a]asplit=2[base][key];'
fc += '[mus][key]sidechaincompress=threshold=0.02:ratio=6:attack=15:release=350:makeup=1[duck];'
for i, (f, t, v) in enumerate(ev):
    pdb, pt = peak(f); g = 10 ** ((-6 - pdb) / 20) * v; ms = max(0, int((t - pt) * 1000))
    inp += ['-i', f]
    fc += f'[{i + 2}:a]aresample=48000,aformat=channel_layouts=stereo,volume={g:.4f},adelay={ms}|{ms}[s{i}];'
fc += ('[base][duck]' + ''.join(f'[s{i}]' for i in range(len(ev))) +
       f'amix=inputs={len(ev) + 2}:normalize=0:duration=first,volume=1.5dB,alimiter=limit=0.84:level=false[a]')
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y'] + inp + ['-filter_complex', fc, '-map', '0:v', '-map', '[a]', '-c:v', 'copy',
                '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', 'out/bxj_final_1080.mp4'], check=True)
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', 'out/bxj_final_1080.mp4', '-vf', 'scale=540:960', '-c:v', 'libx264', '-crf', '24',
                '-preset', 'veryfast', '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', 'out/bxj_final_540.mp4'], check=True)
print('mix ok; music cut', round(m0, 2), '-', round(m1, 2), '; effects', [(os.path.basename(f), round(t, 2)) for f, t, _ in ev])
