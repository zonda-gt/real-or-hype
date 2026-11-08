"""Classify every OCR detection in a final render: OURS (inside an active overlay of ours), IN-SCENE (same text box also
found in the footage-only render), or UNEXPLAINED. usage: verify_final.py spec.py final_ocr.json clean_ocr.json out.json"""
import sys, os, json, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render
spec = render.load_spec(sys.argv[1]); fin = json.load(open(sys.argv[2])); cln = json.load(open(sys.argv[3]))
ovs = render.prep_overlays(spec.OVERLAYS + spec.caption_overlays(render.CAP_Y))
FPS = 30
def inter(a, b):
    return max(0, min(a[2], b[2]) - max(a[0], b[0])) * max(0, min(a[3], b[3]) - max(a[1], b[1]))
res = {'ours': 0, 'in_scene': 0, 'unexplained': []}; frames_with_text = 0
for i, boxes in enumerate(fin['frames']):
    t = i / FPS
    if boxes: frames_with_text += 1
    for b in boxes:
        bb = b[:4]; area = max(1, (bb[2] - bb[0]) * (bb[3] - bb[1]))
        act = [o['box'] for o in ovs if o['t0'] - 0.1 <= t < o['t1'] + 0.1]
        if any(inter(bb, ob) / area > 0.5 for ob in act):
            res['ours'] += 1; continue
        cb = [c[:4] for j in range(max(0, i - 10), min(len(cln['frames']), i + 11)) for c in cln['frames'][j]]
        if any(inter(bb, c) / area > 0.3 for c in cb):
            res['in_scene'] += 1; continue
        res['unexplained'].append([round(t, 2)] + b)
res['frames'] = len(fin['frames']); res['frames_with_text'] = frames_with_text
json.dump(res, open(sys.argv[4], 'w'), ensure_ascii=False, indent=0)
print(f"{sys.argv[2]}: {res['frames']} frames, {res['ours']} detections inside our overlays, {res['in_scene']} in-scene (also in footage-only render), {len(res['unexplained'])} UNEXPLAINED")
for u in res['unexplained'][:40]: print('  ', u)
