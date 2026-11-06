# pick best decodable stream per clip: bvc1 (HEVC) / h264 bit_rate entries, play_addr_h264, or the play endpoint
import json,os,subprocess
os.makedirs("raw/best",exist_ok=True)
def probe(p):
    r=subprocess.run(["ffprobe","-v","error","-select_streams","v:0","-show_entries","stream=codec_name,width,height","-of","csv=p=0",p],capture_output=True,text=True).stdout.strip().split(",")
    return r if len(r)==3 and r[0] in("h264","hevc") else None
def get(urls,out):
    for u in urls:
        p=subprocess.run(["curl","-sS","-L","-m","180","-o",out,"-H","User-Agent: Mozilla/5.0","-H","Referer: https://www.douyin.com/","-w","%{http_code}",u],capture_output=True,text=True)
        if p.stdout.strip()=="200" and os.path.exists(out) and os.path.getsize(out)>50000 and probe(out): return True
    return False
for f in sorted(os.listdir("search/detail")):
    aid=f[:-5]; det=json.load(open("search/detail/"+f)); v=det["video"]
    out=f"raw/best/{aid}.mp4"
    if os.path.exists(out) and probe(out): print(aid,"have",probe(out)); continue
    opts=[]
    for b in v.get("bit_rate",[]):
        if b.get("is_bytevc1")==2: continue
        pa=b["play_addr"]; opts.append((min(pa.get("width",0),pa.get("height",0)),pa.get("url_list",[]),b.get("gear_name")))
    h=v.get("play_addr_h264") or {}
    opts.append((min(h.get("width",0),h.get("height",0)),h.get("url_list",[]),"play_addr_h264"))
    opts.sort(key=lambda x:-x[0])
    h264=f"raw/h264/{aid}.mp4"; hp=probe(h264) if os.path.exists(h264) else None
    done=False
    for res,urls,name in opts:
        if hp and int(min(hp[1],hp[2],key=int))>=res:
            subprocess.run(["cp",h264,out]); print(aid,"play-endpoint",hp); done=True; break
        if get(urls,out): print(aid,name,probe(out)); done=True; break
    if not done and hp: subprocess.run(["cp",h264,out]); print(aid,"play-endpoint-fallback",hp)
    elif not done: print(aid,"FAIL")
