import sys,os,json,time,subprocess
# usage: dysearch.py outdir key "关键词" [pages]
out,key,kw=sys.argv[1],sys.argv[2],sys.argv[3]; pages=int(sys.argv[4]) if len(sys.argv)>4 else 1
os.makedirs(out,exist_ok=True)
tok=os.environ['TIKHUB_API_KEY']
res=[];cursor=0;sid='';bt=''
for p in range(pages):
    body=json.dumps({"keyword":kw,"cursor":cursor,"sort_type":"1","publish_time":"0","filter_duration":"0-1","content_type":"1","search_id":sid,"backtrace":bt})
    for t in range(3):
        r=subprocess.run(['curl','-sS','-m','90','-X','POST','https://api.tikhub.io/api/v1/douyin/search/fetch_video_search_v2','-H',f'Authorization: Bearer {tok}','-H','Content-Type: application/json','-d',body],capture_output=True,text=True)
        try:
            d=json.loads(r.stdout)
            if d.get('code')==200: break
        except Exception: d={}
        time.sleep(3)
    data=(d.get('data') or {})
    for it in data.get('business_data') or []:
        a=(it.get('data') or {}).get('aweme_info')
        if not a: continue
        v=a['video']
        res.append(dict(id=a['aweme_id'],likes=a['statistics']['digg_count'],dur=v.get('duration',0)/1000,w=v.get('width'),h=v.get('height'),
            desc=a['desc'][:80].replace('\n',' '),url=v['play_addr']['url_list'],author=a['author'].get('nickname'),kw=kw))
    bc=data.get('business_config') or {}
    if not bc.get('has_more'): break
    np_=bc.get('next_page') or {}; cursor=np_.get('cursor',cursor+10); sid=np_.get('search_id',''); bt=bc.get('backtrace','')
json.dump(res,open(f'{out}/{key}.json','w'),ensure_ascii=False,indent=1)
for x in res: print(key,x['id'],x['likes'],f"{x['dur']:.0f}s",f"{x['w']}x{x['h']}",x['desc'][:45])
