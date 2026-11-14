# shot plans. shot = (src_id, t_in, out_dur, {x: crop centre 0-1, y, zoom, speed})
# sources (Douyin originals via TikHub). Burned-in subtitles at the bottom -> 'cut'.
B2='7653507861812628772'   # 4K60 vlog (breakfast, capybara, villa room, aerial)
G='7651132730540887336'    # 4K60 vlog (entrance arch, drone villas, carrot at window)
R='7653362319732886150'    # 4K30 vlog (POV carrot, giraffes at restaurant)
V1='6819931162912509199'   # vertical 720p breakfast restaurant
BABY='7673338456038363624' # vertical baby giraffe (keeper)
SKY='7706044234537230691'  # vertical giraffe vs sky
SRC={B2:{'cut':0.14},G:{'cut':0.14},R:{'cut':0.18},V1:{},BABY:{},SKY:{}}
HOOK=[(R,75.70,1.45,{'x':0.78}),(R,77.20,1.65,{'x':0.72})]
MANWIN=(B2,0.92,1.7,{'x':0.6,'speed':0.8})
ARCH=(G,5.40,1.45,{'x':0.62}); DRONE=(G,9.90,1.5,{'x':0.5}); VILLA=(G,11.50,1.1,{'x':0.5})
WINDOW2=(R,77.20,1.6,{'x':0.45}); WOMEN=(G,26.0,1.8,{'x':0.33})
CARROT=(G,17.12,1.15,{'x':0.48}); POV=(R,8.02,1.36,{'x':0.45}); TABLE=(B2,26.65,1.7,{'x':0.42})
CAPY=(B2,31.82,1.3,{'x':0.5}); RACC=(B2,43.12,1.2,{'x':0.55}); CRANE=(B2,28.48,1.2,{'x':0.48})
ROOM=(B2,78.50,1.3,{'x':0.5}); REST=(B2,14.80,1.2,{'x':0.5}); KISS=(B2,96.65,1.05,{'x':0.55}); AER=(B2,97.75,2.15,{'x':0.5})
VERT=(V1,0.3,1.8)
VARIANTS={
 'A':{'lead':{'A1':0.05},'slots':[
   ('A1',HOOK),
   ('A2',[ARCH,DRONE,(B2,97.75,1.2,{'x':0.5})]),
   ('A3',[MANWIN,WOMEN]),
   ('A4',[CARROT,TABLE]),
   ('A5',[CAPY,RACC,CRANE]),
   ('A6',[VILLA,ROOM]),
   ('A7',[REST,(V1,0.3,2.35),(G,19.6,1.4,{'x':0.33})]),
   ('A8',[POV,KISS,AER]),
  ]},
 'B':{'slots':[
   ('B1',[(SKY,0.0,2.0),(BABY,15.3,2.8)]),
   ('B2',[DRONE,ARCH]),
   ('B3',[(R,77.20,1.65,{'x':0.72}),(B2,0.92,1.35,{'x':0.6})]),
   ('B4',[CARROT,POV]),
   ('B5',[VILLA,ROOM,CAPY,RACC]),
   ('B6',[REST,VERT,WOMEN]),
   ('B7',[KISS,AER]),
  ]},
 'C':{'lead':{'C1':0.05},'slots':[
   ('C1',HOOK),
   ('C2',[ARCH,(G,9.90,1.6,{'x':0.5})]),
   ('C3',[(B2,37.85,1.45,{'x':0.5}),(B2,97.75,1.2,{'x':0.5})]),
   ('C4',[(G,12.65,1.3,{'x':0.5}),ROOM,REST]),
   ('C5',[CARROT,POV]),
   ('C6',[REST,(R,75.70,1.45,{'x':0.78}),(V1,12.6,1.4)]),
   ('C7',[KISS,AER]),
  ]},
}
