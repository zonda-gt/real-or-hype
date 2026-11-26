# build_hf.py <project_dir> <plan.json>
# Writes a HyperFrames project for a talking-head reel in the reference style:
#   aroll (jump-cut segments, punch-ins, zoom-blur whips) < broll cutaways < cards (titles, colour cards, comment pill) < captions.
# plan.json: {"duration", "aroll":[{k,start,dur,scale}], "broll":[{id,src,start,dur}], "captions":[{start,end,words:[[text,t,style]]}],
#             "cards":[...], "sfx":[[file,t,vol]], "music":{file,vol}}
import json, sys, html, os

P, plan = sys.argv[1], json.load(open(sys.argv[2]))
DUR = plan["duration"]
W, H = 1080, 1920
os.makedirs(f"{P}/compositions", exist_ok=True)

FONTS = """
@font-face { font-family: "Inter Display HF"; src: url("assets/fonts/InterDisplay-Bold.otf"); font-weight: 700; }
@font-face { font-family: "Inter Display HF"; src: url("assets/fonts/InterDisplay-SemiBold.otf"); font-weight: 600; }
@font-face { font-family: "Inter Display Heavy"; src: url("assets/fonts/InterDisplay-BlackItalic.otf"); font-weight: 900; font-style: italic; }
@font-face { font-family: "Instrument Serif HF"; src: url("assets/fonts/InstrumentSerif-Italic.ttf"); font-style: italic; }
@font-face { font-family: "Playfair HF"; src: url("assets/fonts/PlayfairDisplay-BoldItalic.ttf"); font-weight: 700; font-style: italic; }
"""
TOKENS = """
  --ink: #f5efe6;        /* warm off-white, as in the reference captions */
  --accent: #c8161d;     /* reference red */
  --cream: #efe6d8;
  --navy: #101a20;
"""

def f3(x): return f"{x:.3f}"

def scene(cid, z, body, script, extra_css=""):
    return f"""<template>
  <style>
    {FONTS}
    #{cid} {{ position: absolute; inset: 0; z-index: {z}; {TOKENS} }}
    {extra_css}
  </style>
  <div id="{cid}" data-composition-id="{cid}" data-width="{W}" data-height="{H}" data-layout-allow-overflow>
{body}
  </div>
  <script>
    window.__timelines = window.__timelines || {{}};
    const tl = gsap.timeline({{ paused: true }});
{script}
    window.__timelines["{cid}"] = tl;
  </script>
</template>
"""

# ---------- A-roll: every take its own <video>, one wrapper carries punch-ins and whips ----------
body, js = [], ['    tl.set("#aroll-cam", { scale: 1, filter: "blur(0px)" }, 0);']
body.append('    <div id="aroll-cam" class="cam">')
for s in plan["aroll"]:
    body.append(f'      <video id="a-{s["k"]}" class="clip seg" src="assets/aroll/{s["k"]}.mp4" data-start="{f3(s["start"])}" data-duration="{f3(s["dur"])}" data-track-index="0" muted playsinline></video>')
body.append('    </div>')
for s in plan["aroll"]:
    sc = s.get("scale", 1.0)
    if s.get("whip"):      # zoom-blur arrival, as the reference's cuts
        js.append(f'    tl.fromTo("#aroll-cam", {{ scale: {sc*1.16:.3f}, filter: "blur(14px)" }}, {{ scale: {sc}, filter: "blur(0px)", duration: 0.22, ease: "expo.out" }}, {f3(s["start"])});')
    else:
        js.append(f'    tl.set("#aroll-cam", {{ scale: {sc}, filter: "blur(0px)" }}, {f3(s["start"])});')
css = """.cam { position: absolute; inset: 0; transform-origin: 50% 30%; }
    .seg { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }"""
open(f"{P}/compositions/aroll.html", "w").write(scene("aroll", 1, "\n".join(body), "\n".join(js), css))

# ---------- B-roll cutaways ----------
body, js = ['    <div id="broll-cam" class="cam">'], ['    tl.set("#broll-cam", { scale: 1, filter: "blur(0px)" }, 0);']
for b in plan["broll"]:
    body.append(f'      <video id="b-{b["id"]}" class="clip seg" src="assets/broll/{b["src"]}.mp4" data-start="{f3(b["start"])}" data-duration="{f3(b["dur"])}" data-track-index="0" muted playsinline></video>')
    js.append(f'    tl.fromTo("#broll-cam", {{ scale: 1.2, filter: "blur(16px)" }}, {{ scale: 1.0, filter: "blur(0px)", duration: 0.24, ease: "expo.out" }}, {f3(b["start"])});')
    # slow drift inside the shot so stills of buildings never look frozen
    js.append(f'    tl.fromTo("#b-{b["id"]}", {{ scale: 1.0 }}, {{ scale: 1.06, duration: {f3(b["dur"])}, ease: "none" }}, {f3(b["start"])});')
body.append('    </div>')
css = """.cam { position: absolute; inset: 0; transform-origin: 50% 50%; }
    .seg { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }"""
open(f"{P}/compositions/broll.html", "w").write(scene("broll", 2, "\n".join(body), "\n".join(js), css))

# ---------- Cards: colour cards, stacked titles, comment pill ----------
body, js = [], []
for i, c in enumerate(plan["cards"]):
    cid = f"card{i}"
    st, du = c["start"], c["dur"]
    if c["kind"] in ("cream", "navy"):
        words = "".join(f'<span class="w" id="{cid}-w{j}">{html.escape(t)}</span> ' for j, (t, _) in enumerate(c["words"]))
        body.append(f'    <div id="{cid}" class="clip full {c["kind"]}" data-start="{f3(st)}" data-duration="{f3(du)}" data-track-index="1"><div class="card-text">{words.strip()}</div></div>')
        for j, (t, wt) in enumerate(c["words"]):
            js.append(f'    tl.fromTo("#{cid}-w{j}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.04 }}, {f3(max(st, wt - 0.03))});')
    elif c["kind"] == "title":
        lines = []
        j = 0
        for ln in c["lines"]:
            spans = []
            for t, wt in ln["words"]:
                spans.append(f'<span class="w" id="{cid}-w{j}">{html.escape(t)}</span>')
                js.append(f'    tl.fromTo("#{cid}-w{j}", {{ opacity: 0, filter: "blur(10px)" }}, {{ opacity: 1, filter: "blur(0px)", duration: 0.13, ease: "power3.out" }}, {f3(max(st, wt - 0.03))});')
                j += 1
            lines.append(f'<div class="tl {ln["style"]}" style="font-size:{ln["size"]}px">{" ".join(spans)}</div>')
        body.append(f'    <div id="{cid}" class="clip title" data-start="{f3(st)}" data-duration="{f3(du)}" data-track-index="1" style="top:{c["top"]}px">{"".join(lines)}</div>')
        js.append(f'    tl.to("#{cid}", {{ opacity: 0, filter: "blur(8px)", duration: 0.12, ease: "power2.in" }}, {f3(st + du - 0.12)});')
        js.append(f'    tl.set("#{cid}", {{ opacity: 1, filter: "blur(0px)" }}, {f3(st)});')
    elif c["kind"] == "pill":
        body.append(f'''    <div id="{cid}" class="clip pillwrap" data-start="{f3(st)}" data-duration="{f3(du)}" data-track-index="1" style="top:{c["top"]}px">
      <div class="pill" id="{cid}-pill"><span class="pill-text">&ldquo;{html.escape(c["text"])}&rdquo;</span>
        <span class="pill-send"><svg viewBox="0 0 24 24" width="40" height="40"><path d="M12 19V6M6 11.5 12 5.5l6 6" fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg></span></div>
    </div>''')
        js.append(f'    tl.fromTo("#{cid}-pill", {{ scale: 0.7, opacity: 0, y: 30 }}, {{ scale: 1, opacity: 1, y: 0, duration: 0.42, ease: "back.out(1.7)" }}, {f3(st)});')
css = """.full { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; }
    .cream { background: var(--cream); color: var(--accent); }
    .navy { background: var(--navy); color: var(--ink); }
    .card-text { font-family: "Inter Display HF"; font-weight: 700; font-size: 104px; letter-spacing: -0.05em; text-align: center; padding: 0 120px; line-height: 1.0; }
    .title { position: absolute; left: 0; width: 1080px; text-align: center; }
    .tl { line-height: 0.88; white-space: nowrap; }
    .heavy { font-family: "Inter Display Heavy"; font-weight: 900; font-style: italic; color: var(--ink); letter-spacing: -0.045em; text-transform: uppercase; text-shadow: 0 6px 30px rgba(0,0,0,0.35); }
    .heavy-red { font-family: "Inter Display Heavy"; font-weight: 900; font-style: italic; color: var(--accent); letter-spacing: -0.045em; text-transform: uppercase; text-shadow: 0 6px 30px rgba(0,0,0,0.25); }
    .serif-red { font-family: "Playfair HF"; font-weight: 700; font-style: italic; color: #d4494f; letter-spacing: -0.03em; margin: -4px 0 18px; text-shadow: 0 0 2px rgba(255,255,255,0.35), 0 4px 18px rgba(0,0,0,0.25); }
    .pillwrap { position: absolute; left: 0; width: 1080px; display: flex; justify-content: center; }
    .pill { width: 760px; height: 116px; border-radius: 58px; background: #f7f3ee; display: flex; align-items: center; justify-content: space-between; padding: 0 18px 0 46px; box-shadow: 0 10px 40px rgba(0,0,0,0.35); }
    .pill-text { font-family: "Inter Display HF"; font-weight: 700; font-size: 50px; letter-spacing: -0.03em; color: #111; }
    .pill-send { width: 80px; height: 80px; border-radius: 40px; background: var(--accent); display: flex; align-items: center; justify-content: center; }"""
open(f"{P}/compositions/cards.html", "w").write(scene("cards", 3, "\n".join(body), "\n".join(js), css))

# ---------- Captions: 1-3 words, mid-frame, each word appears on its onset ----------
body, js = [], []
for i, g in enumerate(plan["captions"]):
    gid = f"cap{i}"
    spans = []
    for j, (t, wt, style) in enumerate(g["words"]):
        spans.append(f'<span class="w {style}" id="{gid}-w{j}">{html.escape(t)}</span>')
        if j > 0:   # first word arrives with the group itself
            js.append(f'    tl.fromTo("#{gid}-w{j}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.04 }}, {f3(wt - 0.03)});')
    st, en = g["start"], g["end"]
    top = f' style="top:{g["top"]}px"' if "top" in g else ""
    body.append(f'    <div id="{gid}" class="clip cap"{top} data-start="{f3(st)}" data-duration="{f3(en - st)}" data-track-index="0">{" ".join(spans)}</div>')
    js.append(f'    tl.fromTo("#{gid}", {{ opacity: 0, filter: "blur(6px)" }}, {{ opacity: 1, filter: "blur(0px)", duration: 0.1, ease: "power3.out" }}, {f3(st)});')
css = f""".cap {{ position: absolute; left: 0; width: 1080px; top: {plan.get("cap_top", 940)}px; text-align: center; white-space: nowrap;
      font-family: "Inter Display HF"; font-weight: 700; font-size: 76px; letter-spacing: -0.05em; color: var(--ink);
      text-shadow: 0 2px 4px rgba(0,0,0,0.25), 0 6px 28px rgba(0,0,0,0.45); }}
    .cap .em {{ font-family: "Instrument Serif HF"; font-style: italic; font-weight: 400; font-size: 104px; letter-spacing: -0.02em; color: var(--accent);
      text-shadow: 0 2px 4px rgba(0,0,0,0.25), 0 4px 20px rgba(0,0,0,0.3); }}
    .cap .emw {{ font-family: "Instrument Serif HF"; font-style: italic; font-weight: 400; font-size: 104px; letter-spacing: -0.02em; color: var(--ink); }}"""
open(f"{P}/compositions/captions.html", "w").write(scene("captions", 4, "\n".join(body), "\n".join(js), css))

# ---------- Root ----------
def host(cid, kind, lane):
    return f'      <div id="{cid}" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html" data-start="0" data-duration="{f3(DUR)}" data-track-index="{lane}" data-track-kind="{kind}" data-width="{W}" data-height="{H}"></div>'
audio = [f'      <audio id="voice" class="clip" src="assets/audio/voice.wav" data-start="0" data-duration="{f3(DUR)}" data-track-index="10" data-volume="1"></audio>']
m = plan["music"]
audio.append(f'      <audio id="music" class="clip" src="assets/audio/{m["file"]}" data-start="0" data-duration="{f3(DUR)}" data-media-start="{m.get("offset", 0)}" data-track-index="11" data-volume="{m["vol"]}" data-fade-in="0.3" data-fade-out="0.8"></audio>')
import subprocess
def adur(f): return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f"{P}/assets/audio/{f}"],capture_output=True,text=True).stdout)
for i, (f, t, v) in enumerate(plan["sfx"]):
    audio.append(f'      <audio id="sfx{i}" class="clip" src="assets/audio/{f}" data-start="{f3(t)}" data-duration="{f3(min(adur(f), DUR - t))}" data-track-index="12" data-volume="{v}"></audio>')
root = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: {W}px; height: {H}px; overflow: hidden; background: #000; }}
      #root {{ position: relative; width: 100%; height: 100%; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{f3(DUR)}" data-width="{W}" data-height="{H}">
{host("aroll", "graphics", 0)}
{host("broll", "graphics", 1)}
{host("cards", "graphics", 2)}
{host("captions", "captions", 3)}
{chr(10).join(audio)}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""
open(f"{P}/index.html", "w").write(root)
print("wrote", P)
