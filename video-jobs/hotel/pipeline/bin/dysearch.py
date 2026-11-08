"""Douyin search -> appends compact rows to data/dy_hits.jsonl. usage: dysearch.py "<kw>" [v2|v3] [sort] [publish_time]"""
import sys,json,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import th
kw=sys.argv[1]; ver=sys.argv[2] if len(sys.argv)>2 else 'v2'; sort=sys.argv[3] if len(sys.argv)>3 else '1'; pt=sys.argv[4] if len(sys.argv)>4 else '180'
body={"keyword":kw,"cursor":0,"sort_type":sort,"publish_time":pt,"filter_duration":"0-1","content_type":"1","search_id":"","backtrace":""}
if ver=='v3': body['label_type']=1
d=th.call('POST',f'/api/v1/douyin/search/fetch_video_search_{ver}',body)
D=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','data')
json.dump(d,open(f'{D}/raw_{ver}_{kw}.json','w'),ensure_ascii=False)
items=(d.get('data') or {}).get('business_data') or []
n=0
with open(f'{D}/dy_hits.jsonl','a') as f:
    for it in items:
        a=((it.get('data') or {}).get('aweme_info'))
        if not a: continue
        st=a.get('statistics',{}); au=a.get('author',{})
        row=dict(kw=kw,id=a['aweme_id'],desc=a.get('desc','')[:160],author=au.get('nickname'),uid=au.get('unique_id') or au.get('short_id'),sec_uid=au.get('sec_uid'),fans=au.get('follower_count'),
                 dur=round(a.get('video',{}).get('duration',0)/1000,1),likes=st.get('digg_count'),shares=st.get('share_count'),saves=st.get('collect_count'),comments=st.get('comment_count'),
                 t=a.get('create_time'),ad=bool(a.get('is_ads') or a.get('commerce_info',{}).get('ad_source') if isinstance(a.get('commerce_info'),dict) else a.get('is_ads')),
                 poi=(a.get('poi_info') or {}).get('poi_name') if isinstance(a.get('poi_info'),dict) else None,
                 w=a.get('video',{}).get('width'),h=a.get('video',{}).get('height'))
        f.write(json.dumps(row,ensure_ascii=False)+'\n'); n+=1
        print(f"{row['likes']:>7} sh{row['shares']:>6} sv{row['saves']:>6} {row['dur']:>5}s {row['author'][:12]:12} | {row['poi'] or '':14.14} | {row['desc'][:90]}")
print(kw,'->',n)
