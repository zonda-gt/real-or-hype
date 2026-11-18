# Version A "Sleep with tigers": the night in order. Collage hook of the four biggest wow shots, medium pace, handwritten labels.
import sys; sys.path.insert(0,'/home/user/real-or-hype/work/tiger'); from common import *
COLLAGE=[(HLG,20.0,3.5,0.5),(NIGHT,0.0,3.9,0.5),(LI,55.6,2.4,0.45),(WHITE,0.2,3.9,0.5)]
CUES=[
 (14,[(LI,12.30,1.40,0.5)]),                      # It's in Henan -> the zoo gate
 (18,[(LI,89.6,0.8,0.5),(LI,102.3,1.6,0.5)]),    # about 30 rooms -> room, beds by the window
 (24,[(HLG,13.0,1.1,0.5),(OFF,12.2,1.6,0.5)]),                       # a glass wall facing the tigers
 (29,[(LI,27.4,1.6,0.5)]),                        # Lie on the bed
 (35,[(OFF,26.7,2.3,0.45)]),                       # a Siberian tiger walks right past your feet (rocking chair)
 (42,[(LI,34.6,0.8,0.5),(LI,38.5,1.8,0.5)]),      # Even the shower looks out at them
 (49,[(GLASS,21.6,1.5,0.5),(OFF,44.2,1.6,0.5)]),                     # Then one lies down against the glass
 (57,[(HLG,17.0,1.6,0.5)]),                       # just stares at you (hand next to the tiger)
 (61,[(LI,112.0,1.1,0.5),(OFF,54.2,1.2,0.5)]),                       # Later, a white tiger strolls by
 (67,[(WHITE2,12.0,3.0,0.5)]),                    # At night, they mostly sleep under the lights
 (76,[(T4K,3.3,4.2,0.5)]),      # in the morning, one walks straight up to your window
 (86,[(V4K,47.0,1.1,0.5),(GLASS,4.0,0.8,0.5)]),                       # But here's the part nobody expects
 (92,[(HLG,24.2,1.5,0.5),(LI,32.1,1.4,0.5),(LI,102.4,1.6,0.5)]),     # Rooms start at about $24 (card)
 (103,[(GOLD,28.2,1.3,0.5),(NIGHT,2.2,1.3,0.5),(WHITE,12.5,1.8,0.5)]), # Comment the word tiger
]
TAIL=1.4
TITLE=["CHINA'S","Tiger Hotel"]; TAG="the glass is the wall"
LABELS=[("Siberian tiger",35),("shower with a view",42),("white tiger",61),("good morning",76)]
CARDS=[("rooms from","about $24","¥168 + 2 zoo tickets",92,103)]
CTA=('Comment "TIGER"',103)
