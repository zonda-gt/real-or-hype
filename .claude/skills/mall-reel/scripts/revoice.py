# Re-time a finished edit to a new narration (new voice, or a changed ending) without re-editing by hand.
# Every time in the old edl (shot cuts, labels, pills, title end, follow start) is re-anchored to the same word in the new
# Every time in the old edl (shot cuts, labels, pills, title end, CTA start) is re-anchored to the same word in the new
# words.json, keeping its offset from that word's onset; changed words (new CTA, new price) map proportionally. END = last word end + 0.6 s.
# usage (from the NEW project dir): python3 -I <skill>/scripts/revoice.py <old_project_dir>   -> writes ./edl.py
import sys, os, json, importlib.util, difflib, re, pprint
old = sys.argv[1]
spec = importlib.util.spec_from_file_location('old_edl', os.path.join(old, 'edl.py')); E = importlib.util.module_from_spec(spec); spec.loader.exec_module(E)
OW = json.load(open(os.path.join(old, 'vo/words.json'))); NW = json.load(open('vo/words.json'))
norm = lambda w: re.sub(r'[^a-z0-9一-鿿]', '', w.lower())
sm = difflib.SequenceMatcher(None, [norm(w[0]) for w in OW], [norm(w[0]) for w in NW], autojunk=False)
# old word index -> new word index; changed words (replace/delete/insert blocks) map proportionally inside their block
m = {}
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    for i in range(i1, i2):
        m[i] = j1 + (i - i1) if tag == 'equal' else min(j2 - 1, j1 + (i - i1) * max(1, j2 - j1) // max(1, i2 - i1)) if j2 > j1 else max(0, j1 - 1)
changed = [OW[i][0] for t, i1, i2, j1, j2 in sm.get_opcodes() if t != 'equal' for i in range(i1, i2)]
def t_new(t):
    i = max([k for k, w in enumerate(OW) if w[1] <= t + 0.02] or [0])   # the old word this time belongs to
    return round(NW[m[i]][1] + (t - OW[i][1]), 3)
EDL = [tuple([t_new(e[0])] + list(e[1:])) for e in E.EDL]
EDL[0] = tuple([0.0] + list(EDL[0][1:]))
LABELS = [(t_new(a), t_new(b), *r) for a, b, *r in E.LABELS]
PILLS = [(t_new(a), t_new(b), *r) for a, b, *r in E.PILLS]
T = E.TITLE; TITLE = (*T[:3], T[3], t_new(T[4]))
FOLLOW = (t_new(E.FOLLOW[0]), E.FOLLOW[1])
END = round(NW[-1][2] + 0.6, 2)
src = open(os.path.join(old, 'edl.py')).read()
shots_fn = src[src.index('def shots'):]
with open('edl.py', 'w') as f:
    f.write(f'# Re-timed from {old} by revoice.py for a new narration.\n')
    for name, val in [('END', END), ('EDL', EDL), ('TITLE', TITLE), ('LABELS', LABELS), ('PILLS', PILLS), ('FOLLOW', FOLLOW),
                      ('MUSIC', E.MUSIC), ('CAPTION_REPLACE', getattr(E, 'CAPTION_REPLACE', {}))]:
        f.write(f'{name} = {pprint.pformat(val, width=140)}\n')
    f.write(getattr(E, 'FOLLOW_TEXT', None) and f"FOLLOW_TEXT = {E.FOLLOW_TEXT!r}\n" or '')
    f.write('\n' + shots_fn)
print('wrote edl.py; END', END, '| changed old words:', changed)
