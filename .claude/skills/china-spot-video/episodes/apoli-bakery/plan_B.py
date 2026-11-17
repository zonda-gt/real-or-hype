# Version B: "London vs Shanghai" price comparison - fast (~0.9 s shots), full-screen opener under a price card, no collage.
from srcs import *
COLLAGE=[]
CUES=[
 (0, [(G,13.6,1.0,0.5),(G,15.5,1.0,0.5),(G,16.6,0.9,0.5),(G,11.2,1.0,0.5)]),  # Harry Potter studio tour in London ... $77 (card, slow-mo)
 (10,[(R,26.3,1.4,0.5)]),                               # In Shanghai, there's a castle (stone facade)
 (17,[(S,5.0,0.8,0.5),(S,6.3,0.8,0.5)]),               # you can walk into for free
 (21,[(P,51.6,0.8,0.5),(P,0.5,0.8,0.5),(P,2.0,0.8,0.5)]),  # It's a bakery called Apoli, across from
 (28,[(G,6.0,1.0,0.5)]),                               # Wukang Mansion
 (30,[(P,44.0,0.9,0.5)]),                              # Stone arches
 (32,[(R,4.0,1.1,0.5)]),                               # candle chandeliers
 (35,[(H,8.2,1.0,0.7),(H,9.2,1.0,0.3)]),               # branches growing over the counters
 (40,[(G,0.6,1.3,0.5)]),                               # It's not official Harry Potter
 (45,[(P,10.2,1.2,0.5)]),                              # it's an Italian bakery
 (49,[(T,12.0,1.0,0.5),(T,16.4,1.1,0.5)]),             # But people here call it the Harry Potter bakery
 (58,[(H,13.4,0.8,0.6)]),                              # And the prices?
 (61,[(L,48.3,1.0,0.5),(L,50.5,1.0,0.5),(Q,48.0,0.9,0.5)]),  # The most recommended bread, mentaiko (TOP1)
 (69,[(H,30.2,1.1,0.35)]),                             # Pistachio donuts
 (71,[(G,66.4,0.8,0.6)]),                              # tiramisu
 (72,[(H,26.5,0.9,0.5)]),                              # truffle chicken buns
 (75,[(S,27.5,0.8,0.5),(S,40.0,0.8,0.5)]),             # all around two to three dollars
 (80,[(G,8.7,0.9,0.5),(G,55.2,0.9,0.5)]),              # A full tray and a coffee, about fifteen
 (88,[(P,48.0,1.0,0.5),(P,33.0,1.0,0.5)]),             # That's a fifth of one London ticket
 (95,[(R,23.2,1.0,0.5),(R,24.3,1.1,0.5)]),             # When it opened, people queued over an hour
 (103,[(S,17.6,1.1,0.5),(S,20.0,1.1,0.5),(S,13.5,1.2,0.5)]),  # Comment castle
]
TAIL=1.3
TITLE=[]; TAG=None
LABELS=[("Shanghai, not London",10),("Wukang Mansion",28),("Italian, not official",45),("queued 1 hour+",99)]
CARDS=[("Harry Potter studio tour, London","$77","one adult ticket",0,10),
       ("mentaiko bread","¥15","about $2",65,69),
       ("most pastries","$2–3","about ¥12–25",75,80),
       ("full tray + coffee","$15","1/5 of one London ticket",80,95)]
CTA=('Comment "CASTLE"',103)
CAPTION_FIX={'handle':'candle','Apoli':'APOLI'}
