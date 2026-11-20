# A "Dress up and dine like an emperor": walkthrough in the order you live it. 2x2 collage hook, medium pace, handwritten labels.
import sys,os; sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); from common import *
COLLAGE=[(V,0.0,1.1,0.5),(S,23.4,1.5,0.5),(F,44.4,1.5,0.5),(D,4.1,1.4,0.5)]
CUES=[
 (7,[(V,12.1,1.9,0.5)]),                 # dress up -> robe rack
 (10,[(S,23.4,1.5,0.5)]),                # Tang dynasty royalty -> two Tang hosts
 (15,[(G,1.1,1.1,0.5)]),                 # the show
 (18,[(R,21.7,2.8,0.5)]),                # all around your table -> 360 hall
 (21,[(D,10.2,2.3,0.5)]),                # It's called Yan Tianxia -> red door sign
 (25,[(X,12.9,1.5,0.5)]),                # on the West Bund
 (29,[(V,9.2,1.4,0.5)]),                 # pick a silk robe
 (32,[(V,12.4,1.6,0.5)]),
 (35,[(V,15.5,1.6,0.5)]),                # hair and makeup
 (39,[(R,19.6,1.0,0.5)]),
 (41,[(D,18.0,1.6,0.5)]),                # walk into a round hall
 (48,[(L,15.5,2.7,0.5)]),                # wrapped in a 360 screen
 (51,[(X,1.9,1.9,0.5)]),
 (54,[(R,35.75,1.65,0.5)]),# sit in the front row
 (60,[(P,17.2,3.2,0.5,WASH)]),           # someone washes your hands
 (66,[(G,7.6,1.1,0.5)]),                 # seven acts
 (68,[(X,3.95,1.8,0.5)]),
 (71,[(S,63.6,3.6,0.5)]),                # 90 minutes
 (73,[(S,67.4,1.4,0.5)]),  # dancers fly
 (77,[(S,9.2,1.35,0.5)]),                # over your head
 (80,[(D,4.05,1.5,0.5)]),                # snow
 (85,[(F,33.4,2.8,0.5)]),                # every act brings a new dish
 (90,[(G,57.95,1.0,0.5)]),
 (93,[(F,41.65,1.1,0.5),(G,62.0,1.2,0.5)]),                # Buddha jumps over the wall
 (99,[(X,40.15,1.0,0.5),(X,41.2,1.2,0.5)]),                # golden broth
 (101,[(S,7.6,1.5,0.5)]),                # ends in 1930s Shanghai
 (105,[(V,77.4,1.0,0.5),(G,50.0,1.2,0.5)]),
 (107,[(S,60.3,3.1,0.5)]),               # disco ball
 (111,[(X,7.7,2.3,0.5)]),                # dinner from about $70 (card)
 (116,[(G,79.6,1.6,0.5),(G,81.4,1.8,0.5)]),  # come for the show
 (120,[(F,59.8,2.2,0.5)]),               # not to get full
 (124,[(V,93.9,2.8,0.5),(G,75.5,1.7,0.5)]),               # CTA over the finale
]
TAIL=1.3
TITLE=["SHANGHAI'S","Palace Banquet"]; TAG="dinner + a show"
LABELS=[("silk robes",32),("hair + makeup",39),("front row",54),("hand washing",60),("golden broth",99),("1930s Shanghai",105)]
CARDS=[("dinner, per person","from ¥498","about $70",111,116)]
CTA=('Comment "BANQUET"',124)
