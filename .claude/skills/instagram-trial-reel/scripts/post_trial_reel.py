#!/usr/bin/env python3
"""Publish videos to Instagram as TRIAL reels (Instagram Content Publishing API).

Instagram only accepts a reel from a PUBLIC video URL with the Instagram Login token (graph.instagram.com
rejects direct uploads: "The parameter video_url is required"), wherever the script runs. So for a local file
the script first hosts it in this public GitHub repo: it copies the file to media/trial-reels/, commits, pushes
the current branch, and gives Instagram the raw.githubusercontent.com link. Public URLs are used as they are.

  python3 post_trial_reel.py VIDEO_OR_URL [...] --account steven_chinapal --caption-file caption.txt \
      [--commit-message-file msg.txt] [--dry-run | --yes]

Graduation is always MANUAL (the user's rule): the reel goes to non-followers only, and the user shares it to
followers themselves in the Instagram app. There is deliberately no option for SS_PERFORMANCE (auto-graduation).

  --dry-run        checks the token, the account, every video and the caption; pushes and publishes nothing
  --yes            hosts local files (commit + push) and publishes
  --direct-upload  upload local files straight to Instagram instead (resumable upload). Only for a Facebook Login
                   token with instagram_content_publish; never worked with the Instagram Login token.
Token (never printed), from the environment or an env file (--env-file, default ~/.config/instagram-trial-reel/.env):
  INSTAGRAM_ACCESS_TOKEN [+ INSTAGRAM_USER_ID]   Instagram Login  -> graph.instagram.com
  INSTAGRAM_FB_TOKEN + INSTAGRAM_USER_ID         Facebook Login   -> graph.facebook.com (fallback)
Each video gets a log, VIDEO.ig.json (next to the repo copy for hosted files), so it is never published twice.
Needs: python3, requests, git (for hosting); ffprobe optional (video checks).
"""
import argparse, json, os, re, shutil, subprocess, sys, time
try:
    import requests
except ImportError:
    sys.exit("Needs the requests package: pip install requests")

VER = os.environ.get("GRAPH_VERSION", "v24.0")
HERE = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser()
ap.add_argument("videos", nargs="+")
ap.add_argument("--account", required=True, help="expected Instagram username, e.g. steven_chinapal")
g = ap.add_mutually_exclusive_group(required=True)
g.add_argument("--caption"); g.add_argument("--caption-file")
GRADUATION = "MANUAL"   # always: the user graduates trial reels to followers themselves; never SS_PERFORMANCE
ap.add_argument("--env-file", default=os.path.expanduser("~/.config/instagram-trial-reel/.env"))
ap.add_argument("--repo", default=None, help="git checkout used for hosting (default: the repo this script is in)")
ap.add_argument("--host-dir", default="media/trial-reels", help="folder in the repo for hosted videos")
ap.add_argument("--commit-message-file", default=None, help="commit message for the hosting commit (e.g. with attribution lines)")
ap.add_argument("--direct-upload", action="store_true")
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
    err = ""
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
    """Things Instagram rejects or crops. Returns (problems that stop the post, warnings)."""
    stop, warn = [], []
    size = os.path.getsize(path)
    if size > 1024 ** 3: stop.append(f"file is {size/1e6:.0f} MB (limit 1 GB)")
    if size > 95 * 1024 ** 2 and not a.direct_upload: stop.append(f"file is {size/1e6:.0f} MB; GitHub hosting takes files up to ~95 MB (re-encode smaller)")
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

# ---------- GitHub hosting (what has worked for every trial reel so far) ----------
def git(*args, check=True):
    r = subprocess.run(["git", "-C", REPO, *args], capture_output=True, text=True)
    if check and r.returncode: sys.exit(f"git {' '.join(args)} failed: {r.stderr.strip()[:400]}")
    return r.stdout.strip()

def repo_info():
    root = a.repo or subprocess.run(["git", "-C", HERE, "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
    if not root: sys.exit("Hosting a local file needs a git checkout of the public repo (use --repo).")
    url = subprocess.run(["git", "-C", root, "remote", "get-url", "origin"], capture_output=True, text=True).stdout.strip()
    mm = re.search(r"([^/:]+)/([^/]+?)(?:\.git)?/?$", url)
    if not mm: sys.exit(f"Can't read owner/repo from the origin remote.")
    br = subprocess.run(["git", "-C", root, "branch", "--show-current"], capture_output=True, text=True).stdout.strip()
    if not br: sys.exit("The repo is on a detached HEAD; check out a branch first.")
    return root, mm.group(1), mm.group(2), br

def tracked_copy(path):
    """Path of a tracked file in the repo with exactly the same content, or None."""
    sha = subprocess.run(["git", "-C", REPO, "hash-object", os.path.abspath(path)], capture_output=True, text=True).stdout.strip()
    for line in git("ls-files", "-s").splitlines():
        meta, _, p = line.partition("\t")
        if meta.split()[1:2] == [sha]: return p
    return None

def raw_url(rel): return f"https://raw.githubusercontent.com/{OWNER}/{NAME}/refs/heads/{BRANCH}/{rel}"

def host(path, dry):
    """Put a local file in the repo, push, return its public raw URL."""
    rel = tracked_copy(path)
    if not rel:
        rel = f"{a.host_dir}/{os.path.basename(path)}"; n = 1
        while os.path.exists(os.path.join(REPO, rel)):
            stem, ext = os.path.splitext(os.path.basename(path)); rel = f"{a.host_dir}/{stem}_{n}{ext}"; n += 1
        if dry: return rel, raw_url(rel), "would copy, commit and push"
        os.makedirs(os.path.dirname(os.path.join(REPO, rel)), exist_ok=True)
        shutil.copy2(path, os.path.join(REPO, rel))
        git("add", rel)
        msg = open(a.commit_message_file, encoding="utf-8").read() if a.commit_message_file else f"Add {os.path.basename(path)} for an Instagram trial reel"
        git("commit", "-q", "-m", msg, "--", rel)
    if dry: return rel, raw_url(rel), "already in the repo"
    for i in range(4):
        r = subprocess.run(["git", "-C", REPO, "push", "-u", "origin", BRANCH], capture_output=True, text=True)
        if r.returncode == 0: break
        time.sleep(2 ** (i + 1))
    else: sys.exit(f"git push failed: {r.stderr.strip()[:400]}")
    url, size = raw_url(rel), os.path.getsize(path)
    for _ in range(24):   # raw.githubusercontent.com can lag a few seconds behind a push
        h = requests.head(url, timeout=60, allow_redirects=True)
        if h.status_code == 200 and h.headers.get("content-length") == str(size): return rel, url, "pushed"
        time.sleep(5)
    sys.exit(f"{url} is not publicly reachable ({h.status_code}). Is the repo public? Nothing was published.")

# ---------- checks ----------
base, tok, uid, username = account()
print(f"Account: @{username} (id {uid}) via {base.split('/')[2]}")
if username.lower() != a.account.lower().lstrip("@"):
    sys.exit(f"STOP: this token posts as @{username}, not @{a.account}. Nothing was published.")
needs_repo = any(not v.startswith(("http://", "https://")) for v in a.videos) and not a.direct_upload
if needs_repo:
    REPO, OWNER, NAME, BRANCH = repo_info()
    print(f"Local files are hosted in github.com/{OWNER}/{NAME}, branch {BRANCH}, folder {a.host_dir}/")

items, problems = [], False
for vid in a.videos:
    remote = vid.startswith(("http://", "https://"))
    if remote:
        h = requests.head(vid, timeout=60, allow_redirects=True)
        print(f"{vid}: URL {h.status_code}, {h.headers.get('content-length', '?')} bytes")
        if h.status_code != 200: problems = True
        logs = []
    else:
        if not os.path.isfile(vid): print(f"{vid}: file not found"); problems = True; continue
        stop, warn = probe(vid)
        print(f"{vid}: {os.path.getsize(vid)/1e6:.1f} MB" + "".join(f"\n  warning: {x}" for x in warn) + "".join(f"\n  PROBLEM: {x}" for x in stop))
        problems |= bool(stop)
        logs = [vid + ".ig.json"]
        if needs_repo:
            rel = tracked_copy(vid)
            if rel: logs.append(os.path.join(REPO, rel + ".ig.json")); print(f"  already in the repo as {rel}")
    state = {}
    for lg in logs:
        if os.path.exists(lg): state = json.load(open(lg)); break
    if state.get("media_id"): print(f"  already published: {state.get('permalink') or state['media_id']} (skipped)")
    items.append([vid, remote, logs, state])
print(f"Caption ({len(caption)} chars):\n---\n{caption}\n---\nTrial reel, graduation: {GRADUATION}")
if problems: sys.exit("STOP: fix the problems above. Nothing was published.")
if a.dry_run:
    for vid, remote, logs, state in items:
        if not remote and needs_repo and not state.get("media_id"):
            rel, url, what = host(vid, dry=True); print(f"{vid}: {what} -> {url}")
    print("Dry run OK. Nothing was pushed or published."); sys.exit(0)

# ---------- publish ----------
results = []
for vid, remote, logs, state in items:
    if state.get("media_id"): results.append((vid, state.get("permalink"))); continue
    video_url = vid if remote else None
    if not remote and needs_repo:
        rel, video_url, what = host(vid, dry=False); print(f"{vid}: {what} -> {video_url}")
        logs = [os.path.join(REPO, rel + ".ig.json")] + logs
        state["video_url"] = video_url
    def save():
        for lg in logs: json.dump(state, open(lg, "w"), indent=1)
    cid = state.get("container")
    if not cid:
        data = {"media_type": "REELS", "caption": caption, "trial_params": json.dumps({"graduation_strategy": GRADUATION}), "access_token": tok}
        if video_url: data["video_url"] = video_url
        else: data["upload_type"] = "resumable"
        sc, d = call("POST", f"{base}/{uid}/media", data=data)
        if sc != 200 or "id" not in d: print(f"{vid}: could not create the post: {sc} {clean(d)}"); results.append((vid, None)); continue
        cid = d["id"]; state.update(container=cid, created=time.strftime("%Y-%m-%dT%H:%M:%S")); save()
        if not video_url:   # --direct-upload
            uri = d.get("uri") or f"https://rupload.facebook.com/ig-api-upload/{VER}/{cid}"
            with open(vid, "rb") as fh:
                sc, d = call("POST", uri, headers={"Authorization": f"OAuth {tok}", "offset": "0", "file_size": str(os.path.getsize(vid))}, data=fh)
            if sc != 200: print(f"{vid}: upload failed: {sc} {clean(d)}"); results.append((vid, None)); continue
            state["uploaded"] = True; save()
    print(f"{vid}: Instagram is processing it...")
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
    state["permalink"] = d.get("permalink"); state["graduation"] = GRADUATION; state["posted"] = time.strftime("%Y-%m-%d"); save()
    print(f"{vid}: PUBLISHED as a trial reel {state['permalink'] or state['media_id']}")
    results.append((vid, state["permalink"] or state["media_id"]))
print("\nResult:")
for vid, link in results: print(f"  {'OK    ' if link else 'FAILED'} {vid} {link or ''}")
if needs_repo: print(f"Commit and push the new .ig.json logs in {a.host_dir}/ so these videos are never posted twice.")
sys.exit(0 if all(l for _, l in results) else 1)
