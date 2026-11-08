"""Tiny TikHub client. Key read from env, never written anywhere.
Usage: python3 th.py GET|POST <path> '<json params/body>' <out.json>
Appends a line to calls.log (path + status only)."""
import json, os, sys, time, requests

BASE = "https://api.tikhub.io"
LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "calls.log")


def call(method, path, payload=None, retries=3):
    h = {"User-Agent": "chinapal-reel/1.0", "Authorization": "Bearer " + os.environ["TIKHUB_API_KEY"]}
    for i in range(retries):
        if method == "GET":
            r = requests.get(BASE + path, params=payload or {}, headers=h, timeout=90)
        else:
            r = requests.post(BASE + path, json=payload or {}, headers=h, timeout=90)
        with open(LOG, "a") as f:
            f.write(f"{time.strftime('%H:%M:%S')} {method} {path} {r.status_code}\n")
        if r.status_code == 200:
            return r.json()
        if r.status_code < 500 and r.status_code != 429:
            break
        time.sleep(2 * (i + 1))
    raise SystemExit(f"{path} -> {r.status_code} {r.text[:300]}")


def balance():
    return call("GET", "/api/v1/tikhub/user/get_user_info")["user_data"]["balance"]


if __name__ == "__main__":
    m, p, body, out = sys.argv[1:5]
    d = call(m, p, json.loads(body))
    json.dump(d, open(out, "w"), ensure_ascii=False)
    print("saved", out)
