# Version B "New York vs Shanghai": price comparison. Hero hook (helicopter past Shanghai Tower at night), fast cuts, price cards.
import sys; sys.path.insert(0,'/home/user/real-or-hype/work/helicopter'); from common import *
HERO=(N1,0.6,1.3,0.5)
COLLAGE=[]
CUES=[
 (4,[(H,6.30,1.9,0.5),(H,2.50,0.8,0.5),(R,0.10,1.4,0.5)]),  # a tour over Manhattan costs about $300 (card, generic helicopter shots)
 (10,[(H,0.05,1.15,0.5)]),                        # Over Shanghai
 (12,[(R,5.00,1.0,0.5),(K,2.10,0.9,0.5)]),       # a seat costs about the same (card)
 (18,[(R,1.65,0.95,0.5),(N6,12.10,1.2,0.5)]),     # for around ten minutes
 (22,[(N1,6.20,0.8,0.5),(N1,9.00,0.9,0.5)]),                        # So which skyline wins?
 (26,[(F,11.50,1.4,0.6)]),                        # In Shanghai
 (28,[(Z,16.70,1.0,0.5),(F,21.00,0.95,0.6),(F,8.40,1.0,0.6)]),      # the flight runs straight down the Huangpu River
 (36,[(H,8.25,1.7,0.5),(F,16.50,0.6,0.6)]),       # about 300 meters up
 (40,[(H,12.55,1.75,0.5)]),                       # On one bank, the Bund
 (45,[(H,0.65,0.9,0.5),(G,11.00,0.9,0.5)]),                         # built about a hundred years ago
 (50,[(L,92.0,1.1,0.62)]),                        # On the other
 (53,[(F,16.60,1.0,0.6)]),                        # Lujiazui
 (54,[(F,30.50,1.25,0.6)]),                       # Shanghai Tower
 (56,[(H,10.00,1.15,0.5),(F,32.60,0.9,0.6)]),     # the tallest building in China
 (61,[(F,2.00,1.3,0.6)]),                         # the bottle opener
 (64,[(G,7.80,0.75,0.4)]),                        # Jin Mao
 (66,[(Z,8.30,1.4,0.5),(R,9.45,0.9,0.5)]),        # and the Oriental Pearl, right under your feet
 (74,[(NB,5.75,2.6,0.5)]),                        # Then, after dark (night take-off)
 (77,[(N3,0.20,1.0,0.5)]),                        # the whole skyline
 (80,[(N4,6.00,1.8,0.5)]),                        # lights up
 (82,[(N2,1.20,0.85,0.6),(N2,5.00,0.9,0.6)]),                        # Night flights cost a little more (card)
 (88,[(N1,21.00,1.5,0.5)]),                       # but you get the lights
 (93,[(N3,11.00,1.2,0.5)]),                       # Same money as New York
 (98,[(N1,2.40,1.2,0.5),(N4,8.00,1.3,0.5)]),                        # a skyline that looks like the future
 (106,[(N4,13.50,1.4,0.5),(N1,24.0,1.4,0.5),(N3,12.0,1.6,0.5)]),    # Comment the word helicopter
]
TAIL=1.2
TITLE=["NEW YORK","or Shanghai?"]; TAG="same price"
LABELS=[("the Bund",40),("tallest in China",56),("bottle opener",61)]
CARDS=[("Manhattan, 12-15 min","about $300","with fees",4,10),
       ("Shanghai, about 10 min","about $280","about ¥1,980 a seat",12,22),
       ("night flight","about $300","about ¥2,180 a seat",82,88)]
CTA=('Comment "HELICOPTER"',106)
