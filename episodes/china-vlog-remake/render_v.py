# Render each slot as a graded 1080x1920@30 (9:16) segment with an exact frame count.
import sys, os, subprocess
sys.path.insert(0, os.path.dirname(__file__)); from plan_v import CUTS, SHOTS, HLG, CROP
RAW = os.path.join(os.path.dirname(__file__), '..', 'vraw'); OUT = os.path.join(os.path.dirname(__file__), 'segs_v')
os.makedirs(OUT, exist_ok=True)
FPS = 30
# Look modelled on the reference: contrast with slightly lifted blacks, rolled-off highlights,
# warm highlights / teal shadows, a touch less saturation, soft vignette.
GRADE = ("curves=master='0/0.035 0.25/0.21 0.5/0.5 0.8/0.79 1/0.86',"
         "colorbalance=rs=-0.04:gs=0.0:bs=0.05:rh=0.05:gh=0.01:bh=-0.05,"
         "eq=saturation=0.92,vignette=angle=PI/5.5")
TONEMAP = ("zscale=tin=arib-std-b67:min=bt2020nc:pin=bt2020:t=linear:npl=100,format=gbrpf32le,"
           "zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p,")
def render(k, grade=True):
    i, s, sp, lab = SHOTS[k]
    n = round(CUTS[k + 1] * FPS) - round(CUTS[k] * FPS)
    src_dur = n / FPS * sp + 0.2
    vf = TONEMAP if i in HLG else ''
    vf += f'setpts=(PTS-STARTPTS)/{sp},fps={FPS},'
    if i in CROP:
        z, ax, ay = CROP[i]
        vf += f'scale={int(1080*z)}:{int(1920*z)}:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920:(iw-1080)*{ax}:(ih-1920)*{ay},'
    else:
        vf += 'scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,'
    vf += 'setsar=1,format=yuv420p'
    if grade: vf += ',' + GRADE
    out = f'{OUT}/seg{k:02d}.mp4'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{s:.3f}', '-t', f'{src_dur:.3f}', '-i', f'{RAW}/{i}.mp4',
                    '-vf', vf, '-frames:v', str(n), '-an', '-c:v', 'libx264', '-crf', '14', '-preset', 'medium',
                    '-pix_fmt', 'yuv420p', '-r', str(FPS), out], check=True)
    got = subprocess.run(['ffprobe', '-v', 'error', '-count_frames', '-select_streams', 'v:0', '-show_entries', 'stream=nb_read_frames',
                          '-of', 'csv=p=0', out], capture_output=True, text=True).stdout.strip()
    print(k, lab, 'frames', got, '/', n, flush=True)
if __name__ == '__main__':
    ks = [int(x) for x in sys.argv[1:]] or range(len(SHOTS))
    for k in ks: render(k)
