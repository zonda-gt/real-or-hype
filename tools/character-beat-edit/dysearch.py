import json, sys, requests, time
kw, out = sys.argv[1], sys.argv[2]
body = {"keyword": kw, "cursor": 0, "sort_type": "1", "publish_time": "180", "filter_duration": "0-1", "content_type": "1", "search_id": "", "backtrace": ""}
for i in range(3):
    r = requests.post("https://api.tikhub.io/api/v1/douyin/search/fetch_video_search_v2", json=body,
                      headers={"Authorization": "Bearer dummy"}, timeout=90)
    if r.status_code == 200: break
    time.sleep(3)
print(kw, r.status_code)
d = r.json(); json.dump(d, open(out, "w"), ensure_ascii=False)
items = (d.get("data") or {}).get("business_data") or []
for it in items:
    a = (it.get("data") or {}).get("aweme_info")
    if not a: continue
    v = a.get("video", {})
    print(a["aweme_id"], a.get("statistics", {}).get("digg_count"), round(v.get("duration", 0)/1000,1), f'{v.get("width")}x{v.get("height")}', a.get("desc", "")[:60].replace("\n"," "))
