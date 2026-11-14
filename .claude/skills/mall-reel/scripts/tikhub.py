# Douyin / TikTok search and download through TikHub (api.tikhub.io; key in $TIKHUB_API_KEY, the proxy may inject it).
# Prices (Nov 2026): Douyin search v2 $0.01 per call (the main cost), single-video fetch $0.001, TikTok search $0.001.
#
#   search  <out.json> "<keyword>" [--sort 0|1|2] [--days 0|1|7|180] [--dur 0|0-1|1-5]   Douyin video search (8 results/call)
#   tsearch <out.json> "<keyword>"                                                       TikTok video search (~20 results)
#   list    <json ...> [--days N]                     table of results: id, likes, length, size, date, author, description
#   descs   <json ...> [--days N] [--top N]          full descriptions, most-liked first (shop names live here)
#   preview <outdir> <json-glob> <id ...>            download the search-result stream (576-720p H.264) for triage
#   hd      <outdir> <id ...>                        best decodable stream: 1080p HEVC if offered, else 720p H.264
#
# sort: 0 = relevance, 1 = most liked, 2 = newest. dur "0-1" = under 1 minute (b-roll-ish clips).
import sys, os, json, glob, time, subprocess, urllib.request, urllib.parse

KEY = os.environ.get('TIKHUB_API_KEY', 'x')
API = 'https://api.tikhub.io'
UA = 'curl/8.5.0'   # urllib's default User-Agent gets 403 from TikHub


def call(path, body=None, params=''):
    req = urllib.request.Request(API + path + (('?' + params) if params else ''), data=json.dumps(body).encode() if body else None,
                                 headers={'Authorization': f'Bearer {KEY}', 'Content-Type': 'application/json', 'User-Agent': UA})
    for k in range(3):
        try: return json.load(urllib.request.urlopen(req, timeout=120))
        except Exception as e: print('retry', e, file=sys.stderr); time.sleep(3)
    raise SystemExit('TikHub call failed: ' + path)


def awemes(files):
    seen = {}
    for f in files:
        try: d = json.load(open(f))
        except Exception: continue
        data = d.get('data') or {}
        for b in data.get('business_data') or []:              # Douyin search
            a = (b.get('data') or {}).get('aweme_info')
            if a: seen[a['aweme_id']] = a
        for it in data.get('search_item_list') or []:          # TikTok search
            a = it.get('aweme_info') or it
            if a.get('aweme_id'): seen[a['aweme_id']] = a
    return seen


def arg(flag, default):
    return sys.argv[sys.argv.index(flag) + 1] if flag in sys.argv else default


def recent(a, days):
    return days <= 0 or a.get('create_time', 0) > time.time() - days * 86400


cmd = sys.argv[1]
if cmd == 'search':
    out, kw = sys.argv[2], sys.argv[3]
    d = call('/api/v1/douyin/search/fetch_video_search_v2', {'keyword': kw, 'cursor': 0, 'sort_type': arg('--sort', '1'),
             'publish_time': arg('--days', '180'), 'filter_duration': arg('--dur', '0'), 'content_type': '1'})
    json.dump(d, open(out, 'w'), ensure_ascii=False); print(out, len(awemes([out])), 'videos')
elif cmd == 'tsearch':
    out, kw = sys.argv[2], sys.argv[3]
    d = call('/api/v1/tiktok/app/v3/fetch_video_search_result', params='keyword=' + urllib.parse.quote(kw) + '&offset=0&count=20&sort_type=0&publish_time=0')
    json.dump(d, open(out, 'w'), ensure_ascii=False); print(out, len(awemes([out])), 'videos')
elif cmd in ('list', 'descs'):
    files = [a for a in sys.argv[2:] if not a.startswith('--') and not a.isdigit()]
    days = int(arg('--days', '0')); top = int(arg('--top', '40'))
    L = sorted([a for a in awemes(files).values() if recent(a, days)], key=lambda a: -a['statistics']['digg_count'])
    for a in L[:top]:
        v = a['video']; dur = (a.get('duration') or v.get('duration') or 0) // 1000
        date = time.strftime('%Y-%m', time.gmtime(a.get('create_time', 0)))
        if cmd == 'list':
            print(a['aweme_id'], a['statistics']['digg_count'], f'{dur}s', f"{v.get('width')}x{v.get('height')}", date,
                  (a.get('author') or {}).get('nickname', '')[:10], '|', a.get('desc', '')[:70].replace('\n', ' '))
        else:
            print(a['statistics']['digg_count'], date, '|', a.get('desc', '').replace('\n', ' ')[:500]); print()
elif cmd == 'preview':
    outdir, pattern, ids = sys.argv[2], sys.argv[3], sys.argv[4:]
    os.makedirs(outdir, exist_ok=True); A = awemes(glob.glob(pattern))
    for i in ids:
        a = A.get(i)
        if not a: print(i, 'not in search results'); continue
        v = a['video']; x = v.get('play_addr_h264') or v['play_addr']
        subprocess.run(['curl', '-sS', '-L', '--max-time', '120', '-A', 'Mozilla/5.0', '-o', f'{outdir}/{i}.mp4', x['url_list'][0]])
        print(i, os.path.getsize(f'{outdir}/{i}.mp4'))
elif cmd == 'hd':
    outdir, ids = sys.argv[2], sys.argv[3:]; os.makedirs(outdir, exist_ok=True)
    for i in ids:
        if os.path.exists(f'{outdir}/{i}.mp4'): continue
        v = call('/api/v1/douyin/app/v3/fetch_one_video', params=f'aweme_id={i}')['data']['aweme_detail']['video']
        # is_h265: 0 = H.264, 1 = HEVC (ffmpeg decodes both), 2 = ByteVC2 (ffmpeg CANNOT decode, skip)
        brs = sorted([b for b in v.get('bit_rate') or [] if b.get('is_h265') in (0, 1)],
                     key=lambda b: (b['play_addr'].get('height', 0) * b['play_addr'].get('width', 0), b.get('bit_rate', 0)), reverse=True)
        cands = [b['play_addr']['url_list'][0] for b in brs] + [(v.get('play_addr_h264') or v['play_addr'])['url_list'][0]]
        ok = False
        for u in cands:
            subprocess.run(['curl', '-sS', '-L', '--max-time', '180', '-o', f'{outdir}/{i}.mp4', u])
            t = subprocess.run(['ffmpeg', '-v', 'error', '-i', f'{outdir}/{i}.mp4', '-frames:v', '5', '-f', 'null', '-'], capture_output=True, text=True)
            p = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=codec_name,width,height', '-of', 'csv=p=0', f'{outdir}/{i}.mp4'], capture_output=True, text=True).stdout.strip()
            if p and not t.stderr.strip(): print(i, p); ok = True; break
        if not ok: print(i, 'FAILED')
