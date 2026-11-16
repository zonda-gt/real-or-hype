# v3, PICTURE FIRST: shots chosen for looks and ordered as a journey; narration was written afterwards, one short line per
# shot it describes, starting when that shot appears.  Times are in the ORIGINAL clips (20261115_HHMMSS.mp4).
# (id, clip, in, source_len, speed, audio[, zoom, crop_x_frac, crop_y_frac])
SEGS=[
 # hook
 ('a1','173008', 9.20,1.76,0.8,'amb'),   # him beside the cup, clean white room (hook text); steadiest pose, 0.8x
 # the way in
 ('a2','172149', 3.20,1.05,1.0,'amb'),   # glowing heytea sign at night
 ('a3','172149', 7.90,0.80,1.0,'amb'),   # walking in through the door
 ('a4','172620', 0.40,1.20,1.0,'amb',1.25,0.55,0.58),  # lamp-lit "new style tea" wall
 ('a5','172443', 8.90,1.70,1.0,'amb'),   # tilt up to the animated noodle-cup screen
 ('a6','172212', 0.00,1.40,1.0,'amb'),   # barista in a CUP HEYTEA chef hat
 ('r1','172355', 0.00,3.05,1.2,'real'),  # "We're in the shop now and we're going to give this a try."
 # order + made
 ('b1','172319', 0.00,1.30,1.0,'amb'),   # ordering on the kiosk
 ('b2','172923', 1.40,1.00,1.0,'amb'),   # barista pressing the lid on
 ('b3','172900', 2.20,2.00,1.0,'amb'),   # hero: slow push-in on the cup, steel counter
 # unboxing
 ('c1','173105', 3.20,3.60,2.0,'amb'),   # lifting the lid off -> the topping cup
 ('c2','173105',10.20,1.90,1.0,'amb'),   # overhead: mango noodles + corn
 ('c3','173105',21.20,1.70,1.0,'amb'),   # icy coconut underneath
 ('c4','173105',25.00,2.60,1.6,'amb'),   # pouring the noodles in
 ('c5','173149', 1.50,3.30,2.5,'amb'),   # stirring
 # tasting
 ('d1','173230', 2.40,1.80,1.0,'amb'),   # him raising the cup, warm-lit shelves
 ('r2','173230', 6.45,3.25,1.4,'real'),  # "First try." + first sip
 ('r3','173230',16.40,3.84,1.2,'real'),  # "You've got the coconut flavour and you've got the noodles inside."
 ('d2','173008', 0.20,1.90,1.0,'amb'),   # cup right up to the lens, his face behind
 ('d3','172950', 5.60,2.20,1.0,'amb'),   # lifts the cup up in front of his face
 ('r4','173230',23.50,1.45,1.1,'real'),  # "A different experience."
 ('d4','173230',24.95,2.45,0.86,'amb'),   # smiling with the cup in the mall (CTA)
]
# narration lines, each anchored to the shot it describes: (line, shot, offset)
VO=[('N1','a1',0.30),('N2','a2',0.05),('N3','a4',0.10),('N4','a6',0.05),
    ('N5','b1',0.05),('N6','b3',0.10),('N7','c1',0.05),('N8','c2',0.10),('N9','c3',0.05),('N10','c4',0.05),
    ('N11','d1',0.05),('N12','d2',0.10),('N13','d4',0.05)]
REAL={'r1':"We're in the shop now and we're going to give this a try.",'r2':'First try.',
      'r3':"You've got the coconut flavour and you've got the noodles inside.",'r4':'A different experience.'}
VOTXT={'N1':'Heytea just dropped a Cup Noodle drink,'}
WHOOSH=['a2','c1','d1']
HOOK=('a1',[0.15,0.55,0.95])
SPEECH={'r1':(0.05,2.79),'r2':(6.57,6.95),'r3':(16.62,20.08),'r4':(23.66,24.62)}
