import sys,json,os,re
sys.path.insert(0,os.path.dirname(__file__))
from th import call
JOB=os.environ["JOB"]; OUT=os.path.join(JOB,"search")
cands_path=os.path.join(OUT,"candidates.json")
cands=json.load(open(cands_path)) if os.path.exists(cands_path) else {}
sugg=set()
def extract(a,kw,src):
    v=a.get("video") or {}
    best=None
    for b in v.get("bit_rate") or []:
        pa=b.get("play_addr") or {}
        w,h=pa.get("width") or 0,pa.get("height") or 0
        key=(min(w,h),b.get("bit_rate") or 0)
        if best is None or key>best[0]: best=(key,{"gear":b.get("gear_name"),"w":w,"h":h,"bitrate":b.get("bit_rate"),"is_h265":b.get("is_h265"),"urls":pa.get("url_list",[])})
    s=json.dumps(a,ensure_ascii=False)
    poi=a.get("poi_info") or {}
    ci=a.get("commerce_info") or {}
    edit=(a.get("status") or {}).get("aweme_edit_info") or {}
    au=a.get("author") or {}
    st=a.get("statistics") or {}
    ad_flags=[]
    if ci.get("is_ad"): ad_flags.append("commerce_info.is_ad")
    if "广告" in (edit.get("button_toast") or ""): ad_flags.append("edit_toast:"+edit.get("button_toast"))
    if "广告" in (a.get("desc") or ""): ad_flags.append("desc")
    for lab in (a.get("common_left_top_labels") or []) if isinstance(a.get("common_left_top_labels"),list) else []:
        if "广告" in json.dumps(lab,ensure_ascii=False): ad_flags.append("left_top_label")
    return {"aweme_id":a["aweme_id"],"nickname":au.get("nickname"),"unique_id":au.get("unique_id") or au.get("short_id"),
     "sec_uid":au.get("sec_uid"),"follower_count":au.get("follower_count"),"signature":(au.get("signature") or "")[:120],
     "desc":a.get("desc"),"create_time":a.get("create_time"),"digg":st.get("digg_count"),"share":st.get("share_count"),
     "collect":st.get("collect_count"),"comment":st.get("comment_count"),"duration_ms":a.get("duration") or v.get("duration"),
     "width":v.get("width"),"height":v.get("height"),"play_urls":(v.get("play_addr") or {}).get("url_list",[]),
     "best":best[1] if best else None,"poi_name":poi.get("poi_name"),"poi_addr":poi.get("address_info",{}).get("address") if isinstance(poi.get("address_info"),dict) else None,
     "poi_city":(poi.get("address_info") or {}).get("city") if isinstance(poi.get("address_info"),dict) else None,
     "anchor":json.dumps(a.get("anchor_info") or a.get("anchors"),ensure_ascii=False)[:300] if (a.get("anchor_info") or a.get("anchors")) else None,
     "ad_flags":ad_flags,"ip":a.get("ip_attribution"),"kw":[kw],"src":src}
def add(a,kw,src):
    if not a or "aweme_id" not in a: return
    if a.get("aweme_type") not in (0,None,4,51,55,61,109,111): pass
    r=extract(a,kw,src)
    if r["aweme_id"] in cands:
        if kw not in cands[r["aweme_id"]]["kw"]: cands[r["aweme_id"]]["kw"].append(kw)
        cands[r["aweme_id"]].update({k:v for k,v in r.items() if k not in("kw",)})
    else: cands[r["aweme_id"]]=r
    sw=a.get("suggest_words") or {}
    for g in (sw.get("suggest_words") or []):
        for w in g.get("words") or []: sugg.add(w.get("word"))
def v2(kw,pages=int(os.environ.get("PAGES","3"))):
    cursor,sid,bt=0,"",""
    n=0
    for p in range(pages):
        body={"keyword":kw,"cursor":cursor,"sort_type":"1","publish_time":"180","filter_duration":"0-1","content_type":"1","search_id":sid,"backtrace":bt}
        d=call("POST","/api/v1/douyin/search/fetch_video_search_v2",body)
        dd=(d or {}).get("data") or {}
        bd=dd.get("business_data") or []
        for it in bd:
            a=((it.get("data") or {}).get("aweme_info"))
            if a: add(a,kw,"v2"); n+=1
        bc=dd.get("business_config") or {}
        np_=bc.get("next_page") or {}
        if not bc.get("has_more") or not bd: break
        cursor=np_.get("cursor",cursor+len(bd)); sid=np_.get("search_id") or sid; bt=bc.get("backtrace") or bt
    return n
def v3(kw):
    d=call("POST","/api/v1/douyin/search/fetch_video_search_v3",{"query":kw,"label_type":1})
    json.dump(d,open(os.path.join(OUT,"v3_last.json"),"w"),ensure_ascii=False)
    n=0
    s=d.get("data") if isinstance(d,dict) else None
    # walk for aweme_info dicts
    def walk(o):
        nonlocal n
        if isinstance(o,dict):
            if "aweme_id" in o and "video" in o and "statistics" in o: add(o,kw,"v3"); n+=1; return
            for x in o.values(): walk(x)
        elif isinstance(o,list):
            for x in o: walk(x)
    walk(s)
    return n
if __name__=="__main__":
    mode=sys.argv[1]
    for kw in sys.argv[2:]:
        n=v2(kw) if mode=="v2" else v3(kw)
        print(mode,kw,n,flush=True)
    json.dump(cands,open(cands_path,"w"),ensure_ascii=False,indent=1)
    sp=os.path.join(OUT,"suggest.txt")
    old=set(open(sp).read().split("\n")) if os.path.exists(sp) else set()
    open(sp,"w").write("\n".join(sorted((old|sugg)-{""})))
    print("total",len(cands))
