"""Version A v3: same tower, three budgets — Zhongnan Haibin ~¥500 / Fanhua ¥1,000+ / Pearl Tower suite ¥68,000."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shots import S, part
from common import *
import gfx

S1 = 0.0
S2 = S1 + 0.12 + vo_dur('A1') + 0.15
S3 = S2 + 0.12 + vo_dur('A2') + 0.2
S4 = S3 + 0.12 + vo_dur('A3') + 0.2
S5 = S4 + 0.12 + vo_dur('A4') + 0.2
S6 = S5 + 0.12 + vo_dur('A5') + 0.15
END = S6 + 0.1 + vo_dur('CTA') + 0.6
a1 = lambda i: word_t('A1', S1 + 0.12, i); a2 = lambda i: word_t('A2', S2 + 0.12, i)
a3 = lambda i: word_t('A3', S3 + 0.12, i); a4 = lambda i: word_t('A4', S4 + 0.12, i); a5 = lambda i: word_t('A5', S5 + 0.12, i)

hook_cut = a1(9) - 0.1   # bottom switches to the window+tower on "see"
BEATS = (
    split(S2 - S1, [S['tw_pod'], S['tw_night']],
          [S['zn_bedview'], S['zn_bridge'], S['zn_window'], S['zn_skyline']])
    + seq(S3 - S2, [S['zn_room'], S['zn_lounge'], S['zn_twin'], S['zn_river'], S['zn_skyline'], S['zn_bed'], S['zn_day']])
    + seq(S4 - S3, [part('fh_woman', 0, 3.4), S['fh_wide'], S['fh_golden']])
    + seq(S5 - S4, [S['tw_pod'], S['tw_lounge'], S['tw_night']])
    + seq(S6 - S5, [S['zn_window'], S['zn_bundnight'], S['zn_skyline'], S['zn_day'], S['zn_river'], S['zn_bedview']])
    + seq(END - S6, [S['fh_nightroom'], S['fh_nightsky']])
)
assert abs(sum(b['dur'] for b in BEATS) - END) < 0.02

VO = [('A1', S1 + 0.12), ('A2', S2 + 0.12), ('A3', S3 + 0.12), ('A4', S4 + 0.12), ('A5', S5 + 0.12), ('CTA', S6 + 0.1)]
TOPS = (48, 956 - 280); BOTS = (48, 1000)
LBL = lambda en, zh, t0, t1: (gfx.label([en, zh], 540, 150, anchor='c'), t0, t1, 'fade')
STAMP = (48, 330)
OVERLAYS = [
    (gfx.price_stamp('¥68,000', '10,150', *TOPS, note='regular price'), a1(3), S2, 'pop'),
    (gfx.price_stamp('¥500', '75', *BOTS, note='package deal, 2025'), a1(9), S2, 'pop'),
    LBL('Hotel by Waibaidu Bridge', '上海外滩中南海滨酒店', S2, S3),
    (gfx.price_stamp('¥500', '75', *STAMP, note='package deal, 2025'), a2(0), S3, 'pop'),
    LBL('Fanhua Hotel · North Bund', '沪上·繁花酒店（北外滩滨江店）', S3, S4),
    (gfx.price_stamp('¥1,000+', '150', *STAMP, note='creator quote, Jun 2026'), a3(0), S4, 'pop'),
    LBL('Oriental Pearl Tower suite', '东方明珠230空中酒店 · 230 m up', S4, S5),
    (gfx.price_stamp('¥68,000', '10,150', *STAMP, note='regular price'), a4(0), S5, 'pop'),
    (gfx.price_stamp('¥500', '75', *STAMP, note='package deal, 2025'), S5, S6, None),
    (gfx.pick_badge('OUR PICK', 860, 340), a5(2), S6, 'pop'),
    (gfx.cta(760), S6 + 0.05, END, 'fade'),
]
SFX = [(SFX + 'pop_es.wav', a1(3) - 0.03, -12), (SFX + 'pop_es.wav', a1(9) - 0.03, -12)] + \
      [(SFX + 'whoosh_es.wav', t - 0.3, -16) for t in (S2, S3, S4, S5)] + \
      [(SFX + 'real_es.wav', a5(2) - 0.3, -12)]


def caption_overlays(cap_y):
    return make_captions(BEATS, VO, cap_y)
