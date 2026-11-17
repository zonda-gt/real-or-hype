# Variant B, "3 things to know before you order": opens on the noodles (most surprising image), numbered tips with
# on-screen labels, ends on "save this". SCRIPT FIRST; each line then matched to the shot that fits it.
SEGS=[
 ('h1','173105',10.20,2.20,1.0,'amb'),   # overhead noodles + corn (hook)        B1 "These noodles... are actually a drink."
 ('a1','173008', 9.20,1.76,0.8,'amb'),   # him beside the cup                     B2 "It's Heytea's Cup Noodle collab. Three things to know before you order."
 ('a2','172149', 3.20,1.15,1.0,'amb'),   # neon sign
 ('a3','172149', 7.90,0.80,1.0,'amb'),   # walking in
 ('t1','172539', 0.30,1.40,1.0,'amb'),   # people waiting in the shop             B3 [No.1] "One: go early. Some shops sold out in minutes."
 ('a5','172443', 8.90,2.00,1.0,'amb'),   # animated noodle-cup screen
 ('r1','172355', 0.00,3.05,1.2,'real'),  # his line
 ('b1','172319', 0.00,1.30,1.0,'amb'),   # kiosk                                  B4 "Ask for Fresh Coconut Ramen. It's twenty-two yuan."
 ('a6','172212', 0.00,1.10,1.0,'amb'),   # CUP HEYTEA chef hat
 ('b3','172900', 2.20,1.40,1.0,'amb'),   # hero cup
 ('c1','173105', 3.20,3.60,2.0,'amb'),   # lid lifted off                         B5 [No.2] "Two: don't sip it yet. The lid is the noodles."
 ('c2','173105', 7.00,1.40,1.0,'amb'),   # noodle cup sitting on top
 ('c3','173105',21.20,1.30,1.0,'amb'),   # icy coconut                            B6 "Pour them into the icy coconut, and stir."
 ('c4','173105',25.00,2.00,1.6,'amb'),   # pour
 ('c5','173149', 1.50,2.30,2.5,'amb'),   # stir
 ('d1','173230', 2.40,1.80,1.0,'amb'),   # raises the cup                         B7 [No.3] "Three: it's not savory. At all."
 ('r2','173230', 6.45,3.25,1.4,'real'),  # "First try." + sip
 ('r3','173230',16.40,3.84,1.2,'real'),  # coconut flavour line
 ('d2','173008', 0.20,1.90,1.0,'amb'),   # cup to the lens                        B8 "It's mango and coconut... shaped like ramen."
 ('d3','172950', 5.60,1.60,1.0,'amb'),   # lifts the cup
 ('r4','173230',23.50,1.45,1.1,'real'),  # "A different experience."
 ('d4','173230',24.95,2.10,0.86,'amb'),  # smiling in the mall                    B9 "Save this for your China trip!"
]
VO=[('B1','h1',0.25),('B2','a1',0.05),('B3','t1',0.05),('B4','b1',0.05),('B5','c1',0.05),('B6','c3',0.05),
    ('B7','d1',0.05),('B8','d2',0.10),('B9','d4',0.05)]
REAL={'r1':"We're in the shop now and we're going to give this a try.",'r2':'First try.',
      'r3':"You've got the coconut flavour and you've got the noodles inside.",'r4':'A different experience.'}
VOTXT={'B2':"It's Heytea's Cup Noodle collab. Three things to know before you order."}
WHOOSH=['a1','c1','d1']
HOOK=('h1',[0.10,0.50,0.90])
HOOKTXT=('HEYTEA  ×  CUP NOODLES','these noodles','are a drink.')
OVL=[('tip1.png','t1',0.05,3.0),('tip2.png','c1',0.05,3.1),('tip3.png','d1',0.05,1.75)]
SPEECH={'r1':(0.05,2.79),'r2':(6.57,6.95),'r3':(16.62,20.08),'r4':(23.66,24.62)}
