"""Add or update ChinaPal /comment keyword rules (table inbox_comment_rules) through Supabase REST.

usage: python3 set_comment_rules.py <rules.json> [--dry-run]
rules.json: [{"keyword": "reel", "media_id": null, "message": "...", "public_reply": "...",
              "ask_first": true, "opener": "...", "button": "...", "follow_up": "..."}]
Env: CONCIERGE_SUPABASE_URL, CONCIERGE_SUPABASE_SECRET_KEY (service role). Never prints the key.
Mirrors the app's changeRule(): keyword lower-cased words only, limits keyword 40 / message 1000 /
public reply 600 / opener 600 / button 20 / follow-up 600. Existing rule for the same keyword and post is updated, never deleted.
"""
import json, os, re, sys, unicodedata, requests

URL = os.environ["CONCIERGE_SUPABASE_URL"].rstrip("/") + "/rest/v1/inbox_comment_rules"
KEY = os.environ["CONCIERGE_SUPABASE_SECRET_KEY"]
H = {"apikey": KEY, "Authorization": f"Bearer {KEY}", "Content-Type": "application/json", "Prefer": "return=representation"}
DRY = "--dry-run" in sys.argv
LIM = {"keyword": 40, "message": 1000, "public_reply": 600, "opener": 600, "button": 20, "follow_up": 600}
COLS = "id,media_id,keyword,active,ask_first,button,updated_at"

def norm(t):  # same as comment-data.ts normalize()
    return re.sub(r"[^\w]+|_", " ", unicodedata.normalize("NFKC", t).lower()).strip()

def clean(s): return s.replace(KEY, "***")[:500]

r = requests.get(URL, headers=H, params={"select": COLS, "order": "created_at"}, timeout=60)
if r.status_code != 200: sys.exit(f"read failed {r.status_code} {clean(r.text)}")
print("existing rules:"); [print(" ", x) for x in r.json()]
for rule in json.load(open(sys.argv[1])):
    rule = dict(rule); rule["keyword"] = norm(rule["keyword"])
    for k, n in LIM.items():
        if len(rule.get(k) or "") > n: sys.exit(f"{k} too long ({len(rule[k])} > {n})")
    rule.setdefault("public_reply", ""); rule.setdefault("active", True); rule["updated_by"] = "claude (Steven approved)"
    q = {"select": "id", "keyword": f"eq.{rule['keyword']}", "media_id": "is.null" if rule.get("media_id") is None else f"eq.{rule['media_id']}"}
    ex = requests.get(URL, headers=H, params=q, timeout=60).json()
    print(f"{'update' if ex else 'insert'} rule '{rule['keyword']}' (post: {rule.get('media_id') or 'every post'})")
    if DRY: continue
    if ex: w = requests.patch(URL, headers=H, params={"id": f"eq.{ex[0]['id']}"}, json={**rule, "updated_at": __import__("datetime").datetime.utcnow().isoformat()+"Z"}, timeout=60)
    else: w = requests.post(URL, headers=H, json=rule, timeout=60)
    print("  ->", w.status_code, clean(w.text) if w.status_code >= 300 else "ok")
print("dry run, nothing written" if DRY else "done")
