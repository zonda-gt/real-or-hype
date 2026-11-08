"""Version B v3: ¥500 (Zhongnan Haibin, Pearl Tower in the window) vs ¥8,979 (Bulgari Bund-view room)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shots import S, part
from common import *
import gfx

S1 = 0.0
S2 = S1 + 0.12 + vo_dur('B1') + 0.2
S3 = S2 + 0.12 + vo_dur('B2') + 0.2
S4 = S3 + 0.12 + vo_dur('B3') + 0.2
S5 = S4 + 0.12 + vo_dur('B4') + 0.15
END = S5 + 0.1 + vo_dur('CTA') + 0.6
b1 = lambda i: word_t('B1', S1 + 0.12, i); b2 = lambda i: word_t('B2', S2 + 0.12, i)
b3 = lambda i: word_t('B3', S3 + 0.12, i); b4 = lambda i: word_t('B4', S4 + 0.12, i)

BEATS = (
    split(S2 - S1, [S['bg_pano']], [S['zn_bedview'], S['zn_room'], S['zn_window'], S['zn_skyline']])
    + seq(S3 - S2, [S['zn_bed'], S['zn_lounge'], S['zn_window'], S['zn_river'], S['zn_skyline'], S['zn_day'], S['zn_room'], S['zn_bedview']])
    + seq(S4 - S3, [part('bg_bed', 0, b3(8) - 0.1 - S3), S['bg_closet'], S['bg_sinks'], S['bg_tub']])
    + split(S5 - S4, [part('bg_pano', 1.0)], [S['zn_window'], S['zn_bundnight'], S['zn_bridge'], S['zn_twin'], S['zn_lounge']])
    + split(END - S5, [S['bg_bed'], S['bg_tub']], [S['zn_day'], S['zn_twin'], S['zn_lounge'], S['zn_bed']])
)
assert abs(sum(b['dur'] for b in BEATS) - END) < 0.02

VO = [('B1', S1 + 0.12), ('B2', S2 + 0.12), ('B3', S3 + 0.12), ('B4', S4 + 0.12), ('CTA', S5 + 0.1)]
TOPS = (48, 956 - 280); BOTS = (48, 1000)
LBL = lambda en, zh, t0, t1: (gfx.label([en, zh], 540, 150, anchor='c'), t0, t1, 'fade')
STAMP = (48, 330)
OVERLAYS = [
    (gfx.price_stamp('¥8,979', '1,340', *TOPS, note='booking app, May 2026'), b1(0), S2, 'pop'),
    (gfx.price_stamp('¥500', '75', *BOTS, note='package deal, 2025'), b1(11), S2, 'pop'),
    LBL('Hotel by Waibaidu Bridge', '上海外滩中南海滨酒店', S2, S3),
    (gfx.price_stamp('¥500', '75', *STAMP, note='package deal, 2025'), b2(0), S3, 'pop'),
    LBL('Bulgari Hotel Shanghai', '上海宝格丽酒店 · 外滩景观房', S3, S4),
    (gfx.price_stamp('¥8,979', '1,340', *STAMP, note='booking app, May 2026'), b3(0), S4, 'pop'),
    (gfx.price_stamp('¥8,979', '1,340', *TOPS, note='booking app, May 2026'), S4, S5 + 0.05, None),
    (gfx.price_stamp('¥500', '75', *BOTS, note='package deal, 2025'), S4, END, None),
    (gfx.pick_badge('OUR PICK', 860, 1000), b4(3), END, 'pop'),
    (gfx.cta(700), S5 + 0.05, END, 'fade'),
]
SFX = [(SFX + 'pop_es.wav', b1(0) - 0.03, -12), (SFX + 'pop_es.wav', b1(11) - 0.03, -12)] + \
      [(SFX + 'whoosh_es.wav', t - 0.3, -16) for t in (S2, S3, S4)] + [(SFX + 'real_es.wav', b4(3) - 0.3, -12)]


def caption_overlays(cap_y):
    return make_captions(BEATS, VO, cap_y)
