# Version B "Australia vs China": price comparison. Hero hook (tiger face to face at the glass), fast list cuts, price cards.
import sys; sys.path.insert(0,'/home/user/real-or-hype/work/tiger'); from common import *
HERO=(LI,80.5,3.4,0.5)
COLLAGE=[]
CUES=[
 (11,[(T4K,4.6,0.9,0.5),(HLG,13.0,0.9,0.5)]),      # In China, it's about 24 (card)
 (16,[(LI,12.3,0.6,0.5),(LI,102.4,0.9,0.5)]),      # It's a zoo in Henan
 (22,[(LI,89.6,0.8,0.5),(OFF,12.3,1.0,0.5)]),      # about 30 tiger view rooms
 (27,[(HLG,24.5,0.6,0.5),(V4K,47.0,0.9,0.5)]),     # Floor-to-ceiling glass
 (31,[(GLASS,22.3,1.2,0.5)]),                      # Siberian tigers
 (33,[(LI,112.0,0.9,0.5)]),                        # white tigers
 (35,[(GOLD,28.4,1.0,0.5)]),                       # golden tigers
 (37,[(LI,56.3,1.1,0.45)]),                        # Right outside your bed
 (41,[(OFF,27.3,0.9,0.45)]),                        # they walk past
 (44,[(GLASS,27.0,1.0,0.5)]),                      # they lie down
 (47,[(NIGHT,2.0,1.2,0.5)]),                       # they stare right back
 (51,[(LI,38.6,1.4,0.5)]),                         # They even watch you shower
 (56,[(LI,51.0,0.7,0.5),(HLG,17.1,1.1,0.5)]),      # Staff say the glass is bulletproof
 (62,[(HLG,25.0,1.3,0.5),(OFF,54.2,1.4,0.5)]),     # the price includes two zoo tickets (card)
 (69,[(T4K,5.6,1.3,0.5),(WHITE,1.0,1.2,0.5)]),     # Same view, for a tiny fraction of the price
 (78,[(OFF,44.0,2.2,0.5),(WHITE2,12.5,2.2,0.5)]),  # Comment the word tiger
]
TAIL=1.4
TITLE=["AUSTRALIA: $1,000+","China: $24"]; TAG="a night next to tigers"
LABELS=[]
CARDS=[("in China","about $24","¥168 a night",11,16),("price includes","2 zoo tickets","from ¥168, about $24",62,69)]
CTA=('Comment "TIGER"',78)
CAPTION_FIX={'$1':'$1,000',',000.':''}
