#!/usr/bin/env python3
"""TikHub helper: th.py GET|POST path [json] [outname]. Caches to api/, logs calls to api/calls.log. Never prints the key."""
import sys, os, json, hashlib, urllib.request, time
S=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
method, path = sys.argv[1], sys.argv[2]
body = sys.argv[3] if len(sys.argv)>3 and sys.argv[3] else None
name = sys.argv[4] if len(sys.argv)>4 else hashlib.md5((method+path+(body or '')).encode()).hexdigest()[:10]
out=os.path.join(S,'api',name+'.json')
if os.path.exists(out) and os.environ.get('FORCE')!='1':
    print(out); sys.exit(0)
url='https://api.tikhub.io'+path
req=urllib.request.Request(url, data=body.encode() if body else None, method=method,
  headers={'Authorization':'Bearer '+os.environ['TIKHUB_API_KEY'],'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) ChinaPal-research','Content-Type':'application/json'})
for i in range(3):
    try:
        r=urllib.request.urlopen(req, timeout=90); data=r.read(); code=r.status; break
    except urllib.error.HTTPError as e:
        data=e.read(); code=e.code
        if code<500: break
    except Exception as e:
        data=str(e).encode(); code=0
    time.sleep(3)
open(out,'wb').write(data)
with open(os.path.join(S,'api','calls.log'),'a') as f: f.write(f"{time.strftime('%H:%M:%S')} {code} {method} {path} {(body or '')[:120]} -> {name}\n")
print(out, code, file=sys.stderr); print(out)
