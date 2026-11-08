# Mix audio for promo_dm.py: viral clip's own sound under the hook (fades out as it shrinks into the chat),
# narration lines, and effects from sfx/ (each peak-normalised to -6 dBFS, then a role volume; peaks land on moments).
# usage: promo_audio.py <workdir>   -> <workdir>/promo_final.mp4
import sys, os, json, subprocess, numpy as np
WD = sys.argv[1]; SFX = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sfx')
CFG = json.load(open(f'{WD}/promo.json')); T = CFG['t']
def peak_db(f):
    a = np.frombuffer(subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', f, '-ac', '1', '-f', 'f32le', '-'], capture_output=True).stdout, dtype=np.float32)
    return 20 * np.log10(np.abs(a).max() + 1e-9)
ev = [('whoosh_es', 0.31, T['send'] + 0.1, 0.45), ('whoosh_es', 0.31, T['cta'], 0.45)]
ev += [('pop_es', 0.0, T['reply1'] + d + 0.03, 0.35) for d in T['reply1_step']]
ev += [('pop_es', 0.0, T['reels'] + k * T['reel_step'] + 0.03, 0.25) for k in range(len(CFG['more_reels']))]
ev += [('ding', 0.05, T['plan'] + 0.1, 0.5)]
hv = CFG.get('hook_vol', 1.0); he = T['hook_end']
# duck the clip's music under the first narration line
d0, d1, dv = CFG['vo_starts'][0] - 0.1, CFG['vo_starts'][0] + 1.3, CFG.get('hook_duck', 0.35)
inp = ['-i', f'{WD}/promo_silent.mp4', '-i', f'{WD}/src/viral.mp4']
fc = f"[1:a]atrim=0:{he + 0.6},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,volume='if(between(t,{d0},{d1}),{dv},{hv})':eval=frame,afade=t=out:st={he - 0.1}:d=0.6[hook];"
mix = ['[hook]']; n = 2
for i, st in enumerate(CFG['vo_starts'], 1):
    inp += ['-i', f'{WD}/vo/L{i}.wav']; ms = int(st * 1000)
    fc += f'[{n}:a]aresample=48000,aformat=channel_layouts=stereo,adelay={ms}|{ms}[v{i}];'; mix.append(f'[v{i}]'); n += 1
for k, (nm, po, t, v) in enumerate(ev):
    f = f'{SFX}/{nm}.wav'; inp += ['-i', f]; g = 10 ** ((-6 - peak_db(f)) / 20) * v; ms = max(0, int((t - po) * 1000))
    trim = 'atrim=0:0.45,asetpts=PTS-STARTPTS,afade=t=out:st=0.37:d=0.08,' if nm == 'ding' else ''
    fc += f'[{n}:a]{trim}aresample=48000,aformat=channel_layouts=stereo,volume={g:.4f},adelay={ms}|{ms}[s{k}];'; mix.append(f'[s{k}]'); n += 1
fc += ''.join(mix) + f'amix=inputs={len(mix)}:normalize=0:duration=longest,apad,atrim=0:{T["end"]},alimiter=limit=0.84:level=false[a]'
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y'] + inp + ['-filter_complex', fc, '-map', '0:v', '-map', '[a]', '-c:v', 'copy',
                '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', f'{WD}/promo_final.mp4'], check=True)
print('audio ok')
