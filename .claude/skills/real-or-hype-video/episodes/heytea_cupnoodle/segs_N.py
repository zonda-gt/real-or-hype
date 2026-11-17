# Variant N: same cut and plain pacing as v1, new direction: 'Would you drink a cup of noodles?' + comment CTA.
# Heytea x Cup Noodle "Fresh Coconut Ramen" — shot list. Times are in the ORIGINAL clips (20261115_HHMMSS.mp4).
# (id, clip, in, source_len, speed, audio)  audio: 'amb' = room sound under narration, 'real' = his own line (loudnormed)
# Output length of a shot = source_len / speed.
SEGS=[
 ('h1','173008', 4.20,1.90,1.0,'amb'),   # cup beside his face (hook)
 ('h2','172443', 9.00,1.95,1.0,'amb'),   # big product screen
 ('s1','172149', 1.00,1.50,1.0,'amb'),   # heytea storefront
 ('s2','172443', 0.50,1.30,1.0,'amb'),   # CUP HEYTEA menu screens
 ('s3','172539', 0.30,1.40,1.0,'amb'),   # people waiting
 ('r1','172355', 0.00,3.05,1.2,'real'),  # "We're in the shop now and we're going to give this a try."
 ('s4','172319', 0.00,1.85,1.0,'amb'),   # ordering on the kiosk
 ('s6','172923', 0.20,1.45,1.0,'amb'),   # staff putting the lid on
 ('s7','173105', 0.40,3.50,2.0,'amb'),   # peel the lid, lift the topping cup
 ('s8','173105',10.20,2.20,1.0,'amb'),   # mango noodles + corn close-up
 ('s9','173105',21.00,1.10,1.0,'amb'),   # icy coconut close-up
 ('s10','173105',25.00,2.60,1.6,'amb'),  # pour noodles in
 ('s11','173149', 1.00,4.00,2.5,'amb'),  # stir
 ('r2','173230', 6.45,3.25,1.5,'real'),  # "First try." + first sip
 ('r3','173230',16.40,3.84,1.2,'real'),  # "You've got the coconut flavour and you've got the noodles inside."
 ('s12','173230',10.40,2.80,1.0,'amb'),  # thinking about it
 ('s13','173008', 8.80,1.30,1.0,'amb'),  # cup close to camera
 ('s14','172950', 5.50,1.70,1.0,'amb'),  # cup fills the frame
 ('r4','173230',21.10,3.82,1.2,'real'),  # "It's something else. A different experience."
 ('s15','173230',25.00,2.40,0.95,'amb'),  # smiling with the cup (CTA)
]
# narration: (line, segment it starts on, offset into that segment)
VO=[('L1','h1',0.10),('L2','s1',0.05),('L3','s4',0.05),('L4','s7',0.05),('L5','s9',0.05),('L6','s12',0.10),('L7','s15',0.05)]
# his real lines (exact words for subtitles)
REAL={'r1':"We're in the shop now and we're going to give this a try.",'r2':'First try.',
      'r3':"You've got the coconut flavour and you've got the noodles inside.",'r4':"It's something else. A different experience."}
# subtitle text for narration (how it's spelled on screen; TTS text lives in vo/lines.json)
VOTXT={'L1':'Would you drink a cup of noodles? Because Heytea just made one!'}
WHOOSH=['s1','s7','r2']   # whoosh into these shots
HOOK=('h1',[0.15,0.55,0.95],'h2')   # serif hook text over h1+h2
# where his words start/end in the ORIGINAL clip (from the voiced-energy map), for the gap check
SPEECH={'r1':(0.05,2.79),'r2':(6.57,6.95),'r3':(16.62,20.08),'r4':(21.26,24.62)}

HOOKTXT=('HEYTEA  ×  CUP NOODLES','would you drink','cup noodles?')
