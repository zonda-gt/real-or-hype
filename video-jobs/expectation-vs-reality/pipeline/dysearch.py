#!/usr/bin/env python3
# dysearch.py "keyword" [v2|v3] [sort] [pubtime] -> prints compact table, saves api/s_<kw>.json and appends to api/catalog.jsonl
import sys,json,subprocess,os,hashlib
S=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
kw=sys.argv[1]; ver=sys.argv[2] if len(sys.argv)>2 else 'v2'; sort=sys.argv[3] if len(sys.argv)>3 else '1'; pt=sys.argv[4] if len(sys.argv)>4 else '180'
body={"keyword":kw,"cursor":0,"sort_type":sort,"publish_time":pt,"filter_duration":"0-1","content_type":"1","search_id":"","backtrace":""}
if ver=='v3': body["label_type"]=1
name='s_'+ver+'_'+hashlib.md5((kw+sort+pt).encode()).hexdigest()[:8]
p=subprocess.run([sys.executable,os.path.join(S,'bin/th.py'),'POST',f'/api/v1/douyin/search/fetch_video_search_{ver}',json.dumps(body,ensure_ascii=False),name],capture_output=True,text=True).stdout.strip()
d=json.load(open(p))
items=(d.get('data') or {}).get('business_data') or []
cat=open(os.path.join(S,'api','catalog.jsonl'),'a')
n=0
for it in items:
    a=(it.get('data') or {}).get('aweme_info')
    if not a: continue
    n+=1
    st=a.get('statistics',{}); au=a.get('author',{}); v=a.get('video',{})
    rec={'kw':kw,'id':a['aweme_id'],'desc':a.get('desc','').replace('\n',' ')[:90],'author':au.get('nickname'),'uid':au.get('sec_uid'),'fans':au.get('follower_count'),'likes':st.get('digg_count'),'shares':st.get('share_count'),'collect':st.get('collect_count'),'dur':round(v.get('duration',0)/1000,1),'w':v.get('width'),'h':v.get('height'),'ct':a.get('create_time'),'cover':(v.get('cover') or {}).get('url_list',[None])[0],'ad':bool(a.get('is_ads')) }
    cat.write(json.dumps(rec,ensure_ascii=False)+'\n')
    print(f"{rec['id']} {rec['likes']:>7} 赞 fans={rec['fans']} {rec['dur']}s {rec['w']}x{rec['h']} | {rec['author']} | {rec['desc']}")
print('n=',n, 'keys:', list((d.get('data') or {}).keys())[:8] if isinstance(d.get('data'),dict) else d.get('detail') or d.get('message'))
