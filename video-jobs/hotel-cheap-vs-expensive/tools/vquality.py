# Rough visual-quality metrics per clip (frames at 2 fps, normalised to 540x960)
import cv2, numpy as np, subprocess, sys, json
out = {}
for aid in sys.argv[1:]:
    p = f"raw/best/{aid}.mp4"
    pr = json.loads(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height,bit_rate,codec_name:format=duration,bit_rate", "-of", "json", p], capture_output=True, text=True).stdout)
    st = pr["streams"][0]; br = int(st.get("bit_rate") or pr["format"].get("bit_rate") or 0)
    cap = cv2.VideoCapture(p); fps = cap.get(cv2.CAP_PROP_FPS) or 30; step = max(1, int(round(fps / 2)))
    sh, lu, co, mo = [], [], [], []; prev = None; i = 0
    while True:
        ok, f = cap.read()
        if not ok: break
        if i % step == 0:
            g = cv2.cvtColor(cv2.resize(f, (540, 960)), cv2.COLOR_BGR2GRAY)
            sh.append(cv2.Laplacian(g, cv2.CV_64F).var()); lu.append(g.mean()); co.append(g.std())
            if prev is not None: mo.append(np.abs(g.astype(int) - prev.astype(int)).mean())
            prev = g
        i += 1
    out[aid] = {"res": f'{st["width"]}x{st["height"]}', "codec": st["codec_name"], "kbps": br // 1000,
                "sharp_med": round(float(np.median(sh)), 1), "sharp_p25": round(float(np.percentile(sh, 25)), 1),
                "luma": round(float(np.mean(lu)), 1), "contrast": round(float(np.mean(co)), 1), "shake": round(float(np.median(mo)), 1),
                "dur": round(float(pr["format"]["duration"]), 1)}
    print(aid, out[aid], flush=True)
json.dump(out, open("work/vquality.json", "w"), indent=1)
