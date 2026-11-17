# Version C: "4 things to know" - insider list, medium pace (~1.2 s), one full-screen hero shot under the serif title, #1-#4 stickers.
from srcs import *
COLLAGE=[(P,32.5,3.5,0.5)]                             # crowded castle counter under the title
CUES=[
 (10,[(H,8.2,1.0,0.7),(R,4.2,1.1,0.5)]),               # Number one, it's not official Harry Potter
 (17,[(P,12.0,2.2,0.5)]),                              # It's an Italian bakery called Apoli (sign)
 (23,[(R,5.5,0.8,0.5)]),                               # but the stone walls
 (27,[(T,14.3,1.1,0.5)]),                              # and candle chandeliers
 (30,[(R,26.3,1.2,0.5)]),                              # feel like a castle (facade)
 (34,[(S,5.0,0.7,0.5),(S,6.0,0.8,0.5)]),               # Number two, you can't book
 (39,[(T,7.2,1.1,0.5),(R,23.3,1.1,0.5)]),              # When it opened, people queued over an hour
 (47,[(P,53.0,0.8,0.5),(P,54.2,0.8,0.5)]),             # so go on a weekday morning
 (53,[(S,36.9,0.9,0.5),(S,38.0,0.9,0.5)]),             # Number three, it's self-service
 (58,[(Q,65.7,1.5,0.5)]),                              # Grab a tray and tongs
 (63,[(Q,45.0,0.9,0.5),(L,44.5,0.9,0.5)]),             # pick from over a hundred breads
 (69,[(T,12.0,1.2,0.5)]),                              # then pay at the till
 (74,[(G,62.2,0.7,0.5),(G,62.9,0.7,0.5)]),             # Number four, it's cheap
 (78,[(L,30.0,1.1,0.5),(S,27.5,1.1,0.5)]),             # Most pastries are two to three dollars
 (85,[(L,49.85,2.3,0.5)]),                             # the mentaiko bread is the one everyone recommends (TOP1)
 (94,[(G,4.55,1.4,0.5)]),                              # It's right across from
 (98,[(G,6.0,1.2,0.5)]),                               # Wukang Mansion
 (100,[(G,15.6,1.1,0.5),(G,16.7,1.1,0.5),(G,11.3,1.2,0.5)]),  # Comment castle
]
TAIL=1.3
TITLE=["4 THINGS","to know before you go"]; TAG="Shanghai's Hogwarts bakery"
LABELS=[("#1 not official Harry Potter",10),("#2 no booking",34),("#3 self-service",53),("#4 cheap",74),("Wukang Mansion",98)]
CARDS=[("most pastries","$2–3","about ¥12–25",78,85),("everyone's pick","mentaiko bread","about ¥15 ($2)",85,94)]
CTA=('Comment "CASTLE"',100)
CAPTION_FIX={'Apolli,':'APOLI','Wukong':'Wukang','So,':'So'}
