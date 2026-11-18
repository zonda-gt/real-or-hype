# Version A "Red panda alarm clock": the stay in order. Collage hook (4 in-room wow clips), medium pace, handwritten labels.
import sys; sys.path.insert(0,'/home/user/real-or-hype/work/redpanda'); from common import *
COLLAGE=[(P,1.95,2.05,0.5),(H,7.40,1.30,0.5),(G,48.70,2.50,0.45),(L,8.65,2.50,0.5)]
CUES=[
 (13,[(G,72.20,2.2,0.5)]),                        # It's inside Yancheng Wild Animal World (ZOO sign)
 (19,[(A9,19.05,1.3,0.5),(S,4.25,1.7,0.45)]),     # in Changzhou, about an hour and a half from Shanghai (aerials)
 (29,[(R,2.20,1.55,0.35)]),                       # You sleep in an RV
 (35,[(H,16.75,1.35,0.5)]),                       # or a glass capsule
 (38,[(A9,29.55,2.2,0.5)]),                       # right in the zoo
 (45,[(L,0.30,2.9,0.5)]),                         # there's a knock (door opens, red panda inside)
 (49,[(A9,41.65,1.15,0.35),(A9,1.20,0.95,0.5)]),  # the keeper brings a red panda into your room
 (58,[(L,5.60,3.0,0.5)]),                         # It climbs onto your bed
 (63,[(P,13.75,3.6,0.5)]),                        # sniffs around
 (66,[(A9,9.10,1.30,0.45)]),                       # lets you stroke its back
 (71,[(L,17.85,2.8,0.5)]),                        # Then you feed it apple
 (76,[(L,20.75,2.3,0.5)]),                        # right from your hand
 (80,[(R,32.25,1.7,0.6)]),                        # At breakfast
 (82,[(H,29.10,1.05,0.5),(H,26.30,1.15,0.5)]),    # more red pandas wander past the window
 (89,[(G,58.50,1.95,0.5)]),                       # two days in the zoo
 (98,[(S,10.05,2.8,0.5)]),                        # and a safari drive (camel at the car window)
 (102,[(A9,13.50,1.40,0.5),(A9,59.60,1.25,0.5)]), # Packages start around $120 (card)
 (106,[(H,19.15,1.25,0.5),(H,21.92,0.60,0.5),(A9,0.05,1.1,0.5)]),    # Book the capsule where red pandas come in
 (114,[(H,24.50,1.75,0.55),(P,7.72,2.05,0.5)]),  # Comment the word red panda
]
TAIL=1.3
TITLE=["CHINA'S","Red Panda Hotel"]; TAG="your alarm clock"
LABELS=[("inside the zoo",38),("knock knock",45),("apple snack",71),("the Red Panda Capsule",106)]
CARDS=[("packages from","about $120","about ¥850 · tickets incl.",102,106)]
CTA=('Comment "REDPANDA"',114)
CAPTION_FIX={'Yanchen':'Yancheng'}
