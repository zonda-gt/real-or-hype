import sys,os,json
sys.path.insert(0,os.path.dirname(__file__))
from th import call
os.makedirs("search/detail",exist_ok=True)
for aid in sys.argv[1:]:
    p=f"search/detail/{aid}.json"
    if os.path.exists(p): print(aid,"cached"); continue
    d=call("GET","/api/v1/douyin/app/v3/fetch_one_video",params={"aweme_id":aid})
    det=((d.get("data") or {}).get("aweme_detail")) if isinstance(d,dict) else None
    if not det:
        d=call("GET","/api/v1/douyin/app/v3/fetch_one_video_v2",params={"aweme_id":aid})
        det=((d.get("data") or {}).get("aweme_detail")) if isinstance(d,dict) else None
    if not det: print(aid,"FAIL",str(d)[:200]); continue
    json.dump(det,open(p,"w"),ensure_ascii=False)
    v=det["video"]
    print(aid,"uri",v["play_addr"].get("uri"),[(b.get("gear_name"),b["play_addr"].get("width"),b.get("is_bytevc1"),b.get("is_h265")) for b in v.get("bit_rate",[])][:6])
