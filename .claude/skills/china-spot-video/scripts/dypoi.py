# Find the shop address behind a name: Douyin video search -> location tags (POI) with full addresses.
# usage: dypoi.py "<shop or experience keyword>" [pages=2]
# Prints each distinct POI: videos | top likes | poi_name | district | address | lng,lat ; then the top captions.
import sys,json,os,urllib.request,collections
kw=sys.argv[1]; pages=int(sys.argv[2]) if len(sys.argv)>2 else 2
H={"Authorization":"Bearer "+os.environ.get("TIKHUB_API_KEY","x"),"Content-Type":"application/json","User-Agent":"Mozilla/5.0 (X11; Linux x86_64) Chrome/124 Safari/537.36"}
def walk(o):
    if isinstance(o,dict):
        if 'aweme_id' in o and 'statistics' in o: yield o
        else:
            for v in o.values(): yield from walk(v)
    elif isinstance(o,list):
        for v in o: yield from walk(v)
cursor,sid,bt=0,"",""; vids=[]
for p in range(pages):
    body=json.dumps({"keyword":kw,"cursor":cursor,"sort_type":"0","publish_time":"0","filter_duration":"0","content_type":"1","search_id":sid,"backtrace":bt}).encode()
    try: d=json.load(urllib.request.urlopen(urllib.request.Request("https://api.tikhub.io/api/v1/douyin/search/fetch_video_search_v2",data=body,headers=H),timeout=90))
    except Exception as e: print('ERR',e); break
    vids+=list(walk(d))
    bc=d.get('data',{}).get('business_config',{})
    if not bc.get('has_more'): break
    cursor=bc.get('next_page',{}).get('cursor',cursor+10); sid=bc.get('next_page',{}).get('search_id',''); bt=bc.get('backtrace','')
pois=collections.OrderedDict()
for a in vids:
    p=a.get('poi_info') or {}
    if not p.get('poi_name'): continue
    ai=p.get('address_info') or {}
    k=p['poi_name']
    e=pois.setdefault(k,{'n':0,'likes':0,'district':ai.get('district',''),'city':ai.get('city',''),'addr':ai.get('address',''),'ll':f"{p.get('poi_longitude')},{p.get('poi_latitude')}",'ids':[]})
    e['n']+=1; l=a.get('statistics',{}).get('digg_count') or 0
    if l>e['likes']: e['likes']=l
    e['ids'].append(a['aweme_id'])
print(f"## {kw}: {len(vids)} videos, {len(pois)} POIs")
for k,e in sorted(pois.items(),key=lambda x:-x[1]['n']):
    if e['city'] and '上海' not in e['city']: continue
    print(f"POI {e['n']}v {e['likes']}♥ | {k} | {e['district']} | {e['addr']} | {e['ll']} | ids {','.join(e['ids'][:2])}")
for a in sorted(vids,key=lambda a:-(a.get('statistics',{}).get('digg_count') or 0))[:6]:
    print(f"  [{a['aweme_id']}] {a.get('statistics',{}).get('digg_count')}♥ poi:{(a.get('poi_info') or {}).get('poi_name','')} | {(a.get('desc') or '').replace(chr(10),' ')[:120]}")
