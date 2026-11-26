#!/usr/bin/env python3
"""Generate one Seedance clip of the creator at a real place (SKILL.md section 10).

  seedance.py <out.mp4> <place_frame.jpg> "<Chinese prompt>" [--res 720p] [--model ...] [--dur 4]

The creator's verified portrait asset is reference 1, the 9:16 frame of the
place is reference 2 (sent as a data URL). The Ark key is proxy-injected.
Prints the task id, then polls until done, downloads the video and prints the
tokens used (record 2.5 costs in SKILL.md).
"""
import argparse, base64, json, sys, time, urllib.request

ARK = "https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks"
ME = "asset://asset-20261114110202-8gttx"
STYLE = "竖屏，手机实拍质感，自然柔和的光线，真实感，镜头轻微手持晃动。"

def call(url, body=None):
    req = urllib.request.Request(url, data=json.dumps(body).encode() if body else None, method="POST" if body else "GET",
                                 headers={"Content-Type": "application/json", "Authorization": "Bearer proxy-injected"})
    try:
        return json.load(urllib.request.urlopen(req, timeout=60))
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code}: {e.read().decode()[:500]}")

ap = argparse.ArgumentParser()
ap.add_argument("out"); ap.add_argument("frame"); ap.add_argument("prompt")
ap.add_argument("--res", default="720p"); ap.add_argument("--dur", type=int, default=4)
ap.add_argument("--model", default="doubao-seedance-2-5-260628")
a = ap.parse_args()
frame = "data:image/jpeg;base64," + base64.b64encode(open(a.frame, "rb").read()).decode()
prompt = a.prompt if a.prompt.endswith(STYLE) else a.prompt + STYLE
task = call(ARK, {
    "model": a.model,
    "content": [
        {"type": "text", "text": prompt},
        {"type": "image_url", "image_url": {"url": ME}, "role": "reference_image"},
        {"type": "image_url", "image_url": {"url": frame}, "role": "reference_image"},
    ],
    "ratio": "9:16", "duration": a.dur, "resolution": a.res, "generate_audio": False, "watermark": False,
})
tid = task["id"]; print("task", tid, flush=True)
while True:
    time.sleep(10)
    r = call(f"{ARK}/{tid}")
    if r["status"] in ("succeeded", "failed", "cancelled", "expired"):
        break
json.dump(r, open(a.out + ".json", "w"), ensure_ascii=False, indent=1)
if r["status"] != "succeeded":
    sys.exit(f"{r['status']}: {json.dumps(r.get('error'), ensure_ascii=False)}")
urllib.request.urlretrieve(r["content"]["video_url"], a.out)
print("done", a.out, "tokens", r.get("usage", {}).get("completion_tokens"))
