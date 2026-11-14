# Version E: clips-first edit. Cuts land 0.10 s before the cue word (index into words.json).
B2='7653507861812628772'; G='7651132730540887336'; R='7653362319732886150'; V1='6819931162912509199'
CUT={B2:0.14,G:0.14,R:0.18,V1:0.0}
FPS60={B2,G}
# each cue: (word index where the shot starts, [(src, t_in, max_source_dur, x), ...] filled in order)
CUES=[
 (11,[(G,5.36,1.50,0.62)]),                        # Giraffe Manor -> entrance arch
 (16,[(G,9.88,1.55,0.50)]),                        # Huzhou, two hours from Shanghai -> drone over villas
 (22,[(B2,14.80,1.20,0.50)]),                      # restaurant
 (26,[(V1,12.0,3.0,0.5)]),                         # watch them walk across the field
 (32,[(R,77.20,1.68,0.72)]),                       # stops at your window
 (39,[(R,75.70,1.45,0.78)]),                       # pushes its whole head inside
 (44,[(G,17.12,1.14,0.48)]),                       # carrot
 (49,[(R,8.02,1.10,0.45),(B2,20.60,2.3,0.45)]),    # takes it right from your hand
 (56,[(B2,31.82,1.45,0.50),(B2,2.45,1.7,0.45)]),   # capybaras soak in the pond
 (62,[(B2,43.12,2.30,0.55)]),                      # raccoons
 (67,[(B2,28.48,1.24,0.48)]),                      # cranes in the mist
 (72,[(G,11.48,1.12,0.50)]),                       # villa
 (77,[(B2,78.48,1.32,0.50),(B2,7.08,1.05,0.50)]),  # middle of a bamboo forest
 (84,[(B2,0.30,2.04,0.60)]),                       # but here's the part nobody expects
 (90,[(B2,16.04,1.12,0.50),(V1,0.3,2.5,0.5)]),     # a night with breakfast ... a thousand yuan
 (99,[(B2,26.62,1.80,0.42),(G,27.92,2.10,0.30)]),  # Kenya over $1,400
 (105,[(G,25.80,2.08,0.33)]),                      # get there by 6:30 for a window table
 (114,[(B2,96.64,1.06,0.55),(B2,97.74,2.18,0.50)]),# follow -> kiss, aerial
]
COLLAGE=[(V1,0.0,3.3,0.5),(B2,0.30,2.04,0.60),(G,25.80,2.08,0.33),(G,9.88,1.55,0.50)]  # TL TR BL BR
TAIL=1.3   # video runs this long after the last word
LABELS=[('Giraffe Manor',11),('capybara',56),('raccoons',62),('red-crowned cranes',67),('6:30 AM',105)]
CARDS=[('price',90,99),('kenya',99,105)]
