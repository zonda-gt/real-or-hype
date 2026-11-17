# Variant N, "Would you drink a cup of noodles?": a DIFFERENT CUT from O (creator: B must not look like the same video).
# Opens on the overhead noodles, shop shown via neon sign -> queue -> screen, ordering adds the chef hat, reveal goes
# hero cup -> lid -> noodles in the lid, verdict comes BEFORE his coconut line, ends on him lifting the cup to his face.
SEGS=[
 ('n1','173105',10.20,1.50,1.0,'amb'),   # overhead noodles + corn (hook)          L1 "Would you drink a cup of noodles?
 ('n2','173008', 9.20,1.76,0.8,'amb'),   # him beside the cup                       ...Because Heytea just made one!"
 ('n3','172149', 3.20,1.20,1.0,'amb'),   # neon sign at night                       L2 "It's their new collab with Cup Noodles,
 ('n4','172539', 0.30,1.40,1.0,'amb'),   # people waiting in the shop               ...and people are lining up for it."
 ('n5','172443', 8.90,1.60,1.0,'amb'),   # animated noodle-cup screen
 ('r1','172355', 0.00,3.05,1.3,'real'),  # "We're in the shop now and we're going to give this a try."
 ('n6','172319', 0.00,1.30,1.0,'amb'),   # kiosk                                    L3 "You order the Fresh Coconut Ramen. Twenty-two yuan."
 ('n7','172212', 0.00,1.00,1.0,'amb'),   # CUP HEYTEA chef hat
 ('n8','172923', 1.40,1.00,1.0,'amb'),   # lid pressed on
 ('n9','172900', 2.20,1.60,1.0,'amb'),   # hero cup on the counter                  L4 "The noodles come in the lid.
 ('n10','173105', 3.20,3.60,2.0,'amb'),  # lid lifted off
 ('n11','173105', 7.00,1.00,1.0,'amb'),  # noodles sitting in the lid               ...Mango noodles, with corn!"
 ('n12','173105',22.00,1.50,1.0,'amb'),  # icy coconut, closer                      L5 "Underneath is icy coconut, so you pour it all in and mix."
 ('n13','173105',25.00,2.20,1.6,'amb'),  # pour
 ('n14','173149', 5.00,3.00,2.5,'amb'),  # stir, later and creamier
 ('n15','173230', 2.40,0.80,1.0,'amb'),  # raises the cup
 ('r2','173230', 6.45,3.25,1.6,'real'),  # "First try." + sip
 ('n16','173230',10.40,2.80,1.0,'amb'),  # thinking about it                        L6 "It's sweet, not savory. Basically a mango coconut slush, shaped like ramen."
 ('n17','173008', 0.20,2.00,1.0,'amb'),  # cup right up to the lens
 ('n18','173008', 3.00,1.20,1.0,'amb'),  # cup tilted at the lens
 ('r3','173230',16.40,3.84,1.3,'real'),  # "You've got the coconut flavour and you've got the noodles inside."
 ('r4','173230',21.10,3.82,1.2,'real'),  # "It's something else. A different experience."
 ('n19','172950', 5.40,2.40,1.0,'amb'),  # lifts the cup up to his face (CTA)       L7 "Would you try it? Tell me in the comments!"
]
VO=[('L1','n1',0.10),('L2','n3',0.05),('L3','n6',0.05),('L4','n9',0.05),('L5','n12',0.05),('L6','n16',0.10),('L7','n19',0.05)]
REAL={'r1':"We're in the shop now and we're going to give this a try.",'r2':'First try.',
      'r3':"You've got the coconut flavour and you've got the noodles inside.",'r4':"It's something else. A different experience."}
VOTXT={'L1':'Would you drink a cup of noodles? Because Heytea just made one!'}
WHOOSH=['n3','n10','r2']
HOOK=('n1',[0.15,0.55,0.95],'n2')
HOOKTXT=('HEYTEA  ×  CUP NOODLES','would you drink','cup noodles?')
SPEECH={'r1':(0.05,2.79),'r2':(6.57,6.95),'r3':(16.62,20.08),'r4':(21.26,24.62)}
