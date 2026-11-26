# hiccups.py <src.wav> <cuts.json>
# Finds stutters, false starts, repeated words and fillers inside every kept segment, and proposes a cut point for each.
#  1. verbatim Whisper: an initial prompt full of disfluencies stops Whisper "cleaning" the speech, so "pl- planning" and "we we" are heard
#  2. flags: a word ending in "-", a word that is a prefix of the next ("Plan" -> "planning"), the same word twice in a row,
#     fillers (uh, um, er, ah, hmm), and words the script line does not contain
#  3. cut point = the quietest 5 ms frame between the end of the hiccup and the onset of the word that replaces it
#     (energy on 120 Hz-6 kHz band); reported with its level above the noise floor, so a tight dip is visible
import sys, json, re, subprocess, numpy as np
from faster_whisper import WhisperModel
src, cf = sys.argv[1:3]
m = WhisperModel("medium", device="cpu", compute_type="int8")
PROMPT = "Umm, so, I- I- I was, uh, like, pl- planning, we- we will, you know, the- the thing. Uh, so, yeah."
FILL = {"uh", "um", "umm", "er", "ah", "hmm", "erm"}
x = np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',src,'-ac','1','-ar','16000','-af','highpass=f=120,lowpass=f=6000','-f','f32le','-'],capture_output=True).stdout, np.float32)
H = 80   # 5 ms
env = 20*np.log10(np.array([np.sqrt(np.mean(x[i:i+H]**2))+1e-9 for i in range(0, len(x)-H, H)]))
floor = np.percentile(env, 10)
norm = lambda w: re.sub(r"[^a-z']", "", w.lower())
def dip(a, b):
    i0, i1 = int(a*200), int(b*200)
    if i1 <= i0: return a, 99
    k = i0 + int(np.argmin(env[i0:i1])); return k/200, env[k]-floor
out = []
for k, a0, a1, text in json.load(open(cf)):
    seg = x[int(a0*16000):int(a1*16000)]
    ws = [(a0+w.start, a0+w.end, w.word.strip()) for s in m.transcribe(seg, language='en', beam_size=5, word_timestamps=True,
          initial_prompt=PROMPT, condition_on_previous_text=False)[0] for w in s.words]
    ws = [w for w in ws if norm(w[2]) or w[2].endswith('-')]
    script = [norm(w) for w in text.split()]
    print(f"[{k}] {a0:.2f}-{a1:.2f} heard: " + ' '.join(w for _,_,w in ws))
    for i, (s, e, w) in enumerate(ws):
        n = norm(w); nxt = ws[i+1] if i+1 < len(ws) else None
        why = None
        if w.endswith('-') or (nxt and nxt[2] == '-'): why = 'cut-off word'
        elif nxt and n and norm(nxt[2]) == n: why = 'repeated word'
        elif nxt and n and len(n) >= 2 and norm(nxt[2]).startswith(n) and norm(nxt[2]) != n: why = 'false start'
        elif n in FILL: why = 'filler'
        elif n and n not in script: why = 'not in script'
        if why:
            # what replaces it: the next real word
            j = i+1
            while j < len(ws) and not norm(ws[j][2]): j += 1
            if j < len(ws):
                t, lvl = dip(e - 0.06, ws[j][0] + 0.10)
                print(f"   HICCUP {why}: '{w}' {s:.2f}-{e:.2f} -> next '{ws[j][2]}' @{ws[j][0]:.2f}; quietest point {t:.3f}s at floor+{lvl:.1f} dB")
                out.append({"seg": k, "why": why, "word": w, "start": s, "end": e, "next": ws[j][2], "cut": round(t, 3), "dip_db": round(float(lvl), 1)})
json.dump(out, open(cf.replace('.json', '_hiccups.json'), 'w'), indent=1)
print(len(out), "hiccups")
