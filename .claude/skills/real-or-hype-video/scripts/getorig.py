import json,subprocess,sys,os,concurrent.futures as cf
os.chdir(sys.argv[1])
AT=open('.alipan_at').read().strip()
sel=sys.argv[2].split(',')
files={os.path.splitext(f['name'])[0]:f for f in json.load(open('all_files.json'))}
def short(n): return n
def work(n):
    f=files[n]; ext=os.path.splitext(f['name'])[1]; out=f'orig/{n}{ext}'
    if os.path.exists(out) and os.path.getsize(out)==f['size']: return n,'skip'
    for a in range(3):
        r=subprocess.run(['curl','-sS','-m','30','-X','POST','https://api.alipan.com/v2/file/get_download_url','-H','Content-Type: application/json','-H','Referer: https://www.alipan.com/','-H','Authorization: Bearer '+AT,'-d',json.dumps({"drive_id":f['drive_id'],"file_id":f['file_id'],"expire_sec":3600})],capture_output=True,text=True)
        try: url=json.loads(r.stdout)['url']
        except Exception: continue
        subprocess.run(['curl','-sS','-m','1200','-H','Referer: https://www.alipan.com/','-o',out,url])
        if os.path.exists(out) and os.path.getsize(out)==f['size']: return n,'ok'
    return n,'fail'
with cf.ThreadPoolExecutor(4) as ex:
    for n,s in ex.map(work,sel): print(n,s,flush=True)
print('ORIGDONE')
