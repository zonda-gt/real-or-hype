# Version G: "4 things nobody tells you". New edit: mostly unused clips, new order. Voice: John.
B2='7653507861812628772'; G='7651132730540887336'; R='7653362319732886150'
WAKE='7702806207996158385'; AI='ai_me_breakfast'; AI2='ai_me_capybara'
WAKE2='7685311414965524923'   # 1080x1440: giraffe among diners 12.83-17.13, outside restaurant 5.93-8.77, at window w/ kid 17.13-24.8
BKF='6976808703164992805'     # 720p: giraffe face at the glass 7-11
BIRTH='7650310001970073807'   # 4K: newborn with mother 18.70-21.96, 28.48-31.5 (subs + logo bottom right)
WINTER='7604799138752724410'  # 1080p winter vlog: arch 7.53-10.63, snow cabin 27.80-29.07, indoor giraffe house 47.0-49.73, breakfast 61.27-63.63, drone 63.63-
CALF2='7653265250729437775'   # vertical: calf standing in giraffe house 0-4, keeper petting 7.5-10.5
SRC={B2:{'cut':0.14},G:{'cut':0.14},R:{'cut':0.18},WAKE:{},AI:{},AI2:{},WAKE2:{},BKF:{},BIRTH:{'cut':0.14},WINTER:{'cut':0.19},CALF2:{}}
COLLAGE=[(WAKE2,13.0,3.9,0.5),(BKF,7.0,3.9,0.62),(CALF2,7.4,3.0,0.5),(G,101.30,1.60,0.5)]
CUES=[
 (9, [(WAKE2,6.00,2.70,0.5)]),                       # One: the giraffes come to the restaurant windows
 (17,[(AI,0.05,1.45,0.5)]),                          # at breakfast (you look up)
 (19,[(BKF,7.00,1.50,0.60),(WAKE2,17.20,3.0,0.5)]),  # get there by 6:30 for a window seat
 (29,[(WAKE,10.05,2.50,0.5)]),                       # Two: book an animal wake-up call
 (38,[(WAKE,18.55,2.40,0.5)]),                       # sometimes a raccoon walks into your room
 (45,[(BIRTH,19.90,2.00,0.42)]),                     # Three: giraffes are born here
 (50,[(BIRTH,28.55,2.95,0.45)]),                       # the first one was over six feet tall on day one
 (61,[(WINTER,27.85,1.20,0.5),(B2,29.75,2.0,0.5)]),  # Four: on cold, rainy days
 (66,[(WINTER,47.65,2.05,0.40)]),                    # the giraffes may stay inside
 (71,[(B2,4.22,1.25,0.5)]),                          # so go when it's warm
 (76,[(WINTER,7.60,2.50,0.55),(WINTER,63.70,2.9,0.5)]),  # It's called Giraffe Manor in Huzhou, two hours from Shanghai
 (86,[(AI,1.50,1.20,0.5),(WINTER,61.30,2.30,0.75)]), # a night with breakfast ... a thousand yuan
 (96,[(AI2,1.30,1.40,0.5),(B2,97.74,2.18,0.5)]),     # comment giraffe
]
TAIL=1.3
TITLE=["4 THINGS","nobody tells you"]; TAG="China's giraffe hotel"
LABELS=[("#1 breakfast at the window",9),("be there by 6:30 AM",21),("#2 animal wake-up call",29),("#3 born here",45),("#4 cold days",61),("Giraffe Manor, Huzhou",76)]
CARDS=[("the first one","6 ft 1 in","(1.85 m) at birth",50,61),("1 night + breakfast","¥1,000","about $140",86,96)]
CTA=('Comment "GIRAFFE"',96)
