#!/usr/bin/env python3
"""Publish videos to Instagram as TRIAL reels (Instagram Content Publishing API).

Works with local files (uploaded straight to Instagram, no hosting needed) or public video URLs.

  python3 post_trial_reel.py VIDEO [VIDEO ...] --account steven_chinapal --caption-file caption.txt \
      [--graduation MANUAL|SS_PERFORMANCE] [--dry-run | --yes]

  --dry-run  checks the token, the account and every video, then stops (always run this first)
  --yes      actually publishes; without it the script only checks
Token (never printed), from the environment or an env file (--env-file, default ~/.config/instagram-trial-reel/.env):
  INSTAGRAM_ACCESS_TOKEN [+ INSTAGRAM_USER_ID]   Instagram Login  -> graph.instagram.com
  INSTAGRAM_FB_TOKEN + INSTAGRAM_USER_ID         Facebook Login   -> graph.facebook.com (fallback)
Each local video gets a log next to it, VIDEO.ig.json, so the same file is never published twice.
Needs: python3, requests (pip install requests); ffprobe optional (video checks).
"""
import argparse, json, os, shutil, subprocess, sys, time
try:
    import requests
except ImportError:
    sys.exit("Needs the requests package: pip install requests")

VER = os.environ.get("GRAPH_VERSION", "v24.0")
ap = argparse.ArgumentParser()
ap.add_argument("videos", nargs="+")
ap.add_argument("--account", required=True, help="expected Instagram username, e.g. steven_chinapal")
g = ap.add_mutually_exclusive_group(required=True)
g.add_argument("--caption"); g.add_argument("--caption-file")
ap.add_argument("--graduation", default="MANUAL", choices=["MANUAL", "SS_PERFORMANCE"])
ap.add_argument("--env-file", default=os.path.expanduser("~/.config/instagram-trial-reel/.env"))
m = ap.add_mutually_exclusive_group(required=True)
m.add_argument("--dry-run", action="store_true"); m.add_argument("--yes", action="store_true")
a = ap.parse_args()

if os.path.exists(a.env_file):
    for line in open(a.env_file):
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1); os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
caption = a.caption if a.caption is not None else open(a.caption_file, encoding="utf-8").read().strip()
if len(caption) > 2200: sys.exit(f"Caption is {len(caption)} characters; Instagram allows 2200.")
if caption.count("#") > 30: sys.exit("Caption has more than 30 hashtags.")
SECRETS = [v for v in (os.environ.get("INSTAGRAM_ACCESS_TOKEN"), os.environ.get("INSTAGRAM_FB_TOKEN")) if v]

def clean(x):
    s = x if isinstance(x, str) else json.dumps(x)
    for t in SECRETS: s = s.replace(t, "***")
    return s[:600]

def call(method, url, **kw):
    for attempt in range(3):
        try:
            r = requests.request(method, url, timeout=600, **kw)
            try: return r.status_code, r.json()
            except Exception: return r.status_code, {"raw": r.text[:300]}
        except requests.RequestException as e:
            err = str(e); time.sleep(5 * (attempt + 1))
    return 0, {"error": clean(err)}

def account():
    tried = []
    if os.environ.get("INSTAGRAM_ACCESS_TOKEN"):
        tok = os.environ["INSTAGRAM_ACCESS_TOKEN"]; base = f"https://graph.instagram.com/{VER}"
        sc, d = call("GET", f"{base}/me", params={"fields": "user_id,username", "access_token": tok})
        if sc == 200 and d.get("username"): return base, tok, str(d.get("user_id") or os.environ.get("INSTAGRAM_USER_ID")), d["username"]
        tried.append(("graph.instagram.com", sc, clean(d)))
    if os.environ.get("INSTAGRAM_FB_TOKEN") and os.environ.get("INSTAGRAM_USER_ID"):
        tok = os.environ["INSTAGRAM_FB_TOKEN"]; uid = os.environ["INSTAGRAM_USER_ID"]; base = f"https://graph.facebook.com/{VER}"
        sc, d = call("GET", f"{base}/{uid}", params={"fields": "username", "access_token": tok})
        if sc == 200 and d.get("username"): return base, tok, uid, d["username"]
        tried.append(("graph.facebook.com", sc, clean(d)))
    sys.exit("No working Instagram token. Set INSTAGRAM_ACCESS_TOKEN (and INSTAGRAM_USER_ID) in the environment "
             f"or in {a.env_file}. Tried: {tried}")

def probe(path):
    """Warn about things Instagram rejects or crops. Returns a list of problems that stop the post."""
    stop, warn = [], []
    size = os.path.getsize(path)
    if size > 1024 ** 3: stop.append(f"file is {size/1e6:.0f} MB (limit 1 GB)")
    if not shutil.which("ffprobe"): return stop, ["ffprobe not installed, video not checked"]
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type,codec_name,width,height,r_frame_rate,sample_rate",
                          "-of", "json", path], capture_output=True, text=True)
    try: info = json.loads(out.stdout)
    except Exception: return stop + ["ffprobe could not read the file"], warn
    dur = float(info.get("format", {}).get("duration", 0)); v = [s for s in info.get("streams", []) if s.get("codec_type") == "video"]
    au = [s for s in info.get("streams", []) if s.get("codec_type") == "audio"]
    if not v: stop.append("no video stream")
    else:
        v = v[0]; w, h = v.get("width", 0), v.get("height", 0)
        num, _, den = (v.get("r_frame_rate") or "0/1").partition("/"); fps = float(num) / float(den or 1) if float(den or 1) else 0
        if v.get("codec_name") not in ("h264", "hevc"): stop.append(f"video codec {v.get('codec_name')} (needs H.264 or HEVC)")
        if h and abs(w / h - 9 / 16) > 0.02: warn.append(f"{w}x{h} is not 9:16, Instagram will crop or letterbox it")
        if fps and not 23 <= fps <= 60: stop.append(f"{fps:.1f} fps (needs 23-60)")
    if not 3 <= dur <= 900: stop.append(f"{dur:.1f} s long (reels via the API: 3 s to 15 min)")
    if au and au[0].get("codec_name") != "aac": stop.append(f"audio codec {au[0].get('codec_name')} (needs AAC)")
    if au and int(au[0].get("sample_rate", 0) or 0) > 48000: stop.append("audio sample rate above 48 kHz")
    return stop, warn

base, tok, uid, username = account()
print(f"Account: @{username} (id {uid}) via {base.split('/')[2]}")
if username.lower() != a.account.lower().lstrip("@"):
    sys.exit(f"STOP: this token posts as @{username}, not @{a.account}. Nothing was published.")

items, problems = [], False
for vid in a.videos:
    remote = vid.startswith("http://") or vid.startswith("https://")
    if remote:
        h = requests.head(vid, timeout=60, allow_redirects=True)
        print(f"{vid}: URL {h.status_code}, {h.headers.get('content-length', '?')} bytes")
        if h.status_code != 200: problems = True
        log = None
    else:
        if not os.path.isfile(vid): print(f"{vid}: file not found"); problems = True; continue
        stop, warn = probe(vid)
        print(f"{vid}: {os.path.getsize(vid)/1e6:.1f} MB" + "".join(f"\n  warning: {x}" for x in warn) + "".join(f"\n  PROBLEM: {x}" for x in stop))
        problems |= bool(stop); log = vid + ".ig.json"
    state = json.load(open(log)) if log and os.path.exists(log) else {}
    if state.get("media_id"): print(f"  already published: {state.get('permalink') or state['media_id']} (skipped)")
    items.append((vid, remote, log, state))
print(f"Caption ({len(caption)} chars):\n---\n{caption}\n---\nTrial reel, graduation: {a.graduation}")
if problems: sys.exit("STOP: fix the problems above. Nothing was published.")
if a.dry_run: print("Dry run OK. Nothing was published."); sys.exit(0)

results = []
for vid, remote, log, state in items:
    if state.get("media_id"): results.append((vid, state.get("permalink"))); continue
    save = (lambda: json.dump(state, open(log, "w"), indent=1)) if log else (lambda: None)
    cid = state.get("container")
    if not cid:
        data = {"media_type": "REELS", "caption": caption, "trial_params": json.dumps({"graduation_strategy": a.graduation}), "access_token": tok}
        if remote: data["video_url"] = vid
        else: data["upload_type"] = "resumable"
        sc, d = call("POST", f"{base}/{uid}/media", data=data)
        if sc != 200 or "id" not in d: print(f"{vid}: could not create the post: {sc} {clean(d)}"); results.append((vid, None)); continue
        cid = d["id"]; state.update(container=cid, created=time.strftime("%Y-%m-%dT%H:%M:%S")); save()
        if not remote:
            uri = d.get("uri") or f"https://rupload.facebook.com/ig-api-upload/{VER}/{cid}"
            with open(vid, "rb") as fh:
                sc, d = call("POST", uri, headers={"Authorization": f"OAuth {tok}", "offset": "0", "file_size": str(os.path.getsize(vid))}, data=fh)
            if sc != 200: print(f"{vid}: upload failed: {sc} {clean(d)}"); results.append((vid, None)); continue
            state["uploaded"] = True; save()
    print(f"{vid}: uploaded, Instagram is processing it...")
    status, d = None, {}
    for _ in range(120):
        sc, d = call("GET", f"{base}/{cid}", params={"fields": "status_code,status", "access_token": tok})
        status = d.get("status_code")
        if status in ("FINISHED", "ERROR", "EXPIRED"): break
        time.sleep(10)
    if status != "FINISHED":
        print(f"{vid}: processing ended with {status}: {clean(d)}")
        if status in ("ERROR", "EXPIRED"): state.pop("container", None); save()
        results.append((vid, None)); continue
    sc, d = call("POST", f"{base}/{uid}/media_publish", data={"creation_id": cid, "access_token": tok})
    if sc != 200 or "id" not in d: print(f"{vid}: publish failed: {sc} {clean(d)}"); results.append((vid, None)); continue
    state["media_id"] = d["id"]; save()
    sc, d = call("GET", f"{base}/{state['media_id']}", params={"fields": "permalink", "access_token": tok})
    state["permalink"] = d.get("permalink"); save()
    print(f"{vid}: PUBLISHED as a trial reel {state['permalink'] or state['media_id']}")
    results.append((vid, state["permalink"] or state["media_id"]))
print("\nResult:")
for vid, link in results: print(f"  {'OK    ' if link else 'FAILED'} {vid} {link or ''}")
sys.exit(0 if all(l for _, l in results) else 1)
