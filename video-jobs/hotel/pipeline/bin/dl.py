"""Download Douyin clips (no-watermark play_addr) from saved raw search JSON. usage: dl.py id1 id2 ...  -> clips/<id>.mp4, meta/<id>.json"""
import sys,os,json,glob,requests
B=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
os.makedirs(B+'/clips',exist_ok=True); os.makedirs(B+'/meta',exist_ok=True)
idx={}
for f in glob.glob(B+'/data/raw_*.json')+glob.glob(B+'/meta/*.json'):
    d=json.load(open(f))
    if 'aweme_id' in d: idx[d['aweme_id']]=d; continue
    for it in ((d.get('data') or {}).get('business_data') or []):
        a=(it.get('data') or {}).get('aweme_info')
        if a: idx[a['aweme_id']]=a
H={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36','Referer':'https://www.douyin.com/'}
for i in sys.argv[1:]:
    a=idx.get(i)
    if not a: print(i,'not in index'); continue
    json.dump(a,open(f'{B}/meta/{i}.json','w'),ensure_ascii=False)
    out=f'{B}/clips/{i}.mp4'
    if os.path.exists(out) and os.path.getsize(out)>100000: print(i,'exists'); continue
    v=a['video']; urls=[]
    # watermark-free play addresses only (never download_addr). Prefer hevc/h264; reject ByteDance bvc2.
    for k in ['play_addr_265','play_addr_h264','play_addr']:
        urls+= (v.get(k) or {}).get('url_list',[])
    for br in sorted(v.get('bit_rate') or [],key=lambda b:-(b.get('bit_rate') or 0)):
        urls+= (br.get('play_addr') or {}).get('url_list',[])
    ok=False
    import subprocess
    for u in urls:
        try:
            r=requests.get(u,headers=H,timeout=120)
            if r.status_code==200 and len(r.content)>100000:
                open(out,'wb').write(r.content)
                c=subprocess.run(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=codec_name,width,height','-of','csv=p=0',out],capture_output=True,text=True).stdout.strip()
                if c.split(',')[0] in ('h264','hevc'):
                    print(i,'ok',c,len(r.content)//1024,'KB'); ok=True; break
                os.remove(out)
        except Exception as e: pass
    if not ok: print(i,'FAILED (expired? refresh with fetch_one_video)')
