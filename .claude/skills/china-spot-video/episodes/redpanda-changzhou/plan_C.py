# Version C "4 things before you book": insider list. Hero hook (guest on the bed stroking a red panda), relaxed pace, numbered stickers.
import sys; sys.path.insert(0,'/home/user/real-or-hype/work/redpanda'); from common import *
HERO=(H,5.75,1.60,0.42)
COLLAGE=[]
CUES=[
 (13,[(H,19.15,1.20,0.5)]),                       # One: book the right room
 (18,[(R,2.20,1.55,0.35)]),                       # Not every room gets a visit
 (24,[(A9,33.35,1.1,0.5),(A9,20.42,1.25,0.5)]),   # so pick the capsule where red pandas come in
 (33,[(A9,41.65,1.15,0.35)]),                     # Two: it's short
 (36,[(Q,2.35,6.8,0.4)]),                         # A keeper brings the red panda in for a few minutes, and you can stroke its back
 (53,[(H,26.30,1.15,0.5),(R,32.22,1.0,0.6)]),     # Three: mornings are the best part
 (59,[(A9,53.10,1.85,0.5)]),                      # Red pandas roam the camp
 (64,[(H,7.40,1.3,0.5),(R,34.00,1.1,0.5)]),       # and you eat breakfast right next to them
 (72,[(H,65.65,1.2,0.5),(A9,29.55,2.2,0.5)]),     # Four: it's inside Yancheng Wild Animal World in Changzhou
 (81,[(G,62.20,1.45,0.5),(S,10.05,2.85,0.5)]),    # two days in the zoo and a safari drive
 (95,[(T,33.85,1.15,0.6),(T,35.02,0.85,0.6)]),    # Packages start around $120 (card)
 (99,[(G,6.45,1.95,0.4),(P,13.75,3.75,0.5)]),     # Comment the word red panda
]
TAIL=1.3
TITLE=["4 THINGS","before you book"]; TAG="China's red panda hotel"
LABELS=[("#1 the right room",13),("#2 a few minutes",33),("#3 mornings",53),("#4 2 days of zoo",72)]
CARDS=[("packages from","about $120","about ¥850 · tickets incl.",95,99)]
CTA=('Comment "REDPANDA"',99)
CAPTION_FIX={'1.':'One,','2.':'Two,','3.':'Three,','4.':'Four,'}
