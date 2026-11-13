"""Posting history: history.py show | history.py add CITY PERMALINK MEDIA_ID 'Place 1|Place 2|...'"""
import sys, os, json, time
HF = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'history.json')
h = json.load(open(HF)) if os.path.exists(HF) else []
if sys.argv[1] == 'show':
    for e in h: print(e['date'], e['city'].ljust(10), e['permalink'], '|', ', '.join(e['places']))
    from collections import Counter; c = Counter(e['city'] for e in h)
    print('\nvideos per city:', dict(c))
else:
    _, _, city, link, mid, places = sys.argv
    h.append({'date': time.strftime('%Y-%m-%d'), 'city': city, 'permalink': link, 'media_id': mid, 'places': places.split('|')})
    json.dump(h, open(HF, 'w'), indent=1, ensure_ascii=False); print('added', city)
