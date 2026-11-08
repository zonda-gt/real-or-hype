"""Publish videos to @steven_chinapal as Instagram TRIAL reels (Content Publishing API).

usage: python3 post_trial_reels.py <manifest.json> [--dry-run]
manifest: {"caption": "...", "graduation": "MANUAL"|"SS_PERFORMANCE", "expect_username": "steven_chinapal",
           "videos": [{"name": "...", "url": "https://public/video.mp4"}, ...]}

Reads the token from the environment, never prints it:
  INSTAGRAM_ACCESS_TOKEN (+ optional INSTAGRAM_USER_ID) -> graph.instagram.com (Instagram Login)
  INSTAGRAM_FB_TOKEN + INSTAGRAM_USER_ID               -> graph.facebook.com (Facebook Login), used if the first fails
Writes posted.json next to the manifest so a video is never published twice.
"""
import json, os, sys, time, requests

VER = os.environ.get("GRAPH_VERSION", "v24.0")
man_path = sys.argv[1]; DRY = "--dry-run" in sys.argv
M = json.load(open(man_path))
STATE = os.path.join(os.path.dirname(os.path.abspath(man_path)), "posted.json")
posted = json.load(open(STATE)) if os.path.exists(STATE) else {}
SECRETS = [v for v in (os.environ.get("INSTAGRAM_ACCESS_TOKEN"), os.environ.get("INSTAGRAM_FB_TOKEN")) if v]

def clean(x):
    s = json.dumps(x) if not isinstance(x, str) else x
    for t in SECRETS: s = s.replace(t, "***")
    return s[:600]

def call(method, url, **kw):
    r = requests.request(method, url, timeout=120, **kw)
    try: d = r.json()
    except Exception: d = {"raw": r.text}
    return r.status_code, d

def pick_account():
    tries = []
    if os.environ.get("INSTAGRAM_ACCESS_TOKEN"):
        tok = os.environ["INSTAGRAM_ACCESS_TOKEN"]; base = f"https://graph.instagram.com/{VER}"
        sc, d = call("GET", f"{base}/me", params={"fields": "user_id,username", "access_token": tok})
        if sc == 200 and d.get("username"): return base, tok, d.get("user_id") or os.environ.get("INSTAGRAM_USER_ID"), d["username"]
        tries.append(("instagram", sc, clean(d)))
    if os.environ.get("INSTAGRAM_FB_TOKEN") and os.environ.get("INSTAGRAM_USER_ID"):
        tok = os.environ["INSTAGRAM_FB_TOKEN"]; uid = os.environ["INSTAGRAM_USER_ID"]; base = f"https://graph.facebook.com/{VER}"
        sc, d = call("GET", f"{base}/{uid}", params={"fields": "username", "access_token": tok})
        if sc == 200 and d.get("username"): return base, tok, uid, d["username"]
        tries.append(("facebook", sc, clean(d)))
    sys.exit(f"No working Instagram token: {tries}")

base, tok, uid, username = pick_account()
print(f"account: @{username} (id {uid}) via {base.split('/')[2]}")
if username.lower() != M["expect_username"].lower():
    sys.exit(f"ABORT: token belongs to @{username}, expected @{M['expect_username']}")
for v in M["videos"]:
    h = requests.head(v["url"], timeout=60, allow_redirects=True)
    print(f"{v['name']}: url {h.status_code} {h.headers.get('content-length')} bytes")
    if h.status_code != 200: sys.exit(f"ABORT: {v['name']} url not reachable")
if DRY: print("dry run: stopping before creating containers"); sys.exit(0)

for v in M["videos"]:
    n = v["name"]
    if posted.get(n, {}).get("media_id"): print(f"{n}: already published {posted[n]}"); continue
    cid = posted.get(n, {}).get("container")
    if not cid:
        sc, d = call("POST", f"{base}/{uid}/media", data={"media_type": "REELS", "video_url": v["url"], "caption": M["caption"],
                  "trial_params": json.dumps({"graduation_strategy": M.get("graduation", "MANUAL")}), "access_token": tok})
        if sc != 200 or "id" not in d: print(f"{n}: container FAILED {sc} {clean(d)}"); continue
        cid = d["id"]; posted[n] = {"container": cid}; json.dump(posted, open(STATE, "w"), indent=1)
    print(f"{n}: container {cid}, waiting for processing")
    status = None
    for _ in range(90):
        sc, d = call("GET", f"{base}/{cid}", params={"fields": "status_code,status", "access_token": tok})
        status = d.get("status_code")
        if status in ("FINISHED", "ERROR", "EXPIRED"): break
        time.sleep(10)
    if status != "FINISHED": print(f"{n}: processing {status} {clean(d)}"); continue
    sc, d = call("POST", f"{base}/{uid}/media_publish", data={"creation_id": cid, "access_token": tok})
    if sc != 200 or "id" not in d: print(f"{n}: publish FAILED {sc} {clean(d)}"); continue
    mid = d["id"]; posted[n]["media_id"] = mid; json.dump(posted, open(STATE, "w"), indent=1)
    sc, d = call("GET", f"{base}/{mid}", params={"fields": "permalink", "access_token": tok})
    posted[n]["permalink"] = d.get("permalink"); json.dump(posted, open(STATE, "w"), indent=1)
    print(f"{n}: PUBLISHED media {mid} {d.get('permalink')}")
print("result:", json.dumps(posted, indent=1))
