# Version A "The skyline flight, start to finish": the experience in order. Collage hook, medium pace, handwritten labels.
import sys; sys.path.insert(0,'/home/user/real-or-hype/work/helicopter'); from common import *
COLLAGE=[(R,2.65,1.1,0.5),(N3,0.3,3.0,0.5),(Z,9.2,1.7,0.5),(NB,13.0,3.0,0.5)]
CUES=[
 (8,[(H,14.40,4.2,0.5)]),                         # right down the middle of the skyline -> helicopter past the towers
 (15,[(H,4.40,1.8,0.5),(F,10.40,1.0,0.6)]),        # run by New Sky Helicopter -> Bell 429 on the pad
 (23,[(Z,16.70,1.9,0.5),(F,8.40,1.9,0.6)]),                        # follows the Huangpu River
 (31,[(N6,10.45,1.5,0.5)]),                       # boarding pass
 (34,[(N6,12.10,1.2,0.5)]),                       # headset
 (37,[(Z,0.20,2.4,0.5)]),      # seat by the window
 (41,[(H,6.30,1.3,0.5),(H,3.35,1.0,0.5)]),                         # twin-engine helicopter lifts off
 (49,[(F,7.00,1.3,0.6)]),                         # from the riverside pad
 (52,[(R,2.65,1.15,0.5)]),                        # over the bridges (Nanpu Bridge)
 (57,[(H,8.25,1.7,0.5),(R,0.10,1.4,0.5)]),        # about 300 meters up
 (64,[(H,0.05,2.4,0.5),(H,12.55,1.7,0.5)]),       # the Bund, hundred-year-old buildings
 (73,[(L,87.20,1.0,0.62),(L,92.20,1.1,0.62)]),                         # On the other, Lujiazui
 (78,[(H,10.00,1.1,0.5)]),                        # Shanghai Tower
 (80,[(F,2.00,1.75,0.6)]),                        # the bottle opener
 (83,[(G,7.80,2.0,0.4)]),                         # and Jin Mao
 (87,[(Z,7.35,1.9,0.5),(R,9.45,0.9,0.5)]),        # the Oriental Pearl slides right under you
 (94,[(H,16.60,2.0,0.5)]),                        # But here's the part nobody expects
 (100,[(G,14.20,1.3,0.5),(G,18.00,1.4,0.5)]),                      # only about ten minutes
 (108,[(F,24.00,1.9,0.6),(R,13.20,1.2,0.5)]),     # a seat costs about $280 (card)
 (114,[(L,22.00,1.5,0.62)]),                      # book a few days ahead (route map)
 (120,[(F,21.00,1.4,0.6)]),                       # pick a clear day
 (124,[(NB,12.00,2.6,0.5),(NB,17.40,2.6,0.5)]),   # Comment the word helicopter
]
TAIL=1.2
TITLE=["SHANGHAI","by Helicopter"]; TAG="right through the skyline"
LABELS=[("boarding pass",31),("300 m up",57),("the Bund",64),("bottle opener",80),("Oriental Pearl",87)]
CARDS=[("one seat, about 10 minutes","about $280","about ¥1,980",108,114)]
CTA=('Comment "HELICOPTER"',124)
