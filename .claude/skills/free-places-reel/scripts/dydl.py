import sys,os,json,glob,subprocess
# usage: dydl.py searchdir rawdir key:id ...
sd,rd=sys.argv[1],sys.argv[2]; os.makedirs(rd,exist_ok=True)
idx={}
for f in glob.glob(f'{sd}/*.json'):
    for x in json.load(open(f)): idx[x['id']]=x
for kid in sys.argv[3:]:
    k,i=kid.split(':'); out=f'{rd}/{k}_{i}.mp4'
    if os.path.exists(out) and os.path.getsize(out)>10000: continue
    x=idx.get(i)
    if not x: print('missing',i); continue
    ok=False
    for u in x['url']:
        r=subprocess.run(['curl','-sSL','-m','120','-A','Mozilla/5.0','-H','Referer: https://www.douyin.com/','-o',out,u],capture_output=True)
        if r.returncode==0 and os.path.getsize(out)>10000: ok=True;break
    print(k,i,'OK' if ok else 'FAIL', os.path.getsize(out) if os.path.exists(out) else 0)
