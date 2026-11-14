# Version F: "Kenya vs China". Third distinct edit. Voice: John.
B2='7653507861812628772'; G='7651132730540887336'; R='7653362319732886150'
WAKE='7702806207996158385'; AI='ai_me_breakfast'; AI2='ai_me_capybara'
WAKE2='7685311414965524923'; BKF='6976808703164992805'; CALF2='7653265250729437775'
SKY='7706044234537230691'     # vertical: giraffe against the sky (generic, used for the Kenya line)
SLIDE='7696448570602560619'   # vertical 60fps: bamboo suspension bridge 20-55, bamboo slide 130-136 (avoid 140+ letterboxed)
SRC={B2:{'cut':0.14},G:{'cut':0.14},R:{'cut':0.18},WAKE:{},AI:{},AI2:{},WAKE2:{},BKF:{},CALF2:{},SKY:{},SLIDE:{}}
COLLAGE=[(R,75.70,1.45,0.78),(G,26.00,1.80,0.33),(B2,0.30,2.00,0.60),(R,72.00,1.20,0.5)]
CUES=[
 (6, [(SKY,0.00,1.80,0.5),(SKY,13.40,1.50,0.5)]),       # costs over $1,400 a night, per person (Kenya card)
 (13,[(G,9.88,1.55,0.5),(SLIDE,28.00,2.00,0.5)]),       # China built its own version, two hours from Shanghai
 (22,[(R,73.25,1.05,0.5),(G,5.36,1.50,0.62)]),          # It's called Giraffe Manor, in Huzhou
 (28,[(WAKE2,13.00,3.80,0.5)]),                         # Same idea.
 (30,[(R,37.00,1.10,0.5)]),                             # At breakfast,
 (32,[(AI,0.05,1.45,0.5),(BKF,7.00,1.50,0.60)]),        # a giraffe pushes its whole head through your window
 (41,[(AI,2.40,1.64,0.5)]),                             # Hold out a carrot, and it takes it
 (49,[(R,70.60,1.13,0.45)]),                            # right from your hand
 (53,[(SLIDE,131.00,1.50,0.5)]),                        # And there's more.
 (56,[(CALF2,7.40,3.00,0.5)]),                          # Two baby giraffes have been born here
 (63,[(WAKE,27.90,2.00,0.5)]),                          # Book the animal wake-up call,
 (69,[(WAKE,48.30,3.00,0.5)]),                          # and sometimes a raccoon walks into your room
 (77,[(AI2,1.30,2.70,0.5)]),                            # Outside, capybaras soak in the pond,
 (83,[(R,62.05,1.25,0.5)]),                             # and you sleep in a villa
 (89,[(R,24.40,1.35,0.5)]),                             # in a bamboo forest
 (93,[(AI,1.50,1.20,0.5),(WAKE2,21.00,3.00,0.5)]),      # a night with breakfast here ... a thousand yuan
 (103,[(R,76.00,1.15,0.78),(G,27.92,2.10,0.30)]),       # That's about a tenth of Kenya.
 (109,[(R,0.05,1.15,0.40),(G,104.40,1.35,0.5),(B2,97.74,2.18,0.5)]),  # Comment giraffe
]
TAIL=1.3
TITLE=["KENYA vs CHINA","Giraffe Hotel"]; TAG="same breakfast, a tenth of the price"
LABELS=[("Huzhou, China",13),("Giraffe Manor",24),("2 calves born here",56),("animal wake-up call",63),("capybara",78)]
CARDS=[("the one in Kenya","$1,400+","a night, per person",6,13),
       ("here: 1 night + breakfast","¥1,000","about $140",93,103),
       ("Kenya $1,400+ vs China $140","1/10","the price",103,109)]
CTA=('Comment "GIRAFFE"',109)
