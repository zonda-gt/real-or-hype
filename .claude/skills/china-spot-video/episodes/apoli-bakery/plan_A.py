# Version A "Walk into Hogwarts": the experience in order. Collage hook, medium pace, handwritten labels.
import sys; sys.path.insert(0,'/home/user/real-or-hype/work/apollo')  # copy common.py from this folder into the work dir; from common import *
COLLAGE=[(E,30.0,3.5,0.5),(A1,9.0,1.4,0.5),(E,22.0,3.5,0.5),(N,42.0,3.5,0.5)]
CUES=[
 (10,[(A1,3.40,1.05,0.5),(A1,4.55,1.4,0.5)]),   # It's called Apoli -> glowing door, then the APOLI wall
 (16,[(W3,0.3,2.5,0.5)]),                        # Wukang Mansion
 (18,[(E,0.10,2.2,0.5)]),                        # Walk up the steps
 (23,[(E,4.80,2.5,0.5)]),                        # grab a wooden tray
 (28,[(A1,18.2,2.4,0.5)]),                       # tongs (filling a tray)
 (34,[(E,9.90,2.0,0.5)]),                        # Inside
 (36,[(E,43.6,1.6,0.5)]),                        # stone arches
 (38,[(A1,8.80,1.6,0.5)]),                       # glowing lanterns
 (41,[(E,27.2,2.5,0.5)]),                        # branches crawling across the ceiling
 (46,[(E,12.8,2.6,0.5)]),                        # over a hundred kinds of bread
 (54,[(D,30.0,1.0,0.45)]),                       # pistachio
 (56,[(A1,10.6,1.6,0.5)]),                       # matcha donuts
 (59,[(N,37.3,1.6,0.5)]),                        # cream buns
 (61,[(E,14.0,2.2,0.5)]),                        # piled up like treasure
 (66,[(A1,15.5,2.5,0.5)]),                       # behind the glass, bakers
 (72,[(A1,16.6,1.4,0.5),(D,13.4,1.9,0.5)]),      # making the next batch
 (80,[(E,29.0,2.6,0.5)]),                        # But here's the part nobody expects
 (86,[(D,44.2,0.9,0.5),(N,31.0,1.6,0.5)]),       # Most pastries cost less than $3 (card)
 (92,[(E,32.3,2.6,0.5)]),                        # You can't book
 (96,[(W1,1.0,3.0,0.45)]),                       # weekday morning
 (101,[(E,45.0,2.0,0.5),(E,52.3,3.5,0.5)]),      # Comment the word castle
]
TAIL=1.4
TITLE=["SHANGHAI'S","Hogwarts Bakery"]; TAG="it's real"
LABELS=[("grab a tray",23),("Wukang Mansion",16),("100+ kinds",46),("baked in front of you",66)]
CARDS=[("most pastries","under $3","about ¥20",86,92)]
CTA=('Comment "CASTLE"',101)
