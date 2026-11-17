# Version B "London vs Shanghai": price comparison. Hero hook (glowing door, slow-mo), fast list cuts, price cards.
import sys; sys.path.insert(0,'/home/user/real-or-hype/work/apollo')  # copy common.py from this folder into the work dir; from common import *
HERO=(A1,3.40,1.05,0.5)
COLLAGE=[]
CUES=[
 (9,[(E,0.40,1.0,0.5),(E,2.4,1.4,0.5)]),         # In Shanghai, you can walk into a castle
 (17,[(E,10.5,1.2,0.5)]),                        # for the price
 (20,[(D,30.5,1.6,0.45)]),                       # of a donut
 (23,[(A1,4.55,1.3,0.5),(B1,12.0,0.9,0.5)]),     # It is a bakery called Apoli
 (28,[(A1,6.00,1.2,0.5)]),                       # across from Wukang Mansion
 (32,[(E,16.6,2.2,0.5)]),                        # people call it the Hogwarts bakery
 (39,[(M,45.0,1.2,0.5)]),                        # Stone walls
 (41,[(A1,9.2,0.9,0.5)]),                        # Glowing lanterns
 (43,[(B1,10.0,1.0,0.5)]),                       # Chandeliers
 (44,[(E,27.8,1.4,0.5)]),                        # Branches over your head
 (48,[(E,13.3,1.0,0.5)]),                        # Then, the bread
 (51,[(D,38.0,0.7,0.5),(D,42.2,0.8,0.5)]),       # Over a hundred kinds
 (54,[(F,20.8,0.9,0.5)]),                        # Pistachio
 (55,[(A1,11.4,0.8,0.5)]),                       # Matcha
 (56,[(N,31.0,0.8,0.5)]),                        # Berries
 (57,[(N,38.0,0.9,0.5)]),                        # Cream
 (58,[(D,44.2,0.9,0.5),(F,68.5,1.4,0.5)]),       # less than three dollars (card)
 (64,[(E,5.2,1.3,0.5)]),                         # Grab a tray
 (67,[(E,14.4,1.2,0.5)]),                        # pick whatever you want
 (72,[(E,48.3,1.4,0.5),(E,53.4,1.6,0.5)]),       # eat it on the street outside
 (78,[(W1,4.5,3.0,0.45)]),                       # Same magic, tiny fraction of the price
 (87,[(M,0.30,4.4,0.5)]),                        # Comment the word castle (night storefront)
]
TAIL=1.4
TITLE=["LONDON: $75","Shanghai: $3"]; TAG="same magic?"
LABELS=[]
CARDS=[("most pastries here","under $3","about ¥20",58,64)]
CTA=('Comment "CASTLE"',87)
