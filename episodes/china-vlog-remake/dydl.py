# usage: dydl.py outdir id1 id2 ...  (download highest-quality Douyin videos + contact sheets)
import json, sys, os, subprocess
from concurrent.futures import ThreadPoolExecutor
out = sys.argv[1]; os.makedirs(out + '/sheets', exist_ok=True)
def one(i):
    fn = f'{out}/{i}.mp4'
    if not os.path.exists(fn) or os.path.getsize(fn) < 10000:
        r = subprocess.run(['curl', '-sS', f'https://api.tikhub.io/api/v1/douyin/app/v3/fetch_video_high_quality_play_url?aweme_id={i}',
                            '-H', 'Authorization: Bearer dummy'], capture_output=True, text=True)
        try: u = json.loads(r.stdout)['data']['original_video_url']
        except Exception: return f'{i} NOURL {r.stdout[:200]}'
        subprocess.run(['curl', '-sSL', '-A', 'Mozilla/5.0', '-e', 'https://www.douyin.com/', '-o', fn, u])
    p = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height,r_frame_rate:format=duration',
                        '-of', 'csv=p=0', fn], capture_output=True, text=True).stdout.split()
    dur = float(p[-1]) if p else 0
    n = max(1, int(dur)); cols = 8; rows = (n + cols - 1) // cols
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', fn, '-vf', f'fps=1,scale=240:-2,tile={cols}x{rows}', '-frames:v', '1',
                    f'{out}/sheets/{i}.jpg'])
    return f'{i} {" ".join(p)}'
with ThreadPoolExecutor(4) as ex:
    for r in ex.map(one, sys.argv[2:]): print(r, flush=True)
