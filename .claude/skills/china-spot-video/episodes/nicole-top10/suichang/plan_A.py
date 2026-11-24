SK='/home/user/real-or-hype/.claude/skills/china-spot-video'
T='7705003198705602240'   # shuttle train + shaft, clean vertical
D='7619136917221222001'   # 4K tour, small subtitles at the bottom
E='7673308983226368614'   # 1440p tour, small subtitles at the bottom
SRC={D:{'cut':0.12},E:{'cut':0.12},T:{'cut':0.11}}
SHOTS=[
 (T,0.0,3.5,0.5),        # the shuttle train inside the cave
 (T,8.0,3.0,0.5),        # the lit shaft going 200 m down
 (D,7.85,1.4,0.5),       # green-lit tunnel
 (D,11.0,2.5,0.5),       # red vault door
 (D,29.1,3.0,0.5),       # glowing particles in the mine
 (D,43.4,2.0,0.5),       # underground hot spring
 (E,37.8,1.3,0.5),       # blue cave pool
 (E,19.35,1.0,0.5),      # glowing tunnel
 (D,83.6,3.0,0.5),       # glowing veins on the rock
 (E,85.0,1.9,0.5),       # sparkling cave
]
TEXTS=[("POV: China turned an old mine into\na world 200 m underground",0.0,6.5),("Save this for your China trip",19.6,22.6)]
TEXT_SIZE=46
MUSIC=SK+'/work/music/suichang_underground.m4a'; MUSIC_IN=1.0
