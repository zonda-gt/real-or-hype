SK='/home/user/real-or-hype/.claude/skills/china-spot-video'
V='7602544090656702577'   # vertical 1440x2560 60fps, one subtitle line at y~0.667
A='7614451369328275782'; B='7665755738070276330'   # 3:4 POV clips, subtitle band y~0.47-0.55
BAND='delogo=x=4:y=668:w=1072:h=132'
SRC={A:{'pre':BAND},B:{'pre':BAND},V:{'cut':0.03}}
SHOTS=[
 (V,5.0,2.0,0.5),      # 0 twin racing slides with riders
 (V,0.0,1.35,0.5),     # 1 loop bike, wide
 (A,15.3,1.8,0.5),     # 2 loop bike POV
 (V,8.32,1.7,0.5),     # 3 magic carpet slide
 (A,10.95,2.3,0.5),    # 4 tube slide POV
 (A,6.98,2.1,0.5),     # 5 pillar challenge, top-down
 (V,11.66,1.3,0.5),    # 6 climbing wall
 (A,21.7,1.9,0.5),     # 7 spiral slide + net
 (V,1.4,1.7,0.5),      # 8 VR motorbikes
 (B,27.95,1.9,0.5),    # 9 motorbike racing game POV
 (V,3.15,1.8,0.5),     # 10 Formula racing area
 (V,14.6,1.5,0.5),     # 11 F1 sim pods
 (V,13.02,1.5,0.5),    # 12 slide matrix overview
 (V,10.05,1.6,0.5),    # 13 slides overview
]
import itertools
st=[0]+list(itertools.accumulate(s[2] for s in SHOTS))
def L(txt,i,j=None,y=0.688,w=880): return (txt,st[i],st[(j if j is not None else i)+1],y,'box',w)
Y2=0.514
TEXTS=[("POV: Shanghai has a 3-floor\nindoor playground for adults",0.0,st[2],0.2),
 L("Slide racing",0,w=1040),L("360° loop bike",1),L("360° loop bike",2,y=Y2,w=0),L("Magic carpet slide",3),L("Tube slide",4,y=Y2,w=0),
 L("Pillar challenge",5,y=Y2,w=0),L("Rock climbing",6),L("Spiral slide",7,y=Y2,w=0),L("VR motorbikes",8),L("Racing games",9,y=Y2,w=0),
 L("F1 simulators",10,11),L("100+ activities",12,13),("Save this for your Shanghai trip",st[12],st[14],0.2)]
TEXT_SIZE=46; LABEL_SIZE=54
MUSIC=SK+'/work/music/shplay_levelup.m4a'; MUSIC_IN=29.0
