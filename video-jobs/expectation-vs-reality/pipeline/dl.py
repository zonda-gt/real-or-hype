#!/usr/bin/env python3
# dl.py : download every aweme found in api/s_*.json and api/one_*.json into media/dy/<id>.mp4 (watermark-free play addr, best res)
import json,glob,os,subprocess,sys
from concurrent.futures import ThreadPoolExecutor
S=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.makedirs(S+'/media/dy',exist_ok=True)
aw={}
for f in glob.glob(S+'/api/s_*.json')+glob.glob(S+'/api/one_*.json'):
    d=json.load(open(f))
    dd=d.get('data') or {}
    lst=[(it.get('data') or {}).get('aweme_info') for it in dd.get('business_data') or []]
    if dd.get('aweme_detail'): lst.append(dd['aweme_detail'])
    for a in lst:
        if a: aw[a['aweme_id']]=a
meta={}
def urls(a):
    v=a['video']; c=[]
    for b in sorted(v.get('bit_rate') or [], key=lambda b:(-(b['play_addr'].get('width') or 0)*(b['play_addr'].get('height') or 0), -b.get('bit_rate',0))):
        c+=b['play_addr']['url_list']
    c+=v['play_addr']['url_list']
    h=(v.get('play_addr_h264') or {}).get('url_list') or []
    return h+c
def ok(out):
    r=subprocess.run(['ffmpeg','-v','error','-ss','1','-i',out,'-frames:v','1','-f','null','-'],capture_output=True)
    return r.returncode==0
def go(i):
    a=aw[i]; out=f"{S}/media/dy/{i}.mp4"
    if os.path.exists(out) and os.path.getsize(out)>10000 and ok(out): return i,'have'
    for u in urls(a):
        r=subprocess.run(['curl','-sS','-L','-f','-m','60','-o',out,'-A','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36','-e','https://www.douyin.com/',u],capture_output=True)
        if r.returncode==0 and os.path.getsize(out)>10000 and ok(out): return i,'ok'
    return i,'FAIL'
ids=[i for i,a in aw.items() if a['video'].get('duration',0)<=65000] if len(sys.argv)<2 else sys.argv[1:]
with ThreadPoolExecutor(6) as ex:
    for i,s in ex.map(go,ids): 
        if s!='have': print(i,s)
for i,a in aw.items():
    meta[i]={'id':i,'desc':a.get('desc',''),'author':a['author'].get('nickname'),'unique_id':a['author'].get('unique_id') or a['author'].get('short_id'),'sec_uid':a['author'].get('sec_uid'),'fans':a['author'].get('follower_count'),'likes':a['statistics'].get('digg_count'),'dur':a['video'].get('duration'),'create_time':a.get('create_time'),'link':f"https://www.douyin.com/video/{i}"}
json.dump(meta,open(S+'/api/meta.json','w'),ensure_ascii=False,indent=1)
print(len(aw),'awemes')
