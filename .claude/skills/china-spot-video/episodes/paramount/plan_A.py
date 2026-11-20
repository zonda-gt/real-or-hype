# Version A "Chaplin danced here": the story behind it. Hero hook (gold hall), relaxed pace (~1.5 s), handwritten labels.
import sys; sys.path.insert(0,'/home/user/real-or-hype/work/paramount'); from common import *
HERO=(HALL,9.0,3.0,0.5)
COLLAGE=[]
CUES=[
 (9,[(LIN,0.6,1.6,0.5)]),                        # And you still can
 (13,[(NIGHT,0.0,3.3,0.5)]),                     # It's the Paramount (neon tower at night)
 (16,[(EXT,0.4,3.3,0.5)]),                       # It opened in 1933 (Art Deco tower by day)
(20,[(WIDE,118.0,2.0,0.5),(HALL,30.0,2.2,0.5)]),                  # people called it the Far East's number one ballroom
 (30,[(EXT,48.3,2.2,0.5)]),                      # Climb the red staircase
 (34,[(PROMO,7.5,2.7,0.5)]),                     # past paintings of the jazz age (murals)
 (40,[(LIN,24.0,2.6,0.5)]),                      # The main floor was built on springs
 (47,[(SALSA,2.0,2.0,0.5)]),                     # so it bounced under your feet
 (53,[(VLOG,17.76,1.1,0.5),(PROMO,10.4,1.5,0.5)]),# Upstairs, a glass dance floor (round room), dome
 (60,[(RUMBA,7.0,2.6,0.5)]),                     # China's Young Marshal came here to dance
 (67,[(WALK,2.2,2.4,0.5)]),                      # But here's the part nobody expects (corridor)
 (73,[(EXT,10.0,2.5,0.5)]),                      # After the revolution, it became a cinema (the building)
 (80,[(NIGHT,9.6,2.0,0.5)]),                     # and the sprung floor was lost (empty floor)
 (86,[(WALK,0.0,1.8,0.5)]),                      # It reopened in 2017 (the doors)
 (90,[(HALL,24.0,2.6,0.5)]),                     # with a brand new sprung floor
 (96,[(WIDE,15.0,2.6,0.5)]),                     # Today, a live jazz band
 (101,[(P709B,40.0,2.8,0.5)]),                   # plays every afternoon, from 2 to 5
 (108,[(TEA,21.0,3.4,0.5)]),                     # and a ticket for about $25 (card)
 (114,[(LIN,22.0,2.0,0.5),(HALL,45.0,3.0,0.5)]), # Comment the word Paramount
]
TAIL=1.3
TITLE=["CHAPLIN","Danced Here"]; TAG="and you still can"
LABELS=[("since 1933",16),("red staircase",30),("glass floor",53),("live jazz",96)]
CARDS=[("afternoon tea dance","about $25","¥180 per person",108,114)]
CTA=('Comment "PARAMOUNT"',114)
