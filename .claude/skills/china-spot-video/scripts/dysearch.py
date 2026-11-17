# Douyin video search via TikHub. usage: dysearch.py "<keyword>" <out.json> [sort: 0 relevance | 1 most likes | 2 newest]
# Prints: aweme_id  likes  seconds  WxH  caption. TikHub sits behind Cloudflare: a browser User-Agent is required (else 403 / error 1010).
import sys,json,os,urllib.request
kw,out=sys.argv[1],sys.argv[2]; sort=sys.argv[3] if len(sys.argv)>3 else "1"
body=json.dumps({"keyword":kw,"cursor":0,"sort_type":sort,"publish_time":"0","filter_duration":"0","content_type":"1","search_id":"","backtrace":""}).encode()
req=urllib.request.Request("https://api.tikhub.io/api/v1/douyin/search/fetch_video_search_v2",data=body,
    headers={"Authorization":"Bearer "+os.environ.get("TIKHUB_API_KEY","x"),"Content-Type":"application/json","User-Agent":"Mozilla/5.0 (X11; Linux x86_64) Chrome/124 Safari/537.36"})
try: d=json.load(urllib.request.urlopen(req,timeout=90))
except urllib.error.HTTPError as e: print('ERR',e.code,e.read()[:300]); sys.exit(1)
json.dump(d,open(out,'w'),ensure_ascii=False)
def walk(o):
    if isinstance(o,dict):
        if 'aweme_id' in o and 'statistics' in o: yield o
        else:
            for v in o.values(): yield from walk(v)
    elif isinstance(o,list):
        for v in o: yield from walk(v)
for a in walk(d):
    s=a.get('statistics',{}); v=a.get('video',{})
    print(a['aweme_id'], s.get('digg_count'), round((v.get('duration') or 0)/1000,1), f"{v.get('width')}x{v.get('height')}", (a.get('desc') or '')[:80].replace('\n',' '))
