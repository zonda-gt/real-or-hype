SK='/home/user/real-or-hype/.claude/skills/china-spot-video'
W='7367226032841100607'   # window-open reveal (720p)
L='7468645993622310179'   # laser aerial (720p)
SHOTS=[
 (W,1.5,3.0,0.5),                           # pushing the window open
 (W,4.6,2.5,0.5),                           # the lit-up stilted tower
 (L,1.0,3.0,0.5),                           # aerial: lasers through the giant opening
 ('7655192870329411995',0.0,3.0,0.5),      # aerial: facade + lasers
 ('7312389772016749833',12.0,3.0,0.5),     # the 109.9 m tower from below
 ('7700602940461844326',1.0,2.5,0.5),      # crowd dancing in front of the tower
 ('7655192870329411995',9.0,3.0,0.5),      # night show in front of the tower
 (L,14.0,4.0,0.5),                          # aerial pull-back
]
TEXTS=[("POV: you open a window in\nZhangjiajie and see this",0.0,5.5),("Save this for your China trip",20.0,24.0)]
TEXT_SIZE=46
MUSIC=SK+'/work/music/qilou_dragon.m4a'; MUSIC_IN=11.0
