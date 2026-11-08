"""Build sources.csv from the beats logs of the final renders. usage: sources.py out.csv A:beats.json B:beats.json ..."""
import sys, json, csv, time, os
B = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
rows = {}
for arg in sys.argv[2:]:
    ver, path = arg.split(':', 1)
    for b in json.load(open(path)):
        for sh in b['shots']:
            sp = sh.get('speed', 1.0)
            used = 0.05 if sh.get('freeze') else b['dur'] * sp
            r = rows.setdefault(sh['clip'], {'segs': []})
            r['segs'].append((ver, sh['t'], sh['t'] + used))
with open(sys.argv[1], 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['aweme_id', 'link', 'author', 'douyin_id', 'posted', 'hotel_or_place', 'used_in_versions', 'source_seconds_used', 'source_ranges_used'])
    for cid, r in rows.items():
        j = json.load(open(f'{B}/data/one_{cid}.json'))['data']
        a = j.get('aweme_detail') or j
        au = a['author']
        poi = (a.get('poi_info') or {}).get('poi_name', '') if isinstance(a.get('poi_info'), dict) else ''
        if not poi and os.path.exists(f'{B}/meta/{cid}.json'):
            m = json.load(open(f'{B}/meta/{cid}.json')); poi = (m.get('poi_info') or {}).get('poi_name', '') if isinstance(m.get('poi_info'), dict) else ''
        # merge overlapping ranges to count unique source seconds
        iv = sorted((s, e) for _, s, e in r['segs']); merged = []
        for s, e in iv:
            if merged and s <= merged[-1][1]: merged[-1][1] = max(merged[-1][1], e)
            else: merged.append([s, e])
        secs = sum(e - s for s, e in merged)
        vers = sorted(set(v for v, _, _ in r['segs']))
        w.writerow([cid, f'https://www.douyin.com/video/{cid}', au.get('nickname'), au.get('unique_id') or au.get('short_id'),
                    time.strftime('%Y-%m-%d', time.localtime(a['create_time'])), poi, ' '.join(vers), round(secs, 1),
                    '; '.join(f'{s:.1f}-{e:.1f}s' for s, e in merged)])
print('wrote', sys.argv[1], len(rows), 'clips')
