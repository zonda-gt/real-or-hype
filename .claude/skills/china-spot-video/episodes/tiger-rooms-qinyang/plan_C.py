# Version C "4 things before you book": insider list. Hero hook (tiger walks straight up to the window, 4K), relaxed pace, numbered stickers.
import sys; sys.path.insert(0,'/home/user/real-or-hype/work/tiger'); from common import *
HERO=(T4K,4.3,3.3,0.5)
COLLAGE=[]
CUES=[
 (11,[(HLG,13.0,1.3,0.5)]),                        # One: it's real
 (14,[(LI,12.3,1.0,0.5)]),                         # A zoo in Henan
 (18,[(LI,89.6,1.3,0.5)]),                         # has about 30 rooms
 (22,[(HLG,24.0,1.0,0.5)]),                        # with glass walls
 (25,[(GLASS,21.5,2.2,0.5)]),                      # and tigers on the other side
 (31,[(WOMAN,1.0,2.5,0.55)]),                      # Two: you book by phone, in Chinese
 (38,[(HLG,25.0,1.6,0.5),(LI,102.4,1.6,0.5)]),     # Rooms start at about $24 (card)
 (47,[(OFF,26.9,1.8,0.45)]),                        # and holidays cost more
 (51,[(WHITE2,12.0,2.2,0.5)]),                     # Three: the tigers mostly sleep at night
 (58,[(T4K,8.0,1.8,0.5)]),                         # so set an alarm for the morning
 (65,[(LI,15.8,1.9,0.5)]),      # Four: it's far from Shanghai
 (70,[(LI,13.1,2.4,0.5),(V4K,46.8,1.5,0.5)]),                         # Take the fast train to Zhengzhou, then about an hour (card)
 (84,[(LI,80.6,2.0,0.5),(WHITE,12.5,2.4,0.5)]),    # Comment the word tiger
]
TAIL=1.4
TITLE=["4 THINGS","before you book"]; TAG="China's tiger view rooms"
LABELS=[("#1 it's real",11),("#2 call, in Chinese",31),("#3 they sleep at night",51),("#4 it's far",65)]
CARDS=[("rooms from","about $24","¥168 + 2 zoo tickets",38,47),("Zhengzhou to the zoo","about 1 hour","train to Jiaozuo + taxi",70,84)]
CTA=('Comment "TIGER"',84)
