"""Named shot windows (source seconds, inside detected cut points). Verified clean per shot by check_spec.py."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'bin'))
from common import ZN, FH1, FH2, TOWER, BULGARI
S = dict(
    zn_bed=(ZN, 0.3, 1.13), zn_window=(ZN, 1.43, 2.8), zn_bridge=(ZN, 3.17, 4.27), zn_room=(ZN, 7.33, 8.4),
    zn_bedview=(ZN, 8.77, 9.83), zn_skyline=(ZN, 11.57, 12.23), zn_twin=(ZN, 12.63, 13.83), zn_lounge=(ZN, 15.53, 16.6),
    zn_river=(ZN, 16.93, 17.6), zn_bundnight=(ZN, 17.93, 18.93), zn_pearlnight=(ZN, 19.43, 21.73),
    zn_day=(ZN, 30.87, 31.73), zn_creek=(ZN, 33.23, 34.2),
    fh_woman=(FH1, 0.2, 7.8), fh_wide=(FH1, 15.53, 18.2), fh_lounge=(FH1, 21.53, 23.4), fh_tub=(FH1, 33.63, 34.83),
    fh_bed=(FH1, 36.63, 37.6), fh_room=(FH1, 37.93, 38.97),
    fh_golden=(FH2, 0.37, 2.6), fh_winperson=(FH2, 5.07, 6.13), fh_winwide=(FH2, 6.43, 7.7), fh_bedroom=(FH2, 8.03, 9.1),
    fh_skyline=(FH2, 12.63, 13.13), fh_nightsky=(FH2, 36.17, 37.33), fh_nightroom=(FH2, 37.67, 40.93),
    tw_pod=(TOWER, 2.87, 4.93), tw_lounge=(TOWER, 5.23, 8.13), tw_night=(TOWER, 34.43, 36.83),
    bg_closet=(BULGARI, 8.7, 9.77), bg_bed=(BULGARI, 19.1, 21.8), bg_pano=(BULGARI, 25.73, 32.5), bg_sinks=(BULGARI, 36.1, 38.27),
    bg_tub=(BULGARI, 48.97, 51.27),
)
# per-shot framing overrides for the split layout
SPLIT_CROP = {'zn_bridge': (0, 494, 1080, 956)}
for _k, _y in SPLIT_CROP.items():
    S[_k] = S[_k] + ({'crop_split': _y},)


def part(name, a=None, b=None):
    c, t0, t1 = S[name][:3]
    return (c, t0 if a is None else t0 + a, t1 if b is None else min(t1, t0 + b))
