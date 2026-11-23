SK='/home/user/real-or-hype/.claude/skills/china-spot-video'
G='7163077208322346248'   # glass bridge aerial (24 fps)
S='7363573672910523685'   # slide POV, covered + open sections
SHOTS=[
 (G,0.0,2.4,0.5),                          # aerial: glass bridge over the canyon
 (G,4.2,2.6,0.5),                          # bridge across the gorge
 ('7201300056480304445',1.6,3.0,0.5),     # slide POV from the top
 (S,3.0,3.0,0.5),                          # covered slide POV
 (S,19.0,3.0,0.5),                         # open curve with the cliffs
 ('7265469886720183586',19.5,2.5,0.5),    # rider ahead on the slide
 ('7605853255143617265',13.0,2.5,0.5),    # feet dangling over the canyon (zipline)
 (S,15.0,2.8,0.5),                         # bright section of the slide
 (G,7.0,2.6,0.5),                          # aerial: straight down the bridge
]
TEXTS=[("POV: your legs are done hiking\nso China gives you a slide",0.0,5.0),("Save this for your China trip",21.8,24.4)]
TEXT_SIZE=46
MUSIC=SK+'/work/music/zjjslide_cartoonchase.m4a'; MUSIC_IN=1.5
