"""Fetch HD (no-watermark play_addr) via fetch_one_video. usage: dl_hd.py id...  -> hd/<id>.mp4, data/one_<id>.json"""
import sys,os,json,subprocess,requests
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); import th
B=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'); os.makedirs(B+'/hd',exist_ok=True)
H={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36','Referer':'https://www.douyin.com/'}
for i in sys.argv[1:]:
    out=f'{B}/hd/{i}.mp4'
    if os.path.exists(out): print(i,'exists'); continue
    jf=f'{B}/data/one_{i}.json'
    d=json.load(open(jf)) if os.path.exists(jf) else th.call('GET','/api/v1/douyin/app/v3/fetch_one_video',{'aweme_id':i})
    json.dump(d,open(jf,'w'),ensure_ascii=False)
    a=d['data'].get('aweme_detail') or d['data']; v=a['video']
    cands=[]
    for b in sorted(v.get('bit_rate') or [],key=lambda b:-((b.get('play_addr') or {}).get('width',0)*(b.get('play_addr') or {}).get('height',0)+ (b.get('bit_rate') or 0)/1e7)):
        cands+=(b.get('play_addr') or {}).get('url_list',[])
    for k in ['play_addr_265','play_addr_h264','play_addr']: cands+=(v.get(k) or {}).get('url_list',[])
    ok=False
    for u in cands:
        try:
            r=requests.get(u,headers=H,timeout=180)
            if r.status_code!=200 or len(r.content)<100000: continue
            open(out,'wb').write(r.content)
            c=subprocess.run(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=codec_name,width,height','-of','csv=p=0',out],capture_output=True,text=True).stdout.strip()
            if c.split(',')[0] in ('h264','hevc'): print(i,'ok',c,len(r.content)//1024,'KB'); ok=True; break
            os.remove(out)
        except Exception as e: pass
    if not ok: print(i,'FAILED')
