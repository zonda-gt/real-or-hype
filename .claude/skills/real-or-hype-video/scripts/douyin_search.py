# douyin_search.py "<关键词>" out.json [sort: 0=relevance 1=likes 2=latest]  (TikHub, clips under 1 min)
import sys,json,requests,os
kw=sys.argv[1]; out=sys.argv[2]; sort=sys.argv[3] if len(sys.argv)>3 else '1'
r=requests.post('https://api.tikhub.io/api/v1/douyin/search/fetch_video_search_v2',headers={'Authorization':'Bearer x'},
  json={'keyword':kw,'cursor':0,'sort_type':sort,'publish_time':'0','filter_duration':'0-1','content_type':'1'},timeout=90)
j=r.json(); json.dump(j,open(out,'w'),ensure_ascii=False)
def walk(o):
    if isinstance(o,dict):
        if 'aweme_id' in o and 'video' in o: yield o
        else:
            for v in o.values(): yield from walk(v)
    elif isinstance(o,list):
        for v in o: yield from walk(v)
seen=set()
for a in walk(j.get('data')):
    if a['aweme_id'] in seen: continue
    seen.add(a['aweme_id'])
    v=a['video']; st=a.get('statistics',{})
    print(a['aweme_id'], f"{v.get('width')}x{v.get('height')}", round(v.get('duration',0)/1000,1),'s','likes',st.get('digg_count'), (a.get('desc') or '')[:70].replace('\n',' '))
print(r.status_code, j.get('message','')[:80] if not seen else '')
