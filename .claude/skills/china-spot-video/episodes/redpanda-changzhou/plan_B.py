# Version B "What $120 gets you": price punchline. Hero hook (red panda walks straight up to the lens), fast list cuts, price cards.
import sys; sys.path.insert(0,'/home/user/real-or-hype/work/redpanda'); from common import *
HERO=(L,3.25,1.33,0.5)
COLLAGE=[]
CUES=[
 (11,[(A9,2.86,0.55,0.5)]),                       # Here's
 (13,[(R,3.85,0.7,0.5)]),                         # the whole deal
 (15,[(A9,29.60,0.6,0.5)]),                       # One night
 (19,[(H,19.20,0.55,0.5)]),                       # in a glass capsule
 (21,[(G,72.25,0.7,0.5),(A9,30.70,0.6,0.5)]),                        # inside a zoo
 (25,[(S,4.25,0.65,0.45)]),                       # in Changzhou
 (26,[(A9,1.20,0.95,0.5)]),                       # a red panda visit
 (30,[(A9,41.65,0.9,0.35)]),                      # in the morning (keeper's carrier)
 (33,[(L,4.70,0.65,0.5)]),                        # It climbs up
 (36,[(T,2.80,0.68,0.5)]),                        # says hi
 (38,[(L,18.40,0.7,0.5)]),                        # and eats
 (40,[(L,20.80,1.2,0.5)]),                        # apple from your hand
 (44,[(A9,25.40,0.85,0.5)]),                      # Breakfast
 (46,[(H,26.60,0.88,0.5)]),                        # with red pandas
 (48,[(A9,13.50,1.2,0.5)]),                       # outside the window
 (51,[(G,62.20,0.75,0.5)]),                       # Two days
 (54,[(G,73.40,0.9,0.5)]),                        # of zoo tickets
 (56,[(A9,61.85,1.2,0.5)]),                       # a safari drive
 (60,[(A9,64.75,0.6,0.5)]),                       # deer
 (62,[(S,10.05,0.7,0.5)]),                        # and camels
 (63,[(A9,63.25,1.4,0.5)]),                       # poke their heads into your car
 (69,[(H,54.00,0.75,0.5)]),                       # and an hour
 (71,[(H,55.35,0.85,0.5)]),                       # long
 (73,[(H,61.20,0.9,0.5)]),                        # circus
 (74,[(R,8.35,0.65,0.5)]),                        # The zoo tickets
 (77,[(G,8.50,1.0,0.4)]),                         # alone cost
 (80,[(P,2.00,1.3,0.5)]),                         # about $50 for two
 (83,[(P,9.90,1.0,0.5),(Q,6.00,1.0,0.45),(A9,58.20,1.3,0.6),(H,24.50,1.5,0.55)]),  # Comment the word red panda
]
TAIL=1.3
# title drawn near the top by title_top.py (the panda's face fills the middle of the hero)
TITLE_Y=150
TITLE=["$120 IN CHINA","gets you this"]; TAG="a red panda on your bed"
LABELS=[]
CARDS=[("1 night + red panda visit","about $120","about ¥850 · family package",15,26),
       ("zoo tickets alone","about $50","¥189 each · for two",74,83)]
CTA=('Comment "REDPANDA"',83)
