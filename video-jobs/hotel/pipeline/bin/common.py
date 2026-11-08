"""Shared helpers for version specs."""
import json, os, re
B = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
import gfx

SFX = '/home/user/real-or-hype/.claude/skills/real-or-hype-video/sfx/'

# clip ids
TOWER = '7000007563282550024'      # 酒店控戴瑞克, 东方明珠230空中酒店 (2021-08-24)
RANRAN = '7603339338990692593'     # 然然的生活, 沪上·繁花酒店 (2026-02-05) price 700多
TONY = '7684330220115230050'       # Tony哥游天下, 沪上·繁花酒店 (2026-09-11)
MODU = '7648454699163239076'       # 魔都小姐姐, 沪上·繁花酒店 (2026-06-07)
TANG = '7664910852572069809'       # 小唐嫣, 沪上·繁花酒店 suite (2026-07-21)
HOSTEL = '7626378449230384714'     # 牙牙游, 壹号国际青旅(外滩豫园地铁站店) (2026-04-08)
BULGARI = '7642685720855086065'    # Daisy, 上海宝格丽酒店 (2026-05-22) booking card ¥8979
YAZHI = '7672345128757719034'      # 玖缘, 上海外滩雅致酒店 (2026-08-10) 500多/3天2晚


def vo_dur(k):
    return json.load(open(f'{B}/vo/p/{k}.json'))['dur']


def vo_words(k):
    return json.load(open(f'{B}/vo/p/{k}.json'))['words']


def word_t(k, t0, idx):
    """absolute start time of word idx of line k placed at t0"""
    return t0 + vo_words(k)[idx][1]


def layout_at(beats, t):
    acc = 0
    for b in beats:
        if t < acc + b['dur']:
            return b['layout']
        acc += b['dur']
    return beats[-1]['layout']


def make_captions(beats, vo, cap_y, skip=()):
    """word-by-word captions: chunks of <=3 words, break after punctuation; active word yellow."""
    ovs = []
    for key, t0 in vo:
        if key in skip:
            continue
        ws = vo_words(key)
        chunks = []; cur = []
        for w in ws:
            cur.append(w)
            if len(cur) == 3 or re.search(r'[.,?!:;]$', w[0]):
                chunks.append(cur); cur = []
        if cur: chunks.append(cur)
        for ci, ch in enumerate(chunks):
            end_chunk = chunks[ci + 1][0][1] if ci + 1 < len(chunks) else ch[-1][2] + 0.25
            words = [w[0] for w in ch]
            disp = [re.sub(r'[,;:]$', '', w) for w in words]
            for wi, w in enumerate(ch):
                s = t0 + w[1] - 2 / 30
                e = t0 + (ch[wi + 1][1] if wi + 1 < len(ch) else end_chunk) - 2 / 30
                y = cap_y[layout_at(beats, t0 + ch[0][1])]
                ovs.append((gfx.caption(disp, wi, y), s, e, None))
    return ovs


# ---------- v3 helpers: build beats from ordered shot windows ----------
ZN = '7443092546265353507'   # 优贤妈妈, 上海外滩中南海滨酒店 (2024-11-30)
FH1 = '7622343845196904357'  # 幼儿园抢饭王, 沪上·繁花酒店 (2026-03-28)
FH2 = '7649915486902681963'  # 少东, 沪上·繁花酒店 (2026-06-10)

# crops per (clip, layout): all above burned-in subtitle bands (checked again per shot by check_spec.py)
CROPS = {
    (ZN, 'full'): (132, 0, 816, 1450), (ZN, 'split2'): (0, 300, 1080, 956),
    (FH1, 'full'): (0, 0, 1080, 1920), (FH1, 'split2'): (0, 420, 1080, 956),
    (FH2, 'tall'): (584, 0, 752, 940), (FH2, 'split2'): (429, 0, 1062, 940),
    (TOWER, 'tall'): (584, 0, 752, 940), (TOWER, 'split2'): (429, 0, 1062, 940),
    (BULGARI, 'tall'): (528, 0, 864, 1080), (BULGARI, 'split2'): (350, 0, 1220, 1080),
}


def _layout_for(clip, pref):
    if (clip, pref) in CROPS: return pref
    return 'tall' if (clip, 'tall') in CROPS else 'full'


def _plan(dur, shots):
    """shots: list of (clip, t0, t1[, opts]). -> list of (shot_dict_partial, d) covering dur exactly."""
    total = sum(s[2] - s[1] for s in shots)
    speed = 1.0 if total >= dur else total / dur
    if speed < 0.74: raise SystemExit(f'not enough footage: {total:.2f}s for {dur:.2f}s')
    out = []; left = dur
    for s in shots:
        if left <= 1e-6: break
        avail = (s[2] - s[1]) / speed
        d = min(avail, left)
        opts = s[3] if len(s) > 3 else {}
        out.append((dict(clip=s[0], t=s[1], speed=round(speed, 3), **opts), d)); left -= d
    if left > 1e-3: raise SystemExit('plan underfilled')
    return out


def seq(dur, shots, layout='full'):
    """single-window section: full-bleed (vertical sources) or tall (landscape sources)."""
    beats = []
    for sh, d in _plan(dur, shots):
        lay = _layout_for(sh['clip'], layout)
        sh.pop('crop_split', None); sh.setdefault('zoom', (1.0, 1.04)); sh['crop'] = sh.get('crop', CROPS[(sh['clip'], lay)])
        beats.append(dict(layout=lay, dur=d, shots=[sh]))
    return beats


def _snap(pb, pt, dur, tol=0.45):
    """move bottom cut points onto nearby top cut points (no sub-0.45 s beats), unless that would slow a shot below 0.8x"""
    tb = []; acc = 0
    for _, d in pt: acc += d; tb.append(acc)
    bb = []; acc = 0
    for _, d in pb: acc += d; bb.append(acc)
    nb = list(bb)
    for k, b0 in enumerate(bb[:-1]):
        near = min(tb, key=lambda t: abs(t - b0))
        lo = (nb[k - 1] if k > 0 else 0.0) + 0.5; hi = bb[k + 1] - 0.5
        if abs(near - b0) < tol and lo <= near <= hi and near < dur - 1e-6: nb[k] = near
    def speeds(nb):
        out = []; prev = 0.0
        for (sh, d), b in zip(pb, nb):
            nd = b - prev; used = d * sh['speed']
            out.append(min(sh['speed'], used / nd) if nd > d else sh['speed']); prev = b
        return out
    for _ in range(2 * len(nb)):
        sp = speeds(nb); bad = [k for k, v in enumerate(sp) if v < 0.8]
        if not bad: break
        k = bad[0]
        if k > 0: nb[k - 1] = bb[k - 1]
        if k < len(nb) - 1: nb[k] = bb[k]
    out = []; prev = 0.0
    for (sh, d), b, v in zip(pb, nb, speeds(nb)):
        s2 = dict(sh); s2['speed'] = round(v, 3)
        if v < 0.74: raise SystemExit('snap would slow a shot too much')
        out.append((s2, b - prev)); prev = b
    return out


def split(dur, top, bottom):
    """two full-bleed halves; independent cut points merged into shared beats."""
    pt, pb = _plan(dur, top), _plan(dur, bottom)
    pb = _snap(pb, pt, dur)
    def bounds(p):
        acc, b = 0, []
        for _, d in p: acc += d; b.append(acc)
        return b
    cuts = sorted(set([round(x, 4) for x in bounds(pt) + bounds(pb)]))
    beats = []; prev = 0.0
    def at(p, t):
        acc = 0.0
        for sh, d in p:
            if t < acc + d - 1e-3:
                s = dict(sh); s['t'] = round(sh['t'] + (t - acc) * sh['speed'], 3); return s
            acc += d
        s = dict(p[-1][0]); return s
    for c in cuts:
        if c - prev < 1e-4: continue
        shs = []
        for p in (pt, pb):
            s = at(p, prev); cs = s.pop('crop_split', None); s['crop'] = cs or s.get('crop') or CROPS[(s['clip'], 'split2')]
            s.setdefault('zoom', (1.0, 1.03)); shs.append(s)
        beats.append(dict(layout='split2', dur=c - prev, shots=shs)); prev = c
    return beats
