# Heytea x Cup Noodle "Fresh Coconut Ramen" — shot list. Times are in the ORIGINAL clips (20261115_HHMMSS.mp4).
# (id, clip, in, source_len, speed, audio)  audio: 'amb' = room sound under narration, 'real' = his own line (loudnormed)
# Output length of a shot = source_len / speed.
SEGS=[
 ('o1','172900', 2.00,2.40,1.0,'amb'),   # HERO: slow push-in on the cup on the steel counter (hook text)
 ('o2','172149', 3.20,1.20,1.0,'amb'),   # glowing heytea sign at night
 ('o3','172149', 7.90,0.80,1.0,'amb'),   # walking in through the door
 ('o4','172620', 0.40,1.20,1.0,'amb',1.25,0.55,0.58),  # lamp-lit "new style tea" wall (zoom 1.25 to drop the ticker)
 ('o5','172443', 8.80,2.00,1.0,'amb'),   # tilt up to the animated noodle-cup screen
 ('r1','172355', 0.00,3.05,1.2,'real'),  # "We're in the shop now and we're going to give this a try."
 ('s4','172319', 0.00,1.45,1.0,'amb'),   # ordering on the kiosk
 ('s5','172212', 2.40,1.40,1.0,'amb'),   # bar with the blue screens, barista
 ('s6','172923', 1.40,1.20,1.0,'amb'),   # barista pressing the lid on
 ('s7','173105', 0.40,3.00,2.0,'amb'),   # peel the lid, lift the topping cup
 ('s8','173105',10.20,1.90,1.0,'amb'),   # mango noodles + corn close-up
 ('s9','173105',21.00,1.10,1.0,'amb'),   # icy coconut close-up
 ('s10','173105',25.00,2.60,1.6,'amb'),  # pour noodles in
 ('s11','173149', 1.00,4.00,2.5,'amb'),  # stir
 ('r2','173230', 6.45,3.25,1.3,'real'),  # "First try." + first sip
 ('r3','173230',16.40,3.84,1.2,'real'),  # "You've got the coconut flavour and you've got the noodles inside."
 ('s12','173230',10.40,2.70,1.0,'amb'),  # thinking about it
 ('s13','173008', 8.80,1.30,1.0,'amb'),  # cup close to camera
 ('s14','172950', 5.50,1.20,1.0,'amb'),  # cup fills the frame
 ('r4','173230',21.10,3.82,1.2,'real'),  # "It's something else. A different experience."
 ('s15','173230',25.15,2.25,1.0,'amb'),  # smiling with the cup (CTA)
]
# narration: (line, segment it starts on, offset into that segment)
VO=[('L1','o1',0.35),('L2','o4',0.10),('L3','s4',0.05),('L4','s7',0.05),('L5','s9',0.05),('L6','s12',0.10),('L7','s15',0.05)]
# his real lines (exact words for subtitles)
REAL={'r1':"We're in the shop now and we're going to give this a try.",'r2':'First try.',
      'r3':"You've got the coconut flavour and you've got the noodles inside.",'r4':"It's something else. A different experience."}
# subtitle text for narration (how it's spelled on screen; TTS text lives in vo/lines.json)
VOTXT={'L1':'Heytea just made a Cup Noodle drink, so of course I had to try it.'}
WHOOSH=['o2','s7','r2']   # whoosh into these shots
HOOK=('o1',[0.15,0.55,0.95])   # hook text on this shot; reveal times of k0,k1,k2 (fade+rise 0.45 s), fades out at the shot's end
# where his words start/end in the ORIGINAL clip (from the voiced-energy map), for the gap check
SPEECH={'r1':(0.05,2.79),'r2':(6.57,6.95),'r3':(16.62,20.08),'r4':(21.26,24.62)}
