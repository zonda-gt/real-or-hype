import json,subprocess,sys,os,concurrent.futures as cf
sp=sys.argv[1]; os.chdir(sp)
AT=open('.alipan_at').read().strip(); ST=open('share_token.txt').read().strip()
files=[f for f in json.load(open('all_files.json')) if f.get('category')=='video']
def api(fid):
    body=json.dumps({"share_id":"e3FxGyLuAo8","file_id":fid,"category":"live_transcoding","template_id":"","get_preview_url":True})
    r=subprocess.run(['curl','-sS','-m','40','-X','POST','https://api.alipan.com/v2/file/get_share_link_video_preview_play_info',
      '-H','Content-Type: application/json','-H','Referer: https://www.alipan.com/','-H','Origin: https://www.alipan.com',
      '-H','Authorization: Bearer '+AT,'-H','x-share-token: '+ST,'-d',body],capture_output=True,text=True)
    return json.loads(r.stdout)
def work(f):
    name=os.path.splitext(f['name'])[0]; out=f'prev/{name}.mp4'
    if os.path.exists(out) and os.path.getsize(out)>10000: return name,'skip',None
    for attempt in range(3):
        try:
            info=api(f['file_id'])['video_preview_play_info']
            dur=info['meta']['duration']
            tasks=[t for t in info['live_transcoding_task_list'] if t.get('status')=='finished' and t.get('preview_url')]
            t=sorted(tasks,key=lambda t:t['template_height'])[0]
            r=subprocess.run(['ffmpeg','-loglevel','error','-y','-headers','Referer: https://www.alipan.com/\r\n','-i',t['preview_url'],'-c','copy','-bsf:a','aac_adtstoasc',out],capture_output=True,text=True,timeout=900)
            if r.returncode==0: return name,'ok',dur
            err=r.stderr[-200:]
        except Exception as e: err=str(e)[:200]
    return name,'fail',err
res={}
with cf.ThreadPoolExecutor(6) as ex:
    for name,st,x in ex.map(work,files):
        res[name]=(st,x); print(name,st,x,flush=True)
json.dump(res,open('prev_status.json','w'))
print('ALLDONE')
