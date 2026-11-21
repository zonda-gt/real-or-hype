# Version A "Shanghai's Avengers HQ": walkthrough. 2x2 collage hook, medium pace, handwritten labels.
import sys; sys.path.insert(0,'/home/user/real-or-hype/work/avengers-ggw'); from common import *
CAPTION_FIX={k:v for k,v in CAPTION_FIX.items() if k not in ('set','up')}
MUSIC='/home/user/real-or-hype/work/avengers-ggw/A/music.wav'
COLLAGE=[(C,11.0,3.0,0.5),(R,3.2,2.5,0.5),(P,5.4,2.4,0.5),(Q,8.2,2.0,0.5)]
CUES=[
 (9,[(K,1.0,1.3,0.6)]),                       # This is Grand Gateway
 (14,[(N,0.05,1.45,0.5)]),                    # in Xujiahui
 (15,[(C,28.0,1.9,0.5),(N,1.7,1.3,0.5)]),     # a giant Avengers logo across the towers
 (22,[(R,8.0,1.0,0.5),(Q,3.3,1.2,0.5)]),                      # Doctor Doom, guarding the front door
 (28,[(P,5.4,0.9,0.5)]),                      # and Thor's hammer
 (31,[(N,10.2,1.0,0.5)]),                     # stuck in the ground
 (35,[(C,23.5,1.6,0.5)]),                     # glowing at night
 (38,[(P,16.6,1.6,0.5)]),                     # A countdown clock
 (44,[(L,22.0,1.35,0.5)]),                    # Avengers: Doomsday
 (46,[(Q,10.6,1.4,0.5)]),                     # It's free
 (48,[(N,5.6,1.1,0.55),(C,11.2,1.2,0.5),(K,4.5,2.0,0.6)]),    # only here until December sixth
]
TITLE=["SHANGHAI'S","Avengers HQ"]; TAG="it's real"
LABELS=[("Grand Gateway 66",9),("Doctor Doom",22),("Thor's hammer",28)]
CARDS=[("free entry, until","Dec 6","2026",48,54)]
CTA=None
