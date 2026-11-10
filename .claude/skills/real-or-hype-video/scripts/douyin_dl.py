# douyin_dl.py <dir> <aweme_id>...  H.264/HEVC up to 1080p via TikHub web/fetch_one_video (skips ByteDance bvc2, which ffmpeg cannot decode)
import sys,json,subprocess,os,requests,time
outdir=sys.argv[1]
def walk(o):
    if isinstance(o,dict):
        if 'aweme_id' in o and 'video' in o: yield o
        else:
            for v in o.values(): yield from walk(v)
    elif isinstance(o,list):
        for v in o: yield from walk(v)
for i in sys.argv[2:]:
    for tries in range(3):
        try:
            j=requests.get('https://api.tikhub.io/api/v1/douyin/web/fetch_one_video',params={'aweme_id':i},headers={'Authorization':'Bearer x'},timeout=90).json()
            a=next(walk(j.get('data'))); break
        except Exception as e: print('retry',i,e); time.sleep(3)
    else: print(i,'META FAIL'); continue
    json.dump(a,open(os.path.join(outdir,f'{i}.meta.json'),'w'),ensure_ascii=False)
    v=a['video']; c=[]
    for b in v.get('bit_rate') or []:
        if b.get('is_bytevc1') not in (0,1): continue
        pa=b['play_addr']; px=pa.get('width',0)*pa.get('height',0)
        if px>1920*1080: continue
        c.append((px, b.get('is_h265')==0, b.get('bit_rate',0), pa['url_list']))
    c.sort(reverse=True)
    out=os.path.join(outdir,f'{i}.mp4')
    ok=False
    for px,h264,br,urls in c:
        for u in urls:
            r=subprocess.run(['curl','-sSL','--max-time','180','-A','Mozilla/5.0','-e','https://www.douyin.com/','-o',out,u])
            p=subprocess.run(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=codec_name,width,height,duration','-of','csv=p=0',out],capture_output=True,text=True).stdout.strip()
            if r.returncode==0 and p and 'unknown' not in p:
                print(i,p,os.path.getsize(out)//1024,'KB',(a.get('desc') or '')[:40].replace('\n',' '),'@'+a.get('author',{}).get('nickname',''));ok=True;break
        if ok: break
    if not ok: print(i,'DL FAIL')
