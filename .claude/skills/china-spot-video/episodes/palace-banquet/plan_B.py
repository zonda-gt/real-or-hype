# B "A $70 dinner that's actually a show": price/value angle. Full-screen aerial hero + title, fast list cuts (~0.9 s), price cards.
import sys,os; sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); from common import *
HERO=(S,9.2,1.35,0.5); COLLAGE=[]
CUES=[
 (5,[(X,7.7,1.5,0.5)]),                  # comes with
 (8,[(G,1.1,0.8,0.5),(R,3.4,0.9,0.5)]),  # 90-minute show
 (11,[(R,1.85,1.42,0.5)]),                # It's called Yan Tianxia
 (15,[(L,1.3,1.15,0.5)]),                # palace banquet
 (18,[(X,12.9,0.7,0.5),(D,10.2,0.8,0.5)]),                # on the West Bund
 (22,[(V,63.95,0.9,0.5)]),               # Acrobats fly
 (24,[(S,68.0,1.6,0.5)]),                # on silk ribbons
 (27,[(L,19.35,0.75,0.5),(S,63.6,0.8,0.5)]),               # dancers spin
 (30,[(V,72.05,0.95,0.5),(D,4.05,1.5,0.5)]),   # falling snow
 (32,[(R,21.8,1.5,0.5)]),                # a 360 screen
 (36,[(V,38.5,0.7,0.5),(X,1.9,0.8,0.5)]),                # wraps the whole room
 (40,[(L,23.45,1.1,0.5)]),               # with every act
 (44,[(X,25.8,1.0,0.5),(F,33.4,1.2,0.5)]),               # a new course lands
 (52,[(X,40.15,1.0,0.5),(X,41.2,1.2,0.5)]),    # Buddha jumps over the wall
 (57,[(L,49.7,1.5,0.5)]),                # Tang-style beef
 (60,[(R,39.7,1.1,0.5)]),                # braised pork
 (63,[(D,39.0,1.35,0.5)]),               # black truffle
 (65,[(R,19.6,0.85,0.5),(D,1.6,1.0,0.5)]),                # full royal look
 (70,[(V,9.2,0.9,0.5)]),                 # a robe
 (72,[(V,15.5,1.6,0.5)]),                # hair and makeup
 (75,[(V,21.0,1.3,0.5),(V,24.0,1.0,0.5)]),                # cost about $30 more (card)
 (79,[(D,23.75,0.95,0.5),(L,5.25,1.15,0.5),(R,35.75,1.65,0.5)]),  # front row seats ~$100 (card)
 (89,[(P,17.3,1.6,0.5,WASH)]),           # hand-washing ritual
 (93,[(G,66.1,0.55,0.5),(F,70.5,0.7,0.5)]),               # honest part
 (97,[(F,51.5,0.7,0.5),(F,59.8,0.8,0.5)]),               # portions are small
 (101,[(V,69.2,0.65,0.5),(L,27.75,0.8,0.5)]), # paying for the show
 (106,[(L,63.1,1.8,0.5),(G,75.5,1.7,0.5),(R,45.3,1.4,0.5)]),    # CTA
]
TAIL=1.3
TITLE=["A $70 DINNER","that's a show"]; TAG="Shanghai"
CARDS=[("robe + hair + makeup","¥200","about $30",75,79),("front-row dinner","¥688","about $100",79,89)]
LABELS=[("Buddha Jumps Over the Wall",52),("Tang-style beef",57),("black truffle pork",60)]
CTA=('Comment "BANQUET"',106)
