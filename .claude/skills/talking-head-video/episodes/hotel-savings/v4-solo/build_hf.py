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
for si, s in enumerate(plan["aroll"]):
    # one-frame overlap into the next take: separately rounded start/duration left a 1-frame black gap (ep4 17.067 s)
    d = (plan["aroll"][si+1]["start"] - s["start"] + 0.034) if si+1 < len(plan["aroll"]) else s["dur"]
    body.append(f'      <video id="a-{s["k"]}" class="clip seg" src="assets/aroll/{s["k"]}.mp4" data-start="{f3(s["start"])}" data-duration="{f3(d)}" data-track-index="0" muted playsinline></video>')
body.append('    </div>')
if plan.get("logo"):   # brand mark on the wall above his head: outside the cam wrapper (stays put on punch-ins); B-roll and cards cover it
    body.append('    <img id="aroll-logo" class="logo" src="assets/logo.png" alt="ChinaPal Travel" />')
for s in plan["aroll"]:
    sc = s.get("scale", 1.0)
    if s.get("whip"):      # zoom-blur arrival, as the reference's cuts
        js.append(f'    tl.set("#aroll-cam", {{ scale: {sc*1.16:.3f}, filter: "blur(14px)" }}, {f3(s["start"])}); tl.to("#aroll-cam", {{ scale: {sc}, filter: "blur(0px)", duration: 0.22, ease: "expo.out" }}, {f3(s["start"]+0.001)});')  # set+to: seek-safe in both directions
    else:
        js.append(f'    tl.set("#aroll-cam", {{ scale: {sc}, filter: "blur(0px)" }}, {f3(s["start"])});')
css = """.cam { position: absolute; inset: 0; transform-origin: 50% 30%; }
    .logo { position: absolute; top: 150px; left: 375px; width: 330px; opacity: 0.88; }
    .seg { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }"""
open(f"{P}/compositions/aroll.html", "w").write(scene("aroll", 1, "\n".join(body), "\n".join(js), css))

# ---------- B-roll cutaways ----------
body, js = ['    <div id="broll-cam" class="cam">'], ['    tl.set("#broll-cam", { scale: 1, filter: "blur(0px)" }, 0);']
for b in plan["broll"]:
    body.append(f'      <video id="b-{b["id"]}" class="clip seg" src="assets/broll/{b["src"]}.mp4" data-start="{f3(b["start"])}" data-duration="{f3(b["dur"])}" data-track-index="0" muted playsinline></video>')
    js.append(f'    tl.set("#broll-cam", {{ scale: 1.2, filter: "blur(16px)" }}, {f3(b["start"])}); tl.to("#broll-cam", {{ scale: 1.0, filter: "blur(0px)", duration: 0.24, ease: "expo.out" }}, {f3(b["start"]+0.001)});')
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
                if ln.get("slam"):   # hero word: lands big and blurred, settles in 0.2 s, then dead still
                    spans.append(f'<span class="w slam" id="{cid}-w{j}">{html.escape(t)}</span>')
                    js.append(f'    tl.fromTo("#{cid}-w{j}", {{ opacity: 0, scale: 1.4, filter: "blur(14px)" }}, {{ opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.2, ease: "expo.out" }}, {f3(max(st, wt - 0.03))});')
                else:
                    spans.append(f'<span class="w" id="{cid}-w{j}">{html.escape(t)}</span>')
                    js.append(f'    tl.fromTo("#{cid}-w{j}", {{ opacity: 0, filter: "blur(10px)" }}, {{ opacity: 1, filter: "blur(0px)", duration: 0.13, ease: "power3.out" }}, {f3(max(st, wt - 0.03))});')
                j += 1
            lines.append(f'<div class="tl {ln["style"]}" style="font-size:{ln["size"]}px">{" ".join(spans)}</div>')
        body.append(f'    <div id="{cid}" class="clip title" data-start="{f3(st)}" data-duration="{f3(du)}" data-track-index="1" style="top:{c["top"]}px">{"".join(lines)}</div>')
        if not c.get("hold"):   # a closing title holds to the last frame
            js.append(f'    tl.to("#{cid}", {{ opacity: 0, filter: "blur(8px)", duration: 0.12, ease: "power2.in" }}, {f3(st + du - 0.12)});')
            js.append(f'    tl.set("#{cid}", {{ opacity: 1, filter: "blur(0px)" }}, {f3(st)});')
    elif c["kind"] == "pill":
        body.append(f'''    <div id="{cid}" class="clip pillwrap" data-start="{f3(st)}" data-duration="{f3(du)}" data-track-index="1" style="top:{c["top"]}px">
      <div class="pill" id="{cid}-pill"><span class="pill-text">&ldquo;{html.escape(c["text"])}&rdquo;</span>
        <span class="pill-send"><svg viewBox="0 0 24 24" width="40" height="40"><path d="M12 19V6M6 11.5 12 5.5l6 6" fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg></span></div>
    </div>''')
        js.append(f'    tl.fromTo("#{cid}-pill", {{ scale: 0.7, opacity: 0, y: 30 }}, {{ scale: 1, opacity: 1, y: 0, duration: 0.42, ease: "back.out(1.7)" }}, {f3(st)});')
    elif c["kind"] == "cta":
        # comment -> DM sequence: composer slides up, keyword types in, send tapped, the box becomes the posted
        # comment (heart pops), then the brand's DM notification drops in with the reward and holds to the end
        kw, t_type, t_send, t_dm = c["keyword"], c["t_type"], c["t_send"], c["t_dm"]
        AV = '<svg viewBox="0 0 40 40" width="76" height="76"><circle cx="20" cy="20" r="20" fill="#d9d4cc"/><circle cx="20" cy="15.5" r="7" fill="#a39d94"/><path d="M6.5 34c2.6-6.3 7.6-9 13.5-9s10.9 2.7 13.5 9" fill="#a39d94"/></svg>'
        ARROW = '<svg viewBox="0 0 24 24" width="40" height="40"><path d="M12 19V6M6 11.5 12 5.5l6 6" fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
        HEART = 'M12 21s-7.5-4.6-9.6-9.2C.9 8.4 2.9 4.5 6.6 4.5c2.2 0 3.8 1.3 5.4 3.2 1.6-1.9 3.2-3.2 5.4-3.2 3.7 0 5.7 3.9 4.2 7.3C19.5 16.4 12 21 12 21z'
        letters = "".join(f'<span class="ltr" id="{cid}-l{k}">{html.escape(ch)}</span>' for k, ch in enumerate(kw))
        body.append(f'''    <div id="{cid}" class="clip ctawrap" data-start="{f3(st)}" data-duration="{f3(du)}" data-track-index="1">
      <div class="dm" id="{cid}-dm"><img class="dm-av" src="assets/avatar.jpg" alt="" />
        <div class="dm-body"><div class="dm-top"><span class="dm-name">{html.escape(c["brand"])}</span><span class="dm-when">now</span></div>
        <div class="dm-msg">{html.escape(c["reward"])}</div></div></div>
      <div class="cbox" id="{cid}-box" style="top:{c["top"]}px">
        <div class="layer" id="{cid}-compose">{AV}<div class="field"><span class="ph" id="{cid}-ph">Add a comment&hellip;</span><span class="typed">{letters}</span><span class="caret" id="{cid}-caret"></span></div>
          <div class="send" id="{cid}-send">{ARROW}</div><div class="ring" id="{cid}-ring"></div></div>
        <div class="layer posted" id="{cid}-posted">{AV}<div class="pc"><div class="pc-top"><span class="pc-user">you</span><span class="pc-when">now</span></div><div class="pc-text">{html.escape(kw)}</div></div>
          <svg class="heart" viewBox="0 0 24 24" width="52" height="52"><path d="{HEART}" fill="none" stroke="#8e8e8e" stroke-width="1.8"/><path id="{cid}-hf" d="{HEART}" fill="#e0245e" style="transform-origin:12px 13px"/></svg></div>
      </div>
    </div>''')
        J = js.append
        J(f'    tl.set(["#{cid}-posted"], {{ opacity: 0 }}, 0); tl.set("#{cid}-hf", {{ scale: 0 }}, 0); tl.set("#{cid} .ltr", {{ display: "none" }}, 0);')
        J(f'    tl.fromTo("#{cid}-box", {{ y: 220, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.45, ease: "expo.out" }}, {f3(st)});')
        bt = st + 0.45   # caret blinks until typing starts
        while bt < t_type - 0.05:
            J(f'    tl.set("#{cid}-caret", {{ opacity: 0 }}, {f3(bt)}); tl.set("#{cid}-caret", {{ opacity: 1 }}, {f3(min(bt + 0.25, t_type))});'); bt += 0.5
        J(f'    tl.set("#{cid}-ph", {{ opacity: 0 }}, {f3(t_type)});')
        for k in range(len(kw)):
            J(f'    tl.set("#{cid}-l{k}", {{ display: "inline" }}, {f3(t_type + k * 0.075)});')
        J(f'    tl.fromTo("#{cid}-send", {{ scale: 1 }}, {{ scale: 0.8, duration: 0.08, ease: "power2.in" }}, {f3(t_send)});')
        J(f'    tl.to("#{cid}-send", {{ scale: 1, duration: 0.3, ease: "back.out(2.2)" }}, {f3(t_send + 0.08)});')
        J(f'    tl.fromTo("#{cid}-ring", {{ scale: 0.6, opacity: 0.55 }}, {{ scale: 2.0, opacity: 0, duration: 0.45, ease: "power2.out" }}, {f3(t_send + 0.04)});')
        J(f'    tl.to("#{cid}-compose", {{ opacity: 0, y: -16, duration: 0.18, ease: "power2.in" }}, {f3(t_send + 0.18)});')
        J(f'    tl.fromTo("#{cid}-posted", {{ opacity: 0, y: 22 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "expo.out" }}, {f3(t_send + 0.3)});')
        J(f'    tl.fromTo("#{cid}-hf", {{ scale: 0 }}, {{ scale: 1, duration: 0.4, ease: "back.out(3)" }}, {f3(t_send + 0.62)});')
        J(f'    tl.fromTo("#{cid}-dm", {{ y: -620, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.55, ease: "expo.out" }}, {f3(t_dm)});')
css = """.full { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; }
    .cream { background: var(--cream); color: var(--accent); }
    .navy { background: var(--navy); color: var(--ink); }
    .card-text { font-family: "Inter Display HF"; font-weight: 700; font-size: 104px; letter-spacing: -0.05em; text-align: center; padding: 0 120px; line-height: 1.0; }
    .title { position: absolute; left: 0; width: 1080px; text-align: center; }
    .tl { line-height: 0.88; white-space: nowrap; }
    .heavy { font-family: "Inter Display Heavy"; font-weight: 900; font-style: italic; color: var(--ink); letter-spacing: -0.045em; text-transform: uppercase; text-shadow: 0 6px 30px rgba(0,0,0,0.35); }
    .heavy-red { font-family: "Inter Display Heavy"; font-weight: 900; font-style: italic; color: #cb2329; letter-spacing: -0.045em; text-transform: uppercase; text-shadow: 0 6px 30px rgba(0,0,0,0.25); }
    .serif-red { font-family: "Playfair HF"; font-weight: 700; font-style: italic; color: #d4494f; letter-spacing: -0.03em; margin: -4px 0 18px; text-shadow: 0 0 2px rgba(255,255,255,0.35), 0 4px 18px rgba(0,0,0,0.25); }
    .pillwrap { position: absolute; left: 0; width: 1080px; display: flex; justify-content: center; }
    .pill { width: 760px; height: 116px; border-radius: 58px; background: #f7f3ee; display: flex; align-items: center; justify-content: space-between; padding: 0 18px 0 46px; box-shadow: 0 10px 40px rgba(0,0,0,0.35); }
    .pill-text { font-family: "Inter Display HF"; font-weight: 700; font-size: 50px; letter-spacing: -0.03em; color: #111; }
    .pill-send { width: 80px; height: 80px; border-radius: 40px; background: var(--accent); display: flex; align-items: center; justify-content: center; }
    .slam { display: inline-block; transform-origin: 50% 60%; }
    .small-ink { font-family: "Inter Display HF"; font-weight: 700; color: var(--ink); letter-spacing: -0.045em; text-shadow: 0 2px 4px rgba(0,0,0,0.25), 0 6px 28px rgba(0,0,0,0.45); }
    .ctawrap { position: absolute; inset: 0; }
    .cbox { position: absolute; left: 70px; width: 940px; height: 140px; }
    .layer { position: absolute; inset: 0; border-radius: 70px; background: #fff; display: flex; align-items: center; gap: 22px; padding: 0 22px 0 26px; box-shadow: 0 14px 44px rgba(0,0,0,0.35); }
    .field { flex: 1; position: relative; height: 100%; display: flex; align-items: center; font-family: "Inter Display HF"; font-weight: 700; font-size: 50px; color: #111; letter-spacing: -0.01em; }
    .ph { position: absolute; left: 0; color: #9a9a9a; font-weight: 600; letter-spacing: -0.02em; }
    .ltr { display: none; }
    .caret { width: 4px; height: 56px; background: #0095f6; margin-left: 4px; border-radius: 2px; }
    .send { position: relative; z-index: 2; width: 96px; height: 96px; border-radius: 48px; background: var(--accent); display: flex; align-items: center; justify-content: center; }
    .ring { position: absolute; right: 22px; top: 22px; width: 96px; height: 96px; border-radius: 48px; border: 5px solid var(--accent); opacity: 0; }
    .pc { flex: 1; font-family: "Inter Display HF"; }
    .pc-top { font-size: 32px; font-weight: 700; color: #111; }
    .pc-when { color: #8e8e8e; font-weight: 600; margin-left: 14px; }
    .pc-text { font-size: 50px; font-weight: 700; color: #111; letter-spacing: -0.01em; line-height: 1.05; }
    .heart { margin-right: 22px; overflow: visible; }
    .dm { position: absolute; top: 300px; left: 50px; width: 980px; border-radius: 46px; background: rgba(28,28,30,0.95); display: flex; align-items: center; gap: 26px; padding: 28px 36px; box-shadow: 0 18px 50px rgba(0,0,0,0.4); }
    .dm-av { width: 108px; height: 108px; border-radius: 54px; object-fit: cover; flex: none; }
    .dm-body { flex: 1; font-family: "Inter Display HF"; }
    .dm-top { display: flex; align-items: baseline; }
    .dm-name { font-size: 40px; font-weight: 700; color: #fff; letter-spacing: -0.02em; }
    .dm-when { margin-left: auto; font-size: 32px; font-weight: 600; color: #9b9b9b; }
    .dm-msg { margin-top: 6px; font-size: 40px; font-weight: 600; line-height: 1.2; color: #ececec; letter-spacing: -0.015em; }"""
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
