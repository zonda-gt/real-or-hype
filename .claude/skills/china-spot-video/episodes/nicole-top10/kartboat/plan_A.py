SK='/home/user/real-or-hype/.claude/skills/china-spot-video'
D='7661114647312069105'   # Fenglin Gorge drone (HLG, 60 fps)
SHOTS=[
 ('7656219080009629033',0.0,2.3,0.5),        # POV yellow kart under the start gate, mountains
 (D,43.5,1.9,0.5),                            # aerial: emerald gorge
 ('7651857177070362751',2.4,3.0,0.5),         # POV pink kart, spray, buoy lanes
 ('7648069951043428678',13.6,2.5,0.5),        # chase cam: pink kart on green water
 ('7656219080009629033',11.55,1.8,0.45),      # kart racing past, canyon walls
 ('7653638867400219374',3.0,2.8,0.5),         # rider laughing through the spray
 ('7648069951043428678',5.95,1.5,0.5),         # POV hands on the wheel, spray
 ('7656219080009629033',5.9,2.8,0.5),         # POV yellow kart down the gorge
 ('7661427104446013695',4.0,4.8,0.5),         # POV wide gorge, buoy lane
 (D,52.2,3.0,0.5,0.6),                        # aerial: winding green gorge (slowed)
]
TEXTS=[("POV: you're racing go-kart boats\nthrough a canyon in China",0.0,7.2),("Save this for your China trip",23.4,26.4)]
TEXT_SIZE=46
MUSIC=SK+'/work/music/kartboat_gottagofaster.m4a'; MUSIC_IN=12.5
