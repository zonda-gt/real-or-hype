"""Render a free-places reel: render.py PLAN RAWDIR SONG.mp4 OUT.mp4
Cuts each shot to its slot, blurs/crops as planned, adds the text and the song, writes OUT.mp4 + OUT_540p.mp4,
then scans the result for unplanned cuts/flash frames."""
import sys, os, subprocess, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import CUTS, W, H, FPS, load_plan
import text
from PIL import Image
P = load_plan(sys.argv[1]); RAW, SONG, OUT = sys.argv[2], sys.argv[3], sys.argv[4]
work = OUT + '_work'; os.makedirs(work+'/seg', exist_ok=True); os.makedirs(work+'/ov', exist_ok=True)
F = [round(c*FPS) for c in CUTS]
F[-1] = round(float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', SONG], capture_output=True, text=True).stdout)*FPS)
segs = []
for i, (clip, t0, lab) in enumerate(P['shots']):
    n = F[i+1]-F[i]; out = f'{work}/seg/{i:02d}.mp4'; segs.append(out)
    vf = (P['precrop'][i]+',' if i in P['precrop'] else '') + (f'setpts=(PTS-STARTPTS)/{P["speed"][i]},' if i in P['speed'] else '') + \
         f'fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},setsar=1,tpad=stop_mode=clone:stop=6'
    fc = f'[0:v]{vf}[b0]'; last = 'b0'
    for k, (x, y, w, h) in enumerate(P['blur'].get(i, [])):
        fc += f';[{last}]split[m{k}][c{k}];[c{k}]crop={w}:{h}:{x}:{y},boxblur=lr=24:lp=3:cr=12:cp=3[bl{k}];[m{k}][bl{k}]overlay={x}:{y}[b{k+1}]'; last = f'b{k+1}'
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-ss', str(t0), '-i', f'{RAW}/{clip}.mp4', '-filter_complex', fc, '-map', f'[{last}]',
                    '-frames:v', str(n), '-an', '-c:v', 'libx264', '-crf', '14', '-preset', 'fast', '-pix_fmt', 'yuv420p', out], check=True)
    got = int(subprocess.run(['ffprobe', '-v', 'error', '-count_frames', '-select_streams', 'v:0', '-show_entries', 'stream=nb_read_frames', '-of', 'csv=p=0', out], capture_output=True, text=True).stdout)
    if got != n: sys.exit(f'shot {i+1}: {got} frames, needs {n} (clip too short from {t0}; move the in-point earlier)')
open(f'{work}/list.txt', 'w').write(''.join(f"file '{os.path.abspath(s)}'\n" for s in segs))
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', f'{work}/list.txt', '-c', 'copy', f'{work}/video.mp4'], check=True)
n = F[-1]; st = [None]*n
for f in range(F[0], F[2]): st[f] = ('hook',)
for i in range(2, 20, 2):
    for f in range(F[i], F[i+2]): st[f] = ('place', P['shots'][i][2], min(f-F[i], 9))
for f in range(F[20], n): st[f] = ('end', min(f-F[20], 9))
cache = {}; blank = Image.new('RGBA', (W, H), (0, 0, 0, 0))
for f, s in enumerate(st):
    if s not in cache:
        cache[s] = blank if s is None else text.hook(P['city']) if s[0] == 'hook' else text.place(s[1], s[2]) if s[0] == 'place' else text.cta(s[1])
    cache[s].save(f'{work}/ov/{f:05d}.png', compress_level=1)
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', f'{work}/video.mp4', '-framerate', str(FPS), '-i', f'{work}/ov/%05d.png', '-i', SONG,
    '-filter_complex', '[0:v][1:v]overlay=0:0:format=auto,format=yuv420p[v]', '-map', '[v]', '-map', '2:a', '-c:v', 'libx264', '-crf', '17', '-preset', 'medium',
    '-r', str(FPS), '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', OUT], check=True)
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', OUT, '-vf', 'scale=540:960', '-c:v', 'libx264', '-crf', '23', '-c:a', 'copy', OUT[:-4]+'_540p.mp4'], check=True)
# unplanned cuts / flash frames in the assembled picture
r = subprocess.run(['ffmpeg', '-hide_banner', '-i', f'{work}/video.mp4', '-vf', "select='gt(scene,0.3)',metadata=print", '-an', '-f', 'null', '-'], capture_output=True, text=True).stderr
cutf = set(F); odd = [float(t) for t in re.findall(r'pts_time:([0-9.]+)', r) if min(abs(round(float(t)*FPS)-c) for c in cutf) > 1]
print('DONE', OUT, '| unplanned cuts at', odd if odd else 'none')
