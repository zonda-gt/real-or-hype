import os, json, sys, time, urllib.request, urllib.error, urllib.parse
BASE="https://api.tikhub.io"
H={"Authorization":"Bearer "+os.environ["TIKHUB_API_KEY"],"User-Agent":"chinapal-video/1.0","Content-Type":"application/json"}
LOG=os.path.join(os.environ.get("JOB","."),"search","calls.log")
def call(method,path,body=None,params=None,timeout=60):
    url=BASE+path
    if params:
        url+="?"+urllib.parse.urlencode(params)
    data=json.dumps(body).encode() if body is not None else None
    for i in range(3):
        try:
            req=urllib.request.Request(url,data=data,headers=H,method=method)
            with urllib.request.urlopen(req,timeout=timeout) as r:
                out=json.load(r)
            with open(LOG,"a") as f: f.write(f"{time.time():.0f} {method} {path} ok\n")
            return out
        except urllib.error.HTTPError as e:
            msg=e.read()[:300]
            with open(LOG,"a") as f: f.write(f"{time.time():.0f} {method} {path} HTTP{e.code}\n")
            if e.code in (400,401,402,403,404,422): return {"error":e.code,"msg":msg.decode('utf8','replace')}
            time.sleep(2*(i+1))
        except Exception as e:
            time.sleep(2*(i+1))
    return {"error":"fail"}
def balance():
    d=call("GET","/api/v1/tikhub/user/get_user_info")
    return d.get("user_data",{}).get("balance")
