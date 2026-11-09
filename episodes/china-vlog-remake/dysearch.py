import json, sys, time, urllib.request, os
OUT = sys.argv[1]
kws = sys.argv[2:]
def post(path, body):
    req = urllib.request.Request("https://api.tikhub.io" + path, data=json.dumps(body).encode(),
        headers={"Authorization": "Bearer dummy", "Content-Type": "application/json", "User-Agent": "curl/8.5.0"})
    for i in range(3):
        try:
            return json.load(urllib.request.urlopen(req, timeout=90))
        except Exception as e:
            print("retry", e, file=sys.stderr); time.sleep(3)
    return {}
def walk(o):
    if isinstance(o, dict):
        if 'aweme_id' in o and 'video' in o: yield o; return
        for v in o.values(): yield from walk(v)
    elif isinstance(o, list):
        for v in o: yield from walk(v)
for kw in kws:
    fn = os.path.join(OUT, kw.replace(' ', '_') + '.json')
    if os.path.exists(fn): continue
    r = post('/api/v1/douyin/search/fetch_video_search_v2', {"keyword": kw, "cursor": 0, "sort_type": "0", "publish_time": "0",
            "filter_duration": "0-1", "content_type": "1", "search_id": "", "backtrace": ""})
    res = []
    for a in walk(r.get('data', {})):
        v = a['video']; pa = v.get('play_addr') or {}
        brs = sorted(v.get('bit_rate') or [], key=lambda b: -(b.get('play_addr', {}).get('height') or 0) * 10 - (b.get('play_addr', {}).get('width') or 0))
        best = brs[0]['play_addr'] if brs else pa
        res.append(dict(id=a['aweme_id'], desc=a.get('desc', '')[:80], w=pa.get('width') or v.get('width'), h=pa.get('height') or v.get('height'),
             bw=best.get('width'), bh=best.get('height'), dur=round((v.get('duration') or 0) / 1000, 1),
             likes=(a.get('statistics') or {}).get('digg_count'), author=(a.get('author') or {}).get('nickname'),
             url=(best.get('url_list') or pa.get('url_list') or [None])[0], cover=((v.get('cover') or {}).get('url_list') or [None])[0]))
    json.dump(res, open(fn, 'w'), ensure_ascii=False)
    land = [x for x in res if (x['bw'] or x['w'] or 0) > (x['bh'] or x['h'] or 1)]
    print(kw, 'results', len(res), 'landscape', len(land), flush=True)
