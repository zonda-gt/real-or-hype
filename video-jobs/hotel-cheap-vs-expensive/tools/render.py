#!/usr/bin/env python3
"""Render the ¥200 vs ¥6,000 Shanghai hotel reel.  usage: render.py A|B [music]"""
import json, os, re, subprocess, sys

JOB = "/home/user/real-or-hype/video-jobs/hotel-cheap-vs-expensive"
os.chdir(JOB)
VAR = sys.argv[1]
MUSIC = len(sys.argv) > 2 and sys.argv[2] == "music"
W = f"work/render_{VAR}{'_m' if MUSIC else ''}"
os.makedirs(W, exist_ok=True)
SFX = "/home/user/real-or-hype/.claude/skills/real-or-hype-video/sfx"
FPS = 30

SRC = {
    "G": ("raw/best/7697172755872253690.mp4", "scale=1404:2496,crop=1080:1920:162:271"),
    "S": ("raw/best/7652548155632015814.mp4", "scale=1404:2496,crop=1080:1920:162:180"),
    "B": ("raw/best/7672385530935491529.mp4", "scale=1080:1920,eq=gamma=1.15:saturation=1.08"),
}

HOOK = 5.5
# (timeline start, timeline end, source key, src start, src end)
SHOTS = [
    # tier 1: VX Gefei Hotel (~¥200/night deal)
    (5.50, 6.90, "G", 9.95, 11.00),    # room wide
    (6.90, 7.90, "G", 23.25, 24.60),   # dry/wet separated bathroom sink
    (7.90, 9.30, "G", 15.40, 16.70),   # robot butler in lobby
    (9.30, 11.20, "G", 12.20, 13.70),  # bed + window (no view)
    # tier 2: Sheraton Pudong Riverside (~¥500/night deal)
    (11.20, 12.40, "S", 2.80, 4.00),   # tower exterior
    (12.40, 13.30, "S", 1.75, 2.65),   # bed with river view
    (13.30, 14.80, "S", 0.12, 1.25),   # desk + Bund across the river
    (14.80, 16.10, "S", 5.20, 6.50),   # lobby chandelier
    (16.10, 16.70, "S", 16.62, 17.05), # bathtub + mirror
    (16.70, 17.60, "S", 17.45, 17.98), # bathtub
    # tier 3: Banyan Tree On The Bund suite (¥6,000+/night)
    (17.60, 19.00, "B", 5.80, 7.20),   # suite living room, skyline windows
    (19.00, 20.10, "B", 12.40, 13.50), # corner windows onto Lujiazui towers
    (20.10, 23.00, "B", 36.90, 38.90), # round bathtub facing the river skyline (slow-mo)
    # verdict: back to the Sheraton view
    (23.00, 24.30, "S", 0.12, 1.25),
    (24.30, 25.60, "S", 1.75, 2.65),
    (25.60, 26.60, "S", 12.00, 13.00), # night room with river view
    # CTA background
    (26.60, 30.80, "B", 40.60, 44.80),
]
END = 30.80
HOOK_L = [("G", 12.20, 13.70), ("G", 18.30, 20.20), ("G", 22.00, 23.00), ("G", 24.70, 25.80)]
HOOK_R = [("B", 16.20, 18.70), ("B", 8.60, 11.60)]

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        print(r.stderr[-2000:]); sys.exit(1)

def shot(key, a, b, dur, out, half=False):
    path, tf = SRC[key]
    spd = dur / (b - a)
    vf = f"{tf},setpts=(PTS-STARTPTS)*{spd:.5f},fps={FPS}"
    if half:
        vf += ",crop=540:1920:270:0"
    vf += ",format=yuv420p"
    run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a:.3f}", "-t", f"{b-a+0.2:.3f}", "-i", path, "-an", "-vf", vf,
         "-t", f"{dur:.3f}", "-c:v", "libx264", "-preset", "fast", "-crf", "14", "-r", str(FPS), out])

def concat(files, out):
    lst = out + ".txt"
    open(lst, "w").write("".join(f"file '{os.path.abspath(f)}'\n" for f in files))
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", out])

# ---------- video ----------
segs = []
if not os.path.exists(f"{W}/video.mp4"):
    for side, lst in (("L", HOOK_L), ("R", HOOK_R)):
        parts = []
        tot = sum(b - a for _, a, b in lst)
        for i, (k, a, b) in enumerate(lst):
            p = f"{W}/hook{side}{i}.mp4"
            shot(k, a, b, (b - a) * HOOK / tot, p, half=True); parts.append(p)
        concat(parts, f"{W}/hook{side}.mp4")
    run(["ffmpeg", "-v", "error", "-y", "-i", f"{W}/hookL.mp4", "-i", f"{W}/hookR.mp4", "-filter_complex",
         "[0:v][1:v]hstack=inputs=2,trim=duration=%.3f,setpts=PTS-STARTPTS[v]" % HOOK, "-map", "[v]",
         "-c:v", "libx264", "-preset", "fast", "-crf", "14", "-r", str(FPS), f"{W}/hook.mp4"])
    segs.append(f"{W}/hook.mp4")
    for i, (t0, t1, k, a, b) in enumerate(SHOTS):
        p = f"{W}/s{i:02d}.mp4"; shot(k, a, b, t1 - t0, p); segs.append(p)
    concat(segs, f"{W}/video.mp4")

# ---------- voice ----------
hook = json.load(open(f"work/vo/hook{VAR}_t.json"))
body = json.load(open("work/vo/body_t.json"))
bw = body["words"]
def idx(word, start=0):
    for i in range(start, len(bw)):
        if bw[i]["w"] == word: return i
    raise KeyError(word)
groups = []  # (first idx, last idx, timeline offset)
iT2 = idx("Five"); iT3 = idx("Six"); iV = idx("My"); iC = idx("Comment")
bounds = [(0, iT2 - 1, 5.60 - bw[0]["s"]),
          (iT2, iT3 - 1, 11.40 - bw[iT2]["s"]),
          (iT3, iV - 1, 17.80 - bw[iT3]["s"]),
          (iV, iC - 1, 23.10 - bw[iV]["s"]),
          (iC, len(bw) - 1, 26.82 - bw[iC]["s"])]
pieces = []  # (src start, src end, timeline position)
tl_words = [dict(w) for w in hook["words"]]
for gi, (i0, i1, off) in enumerate(bounds):
    s = 0.0 if i0 == 0 else (bw[i0 - 1]["e"] + bw[i0]["s"]) / 2
    e = body["duration"] if i1 == len(bw) - 1 else (bw[i1]["e"] + bw[i1 + 1]["s"]) / 2
    pieces.append((s, e, s + off))
    for w in bw[i0:i1 + 1]:
        tl_words.append({"w": w["w"], "s": round(w["s"] + off, 3), "e": round(w["e"] + off, 3)})
for a, b in zip(pieces, pieces[1:]):
    assert a[2] + (a[1] - a[0]) <= b[2] + 0.001, ("VO overlap", a, b)
json.dump(tl_words, open(f"{W}/timeline_words.json", "w"), indent=1)

# ---------- captions (ASS) ----------
MERGE = [(("two", "hundred", "yuan"), "¥200"), (("six", "thousand", "yuan"), "¥6,000"),
         (("six", "thousand", "plus"), "¥6,000+"), (("two", "hundred"), "¥200"),
         (("five", "hundred"), "¥500"), (("six", "thousand"), "¥6,000"), (("thirty", "times"), "30×")]
def bare(w): return re.sub(r"[^\w']", "", w.lower())
toks = []; i = 0
while i < len(tl_words):
    for pat, rep in MERGE:
        n = len(pat)
        if tuple(bare(w["w"]) for w in tl_words[i:i + n]) == pat:
            last = tl_words[i + n - 1]["w"]; punct = re.sub(r"^.*?([.,?!…]*)$", r"\1", last)
            toks.append({"w": rep + punct, "s": tl_words[i]["s"], "e": tl_words[i + n - 1]["e"], "price": True}); i += n; break
    else:
        toks.append(dict(tl_words[i], price=False)); i += 1
FUNC = {"a", "the", "for", "of", "on", "in", "and", "with", "your", "to", "i'll", "you", "is"}
caps = []; cur = []
for t in toks:
    cur.append(t)
    txt = " ".join(x["w"] for x in cur)
    if re.search(r"[.,?!…]$", t["w"]):
        caps.append(cur); cur = []
    elif len(cur) >= 3 or len(txt) >= 13:
        k = len(cur)
        while k > 1 and bare(cur[k - 1]["w"]) in FUNC: k -= 1  # don't end a caption on filler words
        if k < len(cur):
            caps.append(cur[:k]); cur = cur[k:]
        else:
            caps.append(cur); cur = []
if cur: caps.append(cur)

def ts(t):
    t = max(0, t); h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"
def clean(w):  # strip trailing commas/periods on captions; keep ? and …
    return re.sub(r"[.,]+$", "", w).replace("...", "…")

from PIL import ImageFont
CAPF = ImageFont.truetype("work/fonts/Montserrat-ExtraBold.ttf", 88)
YEL = "&H002BD9FF&"; GRN = "&H0066E07A&"; WHT = "&H00FFFFFF&"; NAVY = "&H00301A0E&"
ev = []
for gi, g in enumerate(caps):
    st = g[0]["s"] - 0.05
    nxt = caps[gi + 1][0]["s"] - 0.05 if gi + 1 < len(caps) else 99
    en = min(nxt, g[-1]["e"] + 0.35)
    words = []
    for x in g:
        w = clean(x["w"]).upper() if not x["price"] else clean(x["w"])
        words.append(f"{{\\c{YEL}}}{w}{{\\c{WHT}}}" if x["price"] or bare(x["w"]) == "hotel" else w)
    plain = " ".join(re.sub(r"\{[^}]*\}", "", w) for w in words)
    fs = min(88, int(88 * 840 / CAPF.getlength(plain)))  # fit inside x 70..910 (safe area: right 140 px)
    ev.append(("Cap", st, en, f"{{\\an5\\pos(490,1150)\\fs{fs}\\fscx80\\fscy80\\t(0,90,\\fscx100\\fscy100)}}" + " ".join(words)))

def box(x, y, w, h, col=NAVY, alpha="00"):
    return f"{{\\an7\\pos({x},{y})\\bord0\\shad0\\1c{col}\\1a&H{alpha}&\\p1}}m 0 0 l {w} 0 l {w} {h} l 0 {h}{{\\p0}}"
POP = "\\fscx70\\fscy70\\t(0,120,\\fscx112\\fscy112)\\t(120,220,\\fscx100\\fscy100)"
def tier_bar(t0, t1, price, usd, name, note):
    out = [("Box", t0, t1, box(0, 1300, 1080, 240)),
           ("Box", t0, t1, box(0, 1300, 1080, 8, YEL)),
           ("Price", t0, t1, f"{{\\an4\\pos(44,1366){POP}}}{price}{{\\fs52\\c{WHT}}} /night  {{\\c{GRN}}}≈ {usd}"),
           ("Name", t0, t1, f"{{\\an4\\pos(46,1450)}}{name}"),
           ("Note", t0, t1, f"{{\\an4\\pos(46,1505)}}{note}")]
    return out

hook_ts = {"A": (0.05, 1.12), "B": (2.05, 4.33)}[VAR]
# hook: split screen with two price tags (cheap left first, then expensive right)
ev += [("Box", 0, HOOK, box(536, 0, 8, 1920, WHT)),
       # boxes are up from frame 0: they also cover the source's burned-in subtitle band
       ("Box", 0, HOOK, box(0, 1300, 536, 240)), ("Box", 0, HOOK, box(544, 1300, 536, 240)),
       ("Box", 0, HOOK, box(0, 1300, 536, 8, YEL)), ("Box", 0, HOOK, box(544, 1300, 536, 8, YEL)),
       ("Name", 0, hook_ts[0], "{\\an5\\pos(268,1420)}CHEAPEST"), ("Name", 0, hook_ts[1], "{\\an5\\pos(728,1420)}PRICIEST"),
       ("Price", hook_ts[0], HOOK, f"{{\\an5\\pos(268,1385)\\fs84{POP}}}¥200+"),
       ("Name", hook_ts[0], HOOK, f"{{\\an5\\pos(268,1470)\\c{GRN}}}≈ $30 /night"),
       ("Price", hook_ts[1], HOOK, f"{{\\an5\\pos(728,1385)\\fs84{POP}}}¥6,000+"),
       ("Name", hook_ts[1], HOOK, f"{{\\an5\\pos(728,1470)\\c{GRN}}}≈ $900 /night")]
ev += tier_bar(5.50, 11.20, "¥200+", "$30", "VX Gefei Hotel · North Bund", "Huangxing Rd branch · deal: ¥400+ for 2 nights")
ev += tier_bar(11.20, 17.60, "¥500+", "$75", "Sheraton Pudong Riverside · Pudong", "Deal: ¥1,000+ for 2 nights, breakfast for 2")
ev += tier_bar(17.60, 23.00, "¥6,000+", "$900", "Banyan Tree On The Bund · Hongkou", "Supreme River View Suite")
ev += [("Box", 23.0, 26.6, box(0, 1300, 1080, 240)), ("Box", 23.0, 26.6, box(0, 1300, 1080, 8, GRN)),
       ("Price", 23.0, 26.6, f"{{\\an4\\pos(44,1366){POP}\\c{GRN}}}BEST VALUE"),
       ("Name", 23.0, 26.6, "{\\an4\\pos(46,1450)}Sheraton Pudong Riverside · ¥500+ ≈ $75"),
       ("Note", 23.0, 26.6, "{\\an4\\pos(46,1505)}River view + breakfast, ~1/12 of the suite price")]
ev += [("Box", 26.6, END, box(0, 0, 1080, 1920, "&H00000000&", "50")),
       ("CtaS", 26.6, END, f"{{\\an5\\pos(500,560)\\fad(150,0)}}COMMENT"),
       ("CtaB", 26.6, END, f"{{\\an5\\pos(500,720){POP}}}HOTEL"),
       ("CtaS2", 26.6, END, "{\\an5\\pos(500,880)\\fad(200,0)}and I'll send you the full list\\Nwith prices and locations")]

def _check():
    sizes = {"Cap": 88, "Price": 96, "Name": 40, "Note": 32, "CtaS": 84, "CtaB": 190, "CtaS2": 50}
    for sty, a, b, txt in ev:
        if sty == "Box": continue
        m = re.search(r"\\an(\d)\\pos\((\d+),(\d+)\)", txt); an, x, y = int(m[1]), int(m[2]), int(m[3])
        fsm = re.search(r"\\fs(\d+)(?!.*\\fs52)", txt.split("{\\fs52")[0]); size = int(fsm[1]) if fsm else sizes[sty]
        f = ImageFont.truetype("work/fonts/Inter-SemiBold.otf" if sty == "Note" else "work/fonts/Montserrat-ExtraBold.ttf", size)
        sc = 1.12 if "fscx112" in txt else 1.0
        if "{\\fs52" in txt:
            p1, p2 = txt.split("{\\fs52", 1)
            w = f.getlength(re.sub(r"\{[^}]*\}", "", p1)) * sc + ImageFont.truetype("work/fonts/Montserrat-ExtraBold.ttf", 52).getlength(re.sub(r"\{[^}]*\}", "", "{" + p2))
        else:
            w = max(f.getlength(l) for l in re.sub(r"\{[^}]*\}", "", txt).split("\\N")) * sc
        left = x if an in (1, 4, 7) else x - w / 2
        h = size * 1.2 * (txt.count("\\N") + 1) * sc
        top = y - h / 2 if an in (4, 5, 6) else y
        assert left >= 0 and left + w <= 940 and top >= 220 and top + h <= 1540, ("SAFE AREA", sty, txt, left, left + w, top, top + h)
_check()
ass = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Montserrat ExtraBold,88,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,7,3,5,40,140,0,1
Style: Box,Montserrat ExtraBold,20,&H00301A0E,&H00301A0E,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1
Style: Price,Montserrat ExtraBold,96,{YEL},{YEL},&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,4,0,4,0,0,0,1
Style: Name,Montserrat ExtraBold,40,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,4,0,0,0,1
Style: Note,Inter SemiBold,32,&H00D8D8D8,&H00D8D8D8,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,4,0,0,0,1
Style: CtaS,Montserrat ExtraBold,84,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,6,0,5,0,0,0,1
Style: CtaB,Montserrat ExtraBold,190,{YEL},{YEL},&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,9,4,5,0,0,0,1
Style: CtaS2,Montserrat ExtraBold,50,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,5,0,5,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
layer = {"Box": 0, "Price": 2, "Name": 2, "Note": 2, "Cap": 3, "CtaS": 2, "CtaB": 2, "CtaS2": 2}
for sty, a, b, txt in ev:
    ass += f"Dialogue: {layer[sty]},{ts(a)},{ts(b)},{sty},,0,0,0,,{txt}\n"
open(f"{W}/subs.ass", "w").write(ass)
json.dump([{"text": " ".join(x["w"] for x in g), "s": g[0]["s"], "e": g[-1]["e"]} for g in caps], open(f"{W}/captions.json", "w"), indent=1)

# ---------- audio ----------
inputs = ["-i", f"work/vo/hook{VAR}_t.wav", "-i", "work/vo/body_t.wav", "-i", f"{SFX}/pop_es.wav", "-i", f"{SFX}/whoosh_es.wav"]
fl = ["[0:a]aresample=48000,adelay=0|0[h]"]
mix = ["[h]"]
for i, (s, e, pos) in enumerate(pieces):
    fl.append(f"[1:a]atrim={s:.3f}:{e:.3f},asetpts=PTS-STARTPTS,aresample=48000,adelay={int(pos*1000)}|{int(pos*1000)}[b{i}]"); mix.append(f"[b{i}]")
pops = [hook_ts[0], hook_ts[1], 5.50, 11.20, 17.60, 23.00, 26.60]
whooshes = [5.40, 11.10, 17.50, 22.90]
fl.append(f"[2:a]asplit={len(pops)}" + "".join(f"[p{i}]" for i in range(len(pops))))
for i, t in enumerate(pops):
    fl.append(f"[p{i}]volume=0.35,adelay={int(t*1000)}|{int(t*1000)}[pp{i}]"); mix.append(f"[pp{i}]")
fl.append(f"[3:a]asplit={len(whooshes)}" + "".join(f"[w{i}]" for i in range(len(whooshes))))
for i, t in enumerate(whooshes):
    fl.append(f"[w{i}]volume=0.30,adelay={int(t*1000)}|{int(t*1000)}[ww{i}]"); mix.append(f"[ww{i}]")
if MUSIC:
    inputs += ["-i", "work/musicbed.wav"]
    fl.append(f"[4:a]volume=0.13,atrim=0:{END},afade=t=out:st={END-1.2}:d=1.2[mu]"); mix.append("[mu]")
fl.append("".join(mix) + f"amix=inputs={len(mix)}:normalize=0:duration=longest,atrim=0:{END},apad=whole_dur={END}[mx]")
vo_fl = [x for x in fl if x.startswith("[0:a]") or x.startswith("[1:a]")]
vo_mix = "[h]" + "".join(f"[b{i}]" for i in range(len(pieces)))
run(["ffmpeg", "-v", "error", "-y", "-i", f"work/vo/hook{VAR}_t.wav", "-i", "work/vo/body_t.wav", "-filter_complex",
     ";".join(vo_fl + [vo_mix + f"amix=inputs={len(pieces)+1}:normalize=0:duration=longest,atrim=0:{END}[vo]"]), "-map", "[vo]", "-ac", "1", "-ar", "48000", f"{W}/vo_only.wav"])
pre = f"{W}/mix_pre.wav"
run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(fl), "-map", "[mx]", "-ac", "2", "-ar", "48000", pre])
# two-pass loudnorm to -14 LUFS
r = subprocess.run(["ffmpeg", "-v", "info", "-i", pre, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"], capture_output=True, text=True)
m = json.loads(r.stderr[r.stderr.rfind("{"):r.stderr.rfind("}") + 1])
ln = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}"
      f":measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
run(["ffmpeg", "-v", "error", "-y", "-i", pre, "-af", ln + ",aresample=48000", "-ar", "48000", f"{W}/mix.wav"])

# ---------- final ----------
out = f"final_{VAR}{'_music' if MUSIC else ''}.mp4"
run(["ffmpeg", "-v", "error", "-y", "-i", f"{W}/video.mp4", "-i", f"{W}/mix.wav",
     "-vf", f"subtitles={W}/subs.ass:fontsdir=work/fonts", "-map", "0:v", "-map", "1:a",
     "-c:v", "libx264", "-preset", "slow", "-crf", "19", "-pix_fmt", "yuv420p", "-r", str(FPS), "-profile:v", "high",
     "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-t", f"{END}", "-movflags", "+faststart", out])
print("wrote", out)
