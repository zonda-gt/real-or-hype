import json, glob, sys, requests, os
ids = sys.argv[1].split(",")
outdir = sys.argv[2]
found = {}
for f in glob.glob("search/*.json"):
    d = json.load(open(f))
    for it in (d.get("data") or {}).get("business_data") or []:
        a = (it.get("data") or {}).get("aweme_info")
        if a and a["aweme_id"] in ids: found[a["aweme_id"]] = a
meta = {}
for i in ids:
    a = found[i]; v = a["video"]
    cands = []
    for br in v.get("bit_rate") or []:
        pa = br.get("play_addr") or {}
        cands.append((pa.get("height", 0) * (pa.get("width", 0)), br.get("bit_rate", 0), pa.get("url_list", [])))
    cands.sort(key=lambda c: (-c[0], -c[1]))
    # ByteVC2 (bvc2) streams do not decode in ffmpeg: try the H.264 address first
    urls = (v.get("play_addr_h264") or {}).get("url_list", []) + [u for c in cands for u in c[2]] + v.get("play_addr", {}).get("url_list", [])
    ok = False
    for u in urls:
        try:
            r = requests.get(u, headers={"User-Agent": "Mozilla/5.0", "Referer": "https://www.douyin.com/"}, timeout=60)
            if r.status_code == 200 and len(r.content) > 100000 and r.content[4:8] == b"ftyp":
                open(f"{outdir}/{i}.mp4", "wb").write(r.content); ok = True; break
        except Exception as e:
            pass
    meta[i] = {"desc": a.get("desc"), "author": a["author"].get("nickname"), "likes": a.get("statistics", {}).get("digg_count"), "ok": ok}
    print(i, ok, a["author"].get("nickname"))
json.dump(meta, open(f"{outdir}/meta.json", "w"), ensure_ascii=False, indent=1)
