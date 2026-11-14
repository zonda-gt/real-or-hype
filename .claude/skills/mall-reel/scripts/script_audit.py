# Density audit for a mall-reel script. Run BEFORE generating the voice (on script.txt) and again after tightening
# (with vo/words.json present it also prints seconds per sentence).
# usage (from project dir): python3 -I <skill>/scripts/script_audit.py [script.txt]
# Fails (exit 1) when: a content word repeats 3+ times, a filler phrase appears, or a sentence has no fact
# (no name, number, place, price, time or how-to). Every sentence must tell the viewer something new.
import re, sys, json, os
txt = re.sub(r'\[.*?\]', '', open(sys.argv[1] if len(sys.argv) > 1 else 'script.txt').read()).strip()
sents = [s.strip() for s in re.split(r'(?<=[.!?])\s+', txt) if s.strip()]
SOFT = ['super ', 'really ', 'actually', 'basically', 'just ']          # intensifiers: warning only
FILLER = ['one of the coolest', 'the whole place', 'make a whole evening',
          "here's the thing", 'you won\'t believe', 'trust me', 'must-visit', 'hidden gem', 'vibes', 'so cool', 'amazing',
          'at almost every', 'everywhere', 'lots of', 'a lot of', 'all kinds of', 'full of indie shops', 'shops and cafés']
STOP = set('the a an and or but so to of in on at for with it its it\'s is are was were be this that there there\'s here you your '
           'we i my me they their them from by as just now then up out over into about after before more most very can'.split())
ok = True
words = re.findall(r"[a-z0-9'一-鿿]+", txt.lower())
counts = {}
for w in words:
    if w not in STOP and len(w) > 2: counts[w] = counts.get(w, 0) + 1
rep = {w: c for w, c in counts.items() if c >= 3 and w not in ('shanghai',)}
if rep: ok = False; print('REPEATED (say each thing once):', rep)
fil = [f for f in FILLER if f in txt.lower()]
if fil: print('FILLER phrases (cut, or replace with a fact):', fil)
soft = [f.strip() for f in SOFT if f in txt.lower()]
if soft: print('warning, intensifiers (keep only if they help the rhythm):', soft)
times = None
if os.path.exists('vo/words.json'):
    W = json.load(open('vo/words.json')); times = []; k = 0
    for s in sents:
        n = len(re.findall(r"\S+", s)); seg = W[k:k + n]; k += n
        times.append((seg[0][1], seg[-1][2]) if seg else (0, 0))
fact = re.compile(r"\d|¥|yuan|line \d|exit|metro|free|dog-friendly|pet-friendly|book|open|[一-鿿]|\b[A-Z][a-z]+(?: [A-Z][a-z]+)*\b")
print()
for i, s in enumerate(sents):
    body = s[1:] if s else s   # ignore the capital at the sentence start
    has = bool(fact.search(body)) or i == len(sents) - 1   # last line = follow
    t = f'{times[i][0]:5.1f}-{times[i][1]:5.1f}s ' if times else ''
    print(f"{'  ' if has else '??'} {t}{s}")
    if not has: ok = False
print('\n?? = no name/number/price/how-to: what new fact does this sentence add? Cut it or give it one.')
print(f'{len(words)} words, {len(sents)} sentences', '| AUDIT PASS' if ok and not fil else '| AUDIT FAIL')
sys.exit(0 if ok and not fil else 1)
