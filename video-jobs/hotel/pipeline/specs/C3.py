"""Version C v3: ¥68,000 (Pearl Tower suite) vs ¥1,000+ (Fanhua North Bund river view)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shots import S, part
from common import *
import gfx

S1 = 0.0
S2 = S1 + 0.12 + vo_dur('C1') + 0.15
S3 = S2 + 0.12 + vo_dur('C2') + 0.25
S4 = S3 + 0.12 + vo_dur('C3') + 0.25
S5 = S4 + 0.12 + vo_dur('C4') + 0.15
END = S5 + 0.1 + vo_dur('CTA') + 0.6
c1 = lambda i: word_t('C1', S1 + 0.12, i); c2 = lambda i: word_t('C2', S2 + 0.12, i)
c3 = lambda i: word_t('C3', S3 + 0.12, i); c4 = lambda i: word_t('C4', S4 + 0.12, i)

BEATS = (
    split(S2 - S1, [S['tw_pod'], S['tw_night'], S['tw_lounge']], [part('fh_woman', 0, 2.6), S['fh_golden']])
    + seq(S3 - S2, [part('fh_woman', 2.6, 3.8), S['fh_wide'], S['fh_lounge'], S['fh_winwide']])
    + seq(S4 - S3, [S['tw_pod'], S['tw_lounge'], S['tw_night']])
    + split(S5 - S4, [S['tw_lounge'], S['tw_night'], S['tw_pod']], [S['fh_winperson'], S['fh_lounge'], S['fh_bedroom'], S['fh_room'], S['fh_bed'], S['fh_winwide']])
    + seq(END - S5, [S['fh_nightroom'], S['fh_nightsky']])
)
assert abs(sum(b['dur'] for b in BEATS) - END) < 0.02

VO = [('C1', S1 + 0.12), ('C2', S2 + 0.12), ('C3', S3 + 0.12), ('C4', S4 + 0.12), ('CTA', S5 + 0.1)]
TOPS = (48, 956 - 280); BOTS = (48, 1000)
LBL = lambda en, zh, t0, t1: (gfx.label([en, zh], 540, 150, anchor='c'), t0, t1, 'fade')
STAMP = (48, 330)
OVERLAYS = [
    (gfx.price_stamp('¥68,000', '10,150', *TOPS, note='regular price'), c1(0), S2, 'pop'),
    (gfx.price_stamp('¥1,000+', '150', *BOTS, note='creator quote, Jun 2026'), c1(6), S2, 'pop'),
    LBL('Fanhua Hotel · North Bund', '沪上·繁花酒店（北外滩滨江店）', S2, S3),
    (gfx.price_stamp('¥1,000+', '150', *STAMP, note='creator quote, Jun 2026'), c2(0), S3, 'pop'),
    LBL('Oriental Pearl Tower suite', '东方明珠230空中酒店 · 230 m up', S3, S4),
    (gfx.price_stamp('¥68,000', '10,150', *STAMP, note='regular price'), c3(0), S4, 'pop'),
    (gfx.price_stamp('¥68,000', '10,150', *TOPS, note='regular price'), S4, S5, None),
    (gfx.price_stamp('¥1,000+', '150', *BOTS, note='creator quote, Jun 2026'), S4, S5, None),
    (gfx.pick_badge('OUR PICK', 860, 1000), c4(3), S5, 'pop'),
    (gfx.price_stamp('¥1,000+', '150', *STAMP, note='our pick'), S5, END, None),
    (gfx.cta(760), S5 + 0.05, END, 'fade'),
]
SFX = [(SFX + 'pop_es.wav', c1(0) - 0.03, -12), (SFX + 'pop_es.wav', c1(6) - 0.03, -12)] + \
      [(SFX + 'whoosh_es.wav', t - 0.3, -16) for t in (S2, S3, S4)] + [(SFX + 'real_es.wav', c4(3) - 0.3, -12)]


def caption_overlays(cap_y):
    return make_captions(BEATS, VO, cap_y)
