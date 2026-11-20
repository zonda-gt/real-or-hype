# C "4 things before you go": insider list. Snow-dance hero + title card, relaxed pace (~1.6 s), numbered #1-#4 labels.
import sys,os; sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); from common import *
HERO=(V,38.5,1.95,0.5); COLLAGE=[]
CUES=[
 (8,[(G,26.0,2.3,0.5)]),                # Shanghai's palace banquet dinner show
 (13,[(D,10.2,1.2,0.5),(X,12.9,1.3,0.5)]),                # It's called Yan Tianxia
 (21,[(D,19.3,1.7,0.5),(R,21.8,1.7,0.5)]),     # One: book your seat ahead
 (32,[(P,17.2,3.2,0.5,WASH)]),           # only the front row gets the hand-washing ritual
 (41,[(R,19.6,1.0,0.5),(V,12.1,1.9,0.5)]),     # Two: arrive early to dress up
 (49,[(V,9.2,1.4,0.5)]),                 # a silk robe
 (52,[(V,15.5,1.65,0.5)]),                # hair and makeup
 (56,[(V,21.0,1.4,0.5)]),                # about $30 (card)
 (59,[(S,23.4,1.5,0.5),(D,1.6,1.0,0.5)]),                # Three: not only the Tang dynasty
 (66,[(G,29.95,1.75,0.5)]),              # seven acts
 (70,[(X,17.15,2.2,0.5)]),               # from ancient China
 (76,[(S,60.3,3.1,0.5)]),                # 1930s Shanghai
 (81,[(V,69.2,1.75,0.5)]),               # come for the show
 (86,[(F,84.5,1.0,0.5)]),                # not the food
 (89,[(G,61.8,2.9,0.5)]),                # the dishes look great
 (93,[(F,51.5,1.2,0.5),(F,59.8,1.0,0.5)]),    # portions are small
 (100,[(X,1.9,1.9,0.5),(L,1.3,1.15,0.5)]),   # about $70 to $100 (card)
 (108,[(R,45.3,1.4,0.5),(V,93.9,2.8,0.5)]),   # CTA
]
TAIL=1.3
TITLE=["4 THINGS","before you go"]; TAG="Shanghai's palace banquet"
LABELS=[("#1 book ahead",21),("#2 dress up",41),("#3 not just Tang",59),("#4 it's a show",81)]
CARDS=[("robe + hair + makeup","¥200","about $30",56,59),("dinner, per person","¥498–688","about $70–$100",100,108)]
CTA=('Comment "BANQUET"',108)
