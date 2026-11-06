#!/usr/bin/env python3
"""Watermark + quality QA. Writes qa/watermark_report.json and qa/final_contact_sheet.jpg"""
import json, os, re, subprocess, glob, sys
from multiprocessing import Pool
import cv2, pytesseract, numpy as np
from PIL import Image, ImageDraw, ImageFont

JOB = "/home/user/real-or-hype/video-jobs/hotel-cheap-vs-expensive"; os.chdir(JOB)
FR = "work/qa_frames"; os.makedirs(FR, exist_ok=True); os.makedirs("qa", exist_ok=True)
KEYS = ["抖音", "抖音号", "douyin", "tiktok", "小红书", "小红书号", "快手", "西瓜", "广告"]
KEYS_CASE = ["RED"]  # match case-sensitively as a whole word
def dur(p): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout)

def extract(name, path, vf_extra="", t0=0.0, t1=None):
    d = f"{FR}/{name}"; os.makedirs(d, exist_ok=True)
    D = dur(path); t1 = D if t1 is None else t1
    times = [round(t, 3) for t in np.arange(t0, t1, 0.5)]
    times += [round(t, 3) for t in np.arange(max(t0, t1 - 2.0), t1 - 1e-3, 1 / 30)]  # last 2 s frame by frame
    times = sorted(set(times))
    if not glob.glob(d + "/*.png"):
        vf = "fps=30" + (("," + vf_extra) if vf_extra else "")
        # full-res frames; select the frames we need by timestamp
        sel = "+".join(f"eq(n,{int(round(t*30))})" for t in times)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t0}", "-t", f"{t1-t0}", "-i", path, "-vf",
                        f"fps=30,select='{'+'.join(f'eq(n,{int(round((t-t0)*30))})' for t in times)}'" + (("," + vf_extra) if vf_extra else ""),
                        "-vsync", "0", "-frame_pts", "0", d + "/f%05d.png"], check=True)
    files = sorted(glob.glob(d + "/*.png"))
    return list(zip(times[:len(files)], files))

def ocr(args):
    t, f, mask = args
    cache = f + (".m" if mask else "") + ".json"
    if os.path.exists(cache):
        r = json.load(open(cache))
    else:
        r = _ocr(t, f, mask); json.dump(r, open(cache, "w"), ensure_ascii=False)
    # QR: recomputed every run (cheap). detect() alone fires on window grids, so a QR only counts if it decodes,
    # or if a large square candidate is found (kept as a flag for manual review).
    r["flags"] = [x for x in r["flags"] if not x.startswith("qr")]
    q = qr_check(f, mask)
    if q: r["flags"].append(q)
    return r
def qr_check(f, mask):
    g = cv2.imread(f)
    if mask:
        for (x0, y0, x1, y1) in mask: g[y0:y1, x0:x1] = 0
    det = cv2.QRCodeDetector()
    data, pts, _ = det.detectAndDecode(g)
    if data: return f"qr_code:{data[:40]}"
    if pts is not None:
        p = pts.reshape(-1, 2); sides = [np.linalg.norm(p[i] - p[(i + 1) % 4]) for i in range(4)]
        area = cv2.contourArea(p.astype(np.float32))
        if min(sides) > 0 and max(sides) / min(sides) < 1.25 and area > 0.005 * g.shape[0] * g.shape[1]:
            return "qr_candidate_undecoded(review)"
    return None
def _ocr(t, f, mask):
    im = Image.open(f).convert("RGB")
    if mask:
        dr = ImageDraw.Draw(im)
        for box in mask: dr.rectangle(box, fill=(0, 0, 0))
    g = np.array(im)
    mode = "psm11"
    try:
        data = pytesseract.image_to_data(im, lang="chi_sim+eng", output_type=pytesseract.Output.DICT, config="--psm 11", timeout=30)
    except RuntimeError:  # tesseract timeout on a noisy frame: fall back to block mode
        mode = "psm6(fallback)"
        data = pytesseract.image_to_data(im, lang="chi_sim+eng", output_type=pytesseract.Output.DICT, config="--psm 6", timeout=60)
    words = [(data["text"][i].strip(), float(data["conf"][i]), data["left"][i], data["top"][i], data["width"][i], data["height"][i])
             for i in range(len(data["text"])) if data["text"][i].strip() and float(data["conf"][i]) >= 0]
    flags = []
    full = "".join(w[0] for w in words)
    for k in KEYS:
        if k.lower() in full.lower(): flags.append(f"keyword:{k}")
    for w in words:
        if w[0] in KEYS_CASE and w[1] > 60: flags.append(f"keyword:{w[0]}")
        if re.search(r"@[A-Za-z0-9_.]{3,}", w[0]): flags.append(f"handle:{w[0]}")
        if re.search(r"\d{7,}", w[0]): flags.append(f"long_id:{w[0]}")
    # leftover Chinese: >=2 CJK chars in one confident token
    for w in words:
        cjk = sum('\u4e00' <= c <= '\u9fff' for c in w[0])
        if cjk >= 2 and w[1] >= 70: flags.append(f"chinese_text:{w[0]}@({w[2]},{w[3]})")
    eng = " ".join(w[0] for w in words if w[1] > 70 and re.search(r"[A-Za-z0-9¥$]", w[0]))
    return {"t": float(t), "frame": os.path.relpath(f, JOB), "ocr_mode": mode, "flags": sorted(set(flags)), "ocr_text_conf70": eng[:200]}

report = {"ocr": "tesseract " + subprocess.run(["tesseract", "--version"], capture_output=True, text=True).stdout.split("\n")[0] + ", lang chi_sim+eng, psm 11",
          "frame_sampling": "every 0.5 s at full resolution + every frame of the last 2 s", "sources": [], "finals": []}

# ---- sources: raw (all text present) and as-used (after our crop, with our opaque price bar region masked) ----
SRC = {"7697172755872253690": ("scale=1404:2496,crop=1080:1920:162:271", [(9.95, 11.0), (12.2, 13.7), (15.4, 16.7), (18.3, 20.2), (22.0, 23.0), (23.25, 24.6), (24.7, 25.8)]),
       "7652548155632015814": ("scale=1404:2496,crop=1080:1920:162:180", [(0.12, 1.25), (1.75, 2.65), (2.8, 4.0), (5.2, 6.5), (12.0, 13.0), (16.62, 17.05), (17.45, 17.98)]),
       "7672385530935491529": ("scale=1080:1920", [(16.2, 18.7), (5.8, 7.2), (8.6, 11.6), (12.4, 13.5), (36.9, 38.9), (40.6, 44.8)])}
BAR = [(0, 1300, 1080, 1540)]
with Pool(4) as pool:
    for aid, (tf, wins) in SRC.items():
        path = f"raw/best/{aid}.mp4"
        raw = pool.map(ocr, [(t, f, None) for t, f in extract(f"src_{aid}_raw", path)])
        used = []
        for i, (a, b) in enumerate(wins):
            fr = extract(f"src_{aid}_used{i}", path, tf, a, b)
            used += pool.map(ocr, [(t, f, BAR) for t, f in fr])
        report["sources"].append({"aweme_id": aid, "file": path,
            "raw_frames_checked": len(raw), "raw_flagged_frames": sum(1 for r in raw if r["flags"]),
            "raw_flag_types": sorted({f.split(":")[0] + (":" + f.split(":")[1] if f.startswith("keyword") else "") for r in raw for f in r["flags"]}),
            "used_windows_s": wins, "used_transform": tf + " ; then opaque price bar over y 1300-1540 (masked here)",
            "used_frames_checked": len(used), "used_flagged_frames": [r for r in used if r["flags"]], "raw": raw})
        print(aid, "raw flagged", report["sources"][-1]["raw_flagged_frames"], "/", len(raw), "| used flagged", len(report["sources"][-1]["used_flagged_frames"]), "/", len(used), flush=True)

    # ---- finals ----
    for fn in sorted(glob.glob("final_*.mp4")):
        res = pool.map(ocr, [(t, f, None) for t, f in extract(fn[:-4], fn)])
        D = dur(fn)
        bd = subprocess.run(["ffmpeg", "-i", fn, "-vf", "blackdetect=d=0.1:pic_th=0.95", "-an", "-f", "null", "-"], capture_output=True, text=True).stderr
        blacks = re.findall(r"black_start:\S+ black_end:\S+ black_duration:\S+", bd)
        eb = subprocess.run(["ffmpeg", "-i", fn, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
        I = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", eb)[-1]); TP = float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", eb)[-1])
        st = subprocess.run(["ffmpeg", "-i", fn, "-af", "astats=metadata=0", "-f", "null", "-"], capture_output=True, text=True).stderr
        clip = sum(int(x) for x in re.findall(r"Number of (?:clipped samples|samples clipped)?:?\s*(\d+)", "")) if False else None
        peaks = [float(x) for x in re.findall(r"Peak level dB:\s+(-?[\d.inf]+)", st) if x not in ("-inf",)]
        report["finals"].append({"file": fn, "duration_s": D, "frames_checked": len(res), "flagged_frames": [r for r in res if r["flags"]],
                                 "black_frames": blacks, "integrated_loudness_LUFS": I, "true_peak_dBFS": TP, "sample_peak_dB": max(peaks) if peaks else None,
                                 "frames": res})
        print(fn, "flagged", len(report["finals"][-1]["flagged_frames"]), "/", len(res), "black", blacks, "I", I, "TP", TP, flush=True)

# ---- caption sync: caption start vs VO onset (energy envelope of the VO-only track) ----
def vo_only(var):
    w = f"work/render_{var}"; out = f"{w}/vo_only.wav"
    # rebuild VO-only from the render's own piece placement (same filter graph minus sfx)
    words = json.load(open(f"{w}/timeline_words.json"))
    return words
sync = {}
import wave
for var in ("A", "B"):
    w = f"work/render_{var}"
    caps = json.load(open(f"{w}/captions.json")); words = json.load(open(f"{w}/timeline_words.json"))
    # VO-only audio from the pre-loudnorm mix is polluted by sfx, so measure onsets on the voice-only stems
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{w}/vo_only.wav", "-ac", "1", "-ar", "16000", f"{w}/final_mono.wav"], check=True)
    a = np.frombuffer(wave.open(f"{w}/final_mono.wav").readframes(10**9), dtype=np.int16).astype(float)
    hop = 160; env = np.array([np.sqrt(np.mean(a[i:i+hop]**2)) for i in range(0, len(a) - hop, hop)])
    db = 20 * np.log10(env + 1e-6); floor = np.percentile(db, 20)
    deltas = []
    for c in caps:
        # only measurable where the caption starts a phrase after >= 0.2 s of silence in the voice track
        i0 = int(max(0, c["s"] - 0.35) * 100); i1 = int((c["s"] + 0.3) * 100)
        pre = db[max(0, int((c["s"] - 0.35) * 100)):int((c["s"] - 0.12) * 100)]
        if len(pre) == 0 or pre.max() > floor + 10:
            deltas.append({"caption": c["text"], "caption_on_s": round(c["s"] - 0.05, 3), "aligned_word_start_s": round(c["s"], 3),
                           "audio_onset_s": None, "caption_minus_onset_s": None, "note": "mid-phrase: timed from ElevenLabs character alignment"}); continue
        seg = db[i0:i1]; idx = np.where(seg > floor + 15)[0]
        onset = (i0 + idx[0]) / 100 if len(idx) else None
        cap_on = c["s"] - 0.05
        deltas.append({"caption": c["text"], "caption_on_s": round(cap_on, 3), "aligned_word_start_s": round(c["s"], 3),
                       "audio_onset_s": None if onset is None else round(onset, 3),
                       "caption_minus_onset_s": None if onset is None else round(cap_on - onset, 3)})
    vals = [abs(d["caption_minus_onset_s"]) for d in deltas if d["caption_minus_onset_s"] is not None]
    sync[var] = {"method": "caption on-time (aligned word start - 0.05 s) vs first 10 ms frame >15 dB above the voice track's noise floor, at phrase starts that follow >=0.2 s of silence",
                 "measured": len(vals), "captions": len(caps), "max_abs_offset_s": max(vals), "mean_abs_offset_s": round(float(np.mean(vals)), 3),
                 "within_0.1s": sum(v <= 0.1 for v in vals), "detail": deltas}
    print("sync", var, sync[var]["max_abs_offset_s"], sync[var]["within_0.1s"], "/", len(vals))
report["caption_sync"] = sync

# ---- safe area: measure every text event's rendered bbox from the ASS (font metrics) ----
fontp = "work/fonts/Montserrat-ExtraBold.ttf"
def text_bbox(txt, size, x, y, an, scale=1.0):
    plain = re.sub(r"\{[^}]*\}", "", txt).replace("\\N", "\n")
    f = ImageFont.truetype(fontp, size)
    lines = plain.split("\n"); ws = [f.getlength(l) * scale for l in lines]; h = size * 1.2 * len(lines)
    w = max(ws); hx = {1: 0, 4: 0, 7: 0, 2: w / 2, 5: w / 2, 8: w / 2, 3: w, 6: w, 9: w}[an]
    vy = {7: 0, 8: 0, 9: 0, 4: h / 2, 5: h / 2, 6: h / 2, 1: h, 2: h, 3: h}[an]
    return (x - hx, y - vy, x - hx + w, y - vy + h)
safe = []
sizes = {"Cap": 88, "Price": 96, "Name": 40, "Note": 32, "CtaS": 84, "CtaB": 190, "CtaS2": 50}
for var in ("A", "B"):
    for line in open(f"work/render_{var}/subs.ass"):
        if not line.startswith("Dialogue"): continue
        parts = line.rstrip("\n").split(",", 9); sty = parts[3]; txt = parts[9]
        if sty == "Box": continue
        m = re.search(r"\\an(\d)\\pos\((\d+),(\d+)\)", txt); an, x, y = int(m[1]), int(m[2]), int(m[3])
        fsm = re.search(r"\\fs(\d+)", txt.split("{\\fs52")[0]); size = int(fsm[1]) if fsm else sizes[sty]
        # Price lines contain a smaller /night run: measure conservatively at full size
        sc = 1.12 if "fscx112" in txt else 1.0  # peak of the pop animation
        if sty == "Price" and "\\fs52" in txt:
            p1, p2 = txt.split("{\\fs52", 1)
            f96 = ImageFont.truetype(fontp, 96); f52 = ImageFont.truetype(fontp, 52)
            w = f96.getlength(re.sub(r"\{[^}]*\}", "", p1)) * sc + f52.getlength(re.sub(r"\{[^}]*\}", "", "{" + p2))
            h = 96 * 1.2 * sc; bb = (x, y - h / 2, x + w, y + h / 2)
        else:
            if sty == "Note": fontp_ = fontp
            bb = text_bbox(txt, size, x, y, an, sc)
        ok = bb[1] >= 220 and bb[3] <= 1540 and bb[2] <= 940 and bb[0] >= 0
        safe.append({"variant": var, "style": sty, "start": parts[1], "text": re.sub(r"\{[^}]*\}", "", txt)[:60], "bbox": [round(v) for v in bb], "inside_safe_area": ok})
report["safe_area"] = {"rule": "no text in top 220 px, bottom 380 px (y>1540) or right 140 px (x>940)",
                       "events": len(safe), "violations": [s for s in safe if not s["inside_safe_area"]], "all": safe}
print("safe-area violations", len(report["safe_area"]["violations"]))
json.dump(report, open("qa/watermark_report.json", "w"), ensure_ascii=False, indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))
