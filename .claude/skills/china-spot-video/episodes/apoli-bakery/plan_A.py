# Version A: "the walkthrough" - relaxed (~1.5 s shots), 2x2 collage + serif title hook, handwritten labels. Voice: John.
from srcs import *
COLLAGE=[(G,11.0,2.4,0.5),(L,36.3,2.2,0.5),(S,27.5,5.0,0.5),(Q,30.0,5.0,0.5)]
CUES=[
 (9, [(G,3.45,1.04,0.5),(S,8.2,2.5,0.5)]),             # It's called Apoli (castle door with the sign)
 (17,[(G,6.0,1.2,0.5)]),                               # Wukang Mansion
 (19,[(S,4.95,3.1,0.5)]),                              # Push open the castle door
 (25,[(Q,9.0,3.5,0.5)]),                               # you're inside stone walls
 (30,[(T,16.4,2.1,0.5)]),                              # twisted branches on the ceiling
 (36,[(T,14.3,1.9,0.5)]),                              # candle chandeliers
 (38,[(P,10.0,3.5,0.5)]),                              # Then come the counters
 (42,[(L,44.2,2.5,0.5)]),                              # Over a hundred breads and pastries
 (48,[(G,22.9,1.4,0.5)]),                              # truffle chicken buns
 (51,[(H,30.0,2.0,0.5)]),                              # pistachio donuts
 (53,[(Q,43.4,1.5,0.5)]),                              # cinnamon swirls
 (55,[(G,66.0,1.9,0.5)]),                              # tiramisu
 (56,[(Q,65.6,2.0,0.5)]),                              # Grab a tray and tongs
 (62,[(T,22.7,1.4,0.5)]),                              # pick whatever you want
 (66,[(G,1.9,1.4,0.5)]),                               # But here's the part nobody expects
 (72,[(L,41.6,2.3,0.5)]),                              # Most pastries cost about two to three dollars (card)
 (80,[(P,4.0,3.0,0.5)]),                               # No booking, and no entry fee
 (86,[(T,7.2,1.7,0.5),(R,23.2,2.6,0.5)]),              # Go on a weekday morning, before the queue
 (94,[(G,10.6,2.9,0.5),(Q,21.0,4.0,0.5)]),             # Comment castle
]
TAIL=1.3
TITLE=["SHANGHAI'S","Hogwarts Bakery"]; TAG="pastries from $2"
LABELS=[("across from Wukang Mansion",17),("100+ breads",42),("pistachio donut",51),("tray + tongs",56),("go before the queue",86)]
CARDS=[("most pastries","$2–3","about ¥12–25 each",72,80)]
CTA=('Comment "CASTLE"',94)
CAPTION_FIX={'Apoli':'APOLI'}
