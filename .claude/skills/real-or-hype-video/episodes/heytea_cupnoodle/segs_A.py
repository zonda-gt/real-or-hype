# Variant A, "I had to try this": personal story in the reference's voice (setup -> disbelief -> shop -> reveal ->
# soup or drink? -> taste -> verdict -> follow). SCRIPT FIRST; each line then matched to the shot that fits it.
SEGS=[
 ('a1','173008', 9.20,1.76,0.8,'amb'),   # him beside the cup                     A1 "Heytea just turned Cup Noodles into a drink."
 ('a2','172149', 3.20,1.75,1.0,'amb'),   # neon sign at night (A1 continues)
 ('a3','172149', 7.90,0.80,1.0,'amb'),   # walking in                             A2 "I honestly thought it was a joke."
 ('a4','172620', 0.40,0.95,1.0,'amb',1.25,0.55,0.58),  # lamp wall
 ('a5','172443', 8.90,2.50,1.0,'amb'),   # animated noodle-cup screen             A3 "Nope. Some shops sold out in minutes."
 ('a6','172212', 0.00,1.90,1.0,'amb'),   # CUP HEYTEA chef hat                    A4 "Even the staff wear noodle chef hats!"
 ('r1','172355', 0.00,3.05,1.3,'real'),  # his line
 ('b1','172319', 0.00,1.85,1.0,'amb'),   # kiosk                                  A5 "Fresh Coconut Ramen. Twenty-two yuan."
 ('b2','172923', 1.40,1.00,1.0,'amb'),   # lid pressed on (A5 continues)
 ('b3','172900', 2.20,2.20,1.0,'amb'),   # hero cup on steel counter              A6 "Looks exactly like the real thing, right?"
 ('c1','173105', 3.20,4.10,2.0,'amb'),   # lid lifted off                         A7 "Plot twist: the lid is the noodles."
 ('c2','173105',10.20,1.90,1.0,'amb'),   # overhead noodles + corn                A8 "Mango noodles, and real corn."
 ('c3','173105',21.20,2.00,1.0,'amb'),   # icy coconut                            A9 "And underneath? Icy coconut."
 ('c4','173105',25.00,2.20,1.6,'amb'),   # pour                                   A10 "Dump it in, stir it up..."
 ('c5','173149', 1.50,2.30,2.5,'amb'),   # stir
 ('d1','173230', 2.40,2.50,1.0,'amb'),   # raises the cup                         A11 "Moment of truth. Soup, or drink?"
 ('r2','173230', 6.45,3.25,1.6,'real'),  # "First try." + sip
 ('r3','173230',16.40,3.84,1.3,'real'),  # coconut flavour line
 ('d2','173008', 0.20,1.90,1.0,'amb'),   # cup to the lens                        A12 "Sweet, icy, and honestly? It works."
 ('d3','172950', 5.60,1.00,1.0,'amb'),   # lifts the cup in front of his face
 ('r4','173230',23.50,1.45,1.1,'real'),  # "A different experience."
 ('d4','173230',24.95,1.95,0.86,'amb'),  # smiling in the mall                    A13 "Follow for more weird food in China!"
]
VO=[('A1','a1',0.30),('A2','a3',0.05),('A3','a5',0.05),('A4','a6',0.05),('A5','b1',0.05),('A6','b3',0.05),
    ('A7','c1',0.05),('A8','c2',0.10),('A9','c3',0.05),('A10','c4',0.05),('A11','d1',0.05),('A12','d2',0.10),('A13','d4',0.05)]
REAL={'r1':"We're in the shop now and we're going to give this a try.",'r2':'First try.',
      'r3':"You've got the coconut flavour and you've got the noodles inside.",'r4':'A different experience.'}
VOTXT={'A1':'Heytea just turned Cup Noodles into a drink.'}
WHOOSH=['a2','c1','d1']
HOOK=('a1',[0.15,0.55,0.95])
HOOKTXT=('HEYTEA  ×  CUP NOODLES','a cup noodle','you drink?')
SPEECH={'r1':(0.05,2.79),'r2':(6.57,6.95),'r3':(16.62,20.08),'r4':(23.66,24.62)}
