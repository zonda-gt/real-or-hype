import os,json,math
D=os.getcwd(); A=f'file://{D}/a'; O=f'file://{D}/out'
P=json.load(open('tools/places.json')); BR='#FF5A36'; Y='#FFD43B'
HEAD=f"""<!doctype html><html><head><meta charset=utf-8><link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@900&display=swap" rel=stylesheet><style>
@font-face{{font-family:MX;src:url({A}/Montserrat-ExtraBold.ttf)}}*{{box-sizing:border-box;margin:0;padding:0}}
body{{width:1080px;height:1920px;overflow:hidden;position:relative;font-family:Inter,sans-serif;background:#000}}
.L{{position:absolute;inset:0}}.bg{{background-size:cover;background-position:center}}.cut{{position:absolute;inset:0;width:1080px;height:1920px}}
.cap{{position:absolute;left:0;right:0;top:1440px;text-align:center;font-family:MX;color:#fff;text-shadow:0 4px 18px #000b,0 0 3px #000a}}
.cap .s{{font-size:56px;letter-spacing:-.01em}}.cap .k{{font-size:96px;white-space:nowrap;color:{Y};line-height:1.02;letter-spacing:-.02em}}
.rc{{position:absolute;border-radius:22px;overflow:hidden;background-size:cover;background-position:center;box-shadow:0 18px 40px #0006;border:5px solid #fff}}
.rc .v{{position:absolute;left:12px;bottom:10px;color:#fff;font:700 24px Inter;text-shadow:0 2px 6px #000}}
"""
def cap(s,k): return f'<div class=cap><div class=s>{s}</div><div class=k>{k}</div></div>'
def page(n,css,body):
    p=f'{D}/html/f_{n}.html'; open(p,'w').write(HEAD+css+'</style></head><body>'+body+'</body></html>'); return dict(html=p,w=1080,h=1920,s=1,out=f'{D}/out/frame_{n}.png')
J=[]
def card(p,x,y,w,rot=0,z=1,extra=''):
    return f'<div class=rc style="left:{x}px;top:{y}px;width:{w}px;height:{int(w*1.5)}px;transform:rotate({rot}deg);z-index:{z};background-image:url({A}/{p[0]}.jpg);{extra}"><span class=v>▶ {p[2]}</span></div>'
# 1 couch wall
pos=[(30,120,190,-6),(250,40,170,4),(690,60,180,-3),(880,190,170,7),(20,560,180,5),(860,560,190,-5),(130,330,160,-2),(760,340,150,3),(450,-20,170,-4)]
wall=''.join(card(P[i],x,y,w,r) for i,(x,y,w,r) in enumerate(pos))
J.append(page('01_couchwall','',f'<div class="L bg" style="background-image:url({A}/bg_me_talk.jpg)"></div>{wall}<img class=cut src="{A}/cut_me_talk.png">'+cap("you've saved","hundreds of reels")))
# 2 orbit
back,front='',''
for i in range(10):
    a=2*math.pi*i/10+0.3; x=540+470*math.cos(a); yv=980+150*math.sin(a); depth=(math.sin(a)+1)/2
    w=int(130+90*depth); h=int(w*1.5); el=f'<div class=rc style="left:{x-w/2:.0f}px;top:{yv-h/2:.0f}px;width:{w}px;height:{h}px;transform:rotate({math.cos(a)*-12:.0f}deg) perspective(800px) rotateY({math.cos(a)*35:.0f}deg);background-image:url({A}/{P[i][0]}.jpg);opacity:{0.75+0.25*depth:.2f};filter:blur({(1-depth)*2:.1f}px)"></div>'
    if math.sin(a)>0: front+=el
    else: back+=el
J.append(page('02_orbit','',f'<div class="L bg" style="background-image:url({A}/bg_me_talk.jpg)"></div>{back}<img class=cut src="{A}/cut_me_talk.png">{front}'+cap('rooftop bars, dumpling spots,','that café…')))
# 3 vertigo
J.append(page('03_vertigo','',f'<div class="L bg" style="background-image:url({A}/room.jpg);transform:scale(1.4);filter:blur(2.5px)"></div><img class=cut src="{A}/cut_me_talk.png">'+cap("and you've been to","none of them.")))
# 4 UI world
fly=f'<div class=rc style="left:90px;top:330px;width:200px;height:300px;transform:rotate(-14deg);background-image:url({A}/{P[4][0]}.jpg);box-shadow:-60px 30px 50px #0005"></div><div style="position:absolute;left:40px;top:560px;width:300px;height:14px;border-radius:7px;background:linear-gradient(90deg,transparent,#fff9);transform:rotate(-30deg)"></div>'
phone=f'<img src="{O}/screen_dm_sending.png" style="position:absolute;left:610px;top:120px;width:420px;border-radius:46px;border:8px solid #111;box-shadow:0 30px 80px #0008;transform:perspective(1400px) rotateY(-14deg) rotateZ(3deg)">'
J.append(page('04_uiworld','',f'<div class="L bg" style="background-image:url({A}/bg_me_talk.jpg)"></div><img class=cut src="{A}/cut_me_talk.png">{phone}{fly}'+cap('so just send them','all to us')))
# 5 checklist
items=[('Save the reel',1),('Send it to @steven_chinapal',1),('Get your trip',0)]
li=''.join(f'<div style="display:flex;align-items:center;gap:26px;padding:20px 0;font:700 46px Inter;color:{"#fff" if d else "#ffffff88"}"><span style="width:56px;height:56px;border-radius:50%;display:grid;place-items:center;font-size:34px;{"background:"+BR if d else "border:4px solid #ffffff66"}">{"✓" if d else ""}</span>{t}</div>' for t,d in items)
panel=f'<div style="position:absolute;left:90px;top:150px;width:900px;padding:36px 48px;border-radius:40px;background:#16161acc;backdrop-filter:blur(24px);border:2px solid #ffffff22;box-shadow:0 30px 80px #0007"><div style="display:flex;justify-content:space-between;font:700 30px Inter;letter-spacing:.12em;color:#ffffffaa;margin-bottom:10px"><span>ALL YOU NEED TO DO</span><span>2 of 3</span></div>{li}</div>'
J.append(page('05_checklist','',f'<div class="L bg" style="background-image:url({A}/bg_me_talk.jpg)"></div><img class=cut src="{A}/cut_me_talk.png">{panel}'))
# 6 pull-back reveal
steps=[("Watched your 10 reels",1),("Found 10 places",1),("Grouped them by area",1),("Checking opening hours",0),("Building 3 days",0)]
st=''.join(f'<div style="display:flex;gap:18px;align-items:center;font:600 34px Inter;color:{"#1d1d1f" if d else "#a5a5aa"};padding:9px 0"><span style="width:40px;height:40px;border-radius:50%;display:grid;place-items:center;color:#fff;font-size:22px;{"background:"+BR if d else "border:3px solid #cfcac1"}">{"✓" if d else ""}</span>{s}</div>' for s,d in steps)
strip=''.join(f'<div style="width:150px;height:210px;border-radius:18px;background:url({A}/{q[0]}.jpg) center/cover"></div>' for q in P[:5])
win=f'''<div style="position:absolute;inset:0;background:#E9E4DA"></div><div style="position:absolute;left:70px;top:270px;width:940px;height:1560px;border-radius:40px;background:#FAF8F4;box-shadow:0 40px 100px #0003;overflow:hidden">
<div style="height:70px;display:flex;align-items:center;gap:14px;padding:0 30px;border-bottom:2px solid #eee"><i style="width:18px;height:18px;border-radius:50%;background:#ff5f57"></i><i style="width:18px;height:18px;border-radius:50%;background:#febc2e"></i><i style="width:18px;height:18px;border-radius:50%;background:#28c840"></i><span style="margin-left:20px;font:600 26px Inter;color:#888">ChinaPal · building your trip</span></div>
<div style="margin:30px;height:760px;border-radius:28px;background-image:url({A}/bg_me_talk.jpg);background-size:cover;background-position:center 35%"></div>
<div style="padding:0 50px">{st}<div style="margin-top:26px;height:20px;border-radius:10px;background:#e6e1d8;overflow:hidden"><i style="display:block;height:100%;width:62%;background:{BR}"></i></div><div style="display:flex;gap:16px;margin-top:40px">{strip}</div></div></div>
<div style="position:absolute;left:60px;top:30px;font:900 190px Inter;letter-spacing:-.05em;color:#1d1d1f">62%</div>'''
J.append(page('06_pullback','',win))
# 7 route grow
pins=[(90,640),(260,470),(470,330),(660,390),(870,470),(985,680)]
d='M'+' L'.join(f'{x},{y}' for x,y in pins)
idx=[0,6,1,5,8,2]
svg=f'<svg class=L width=1080 height=1920><path d="{d}" stroke="{BR}" stroke-width=12 fill=none stroke-dasharray="26 18" stroke-linecap="round"/></svg>'
pn=''.join(f'<div style="position:absolute;left:{x-60}px;top:{y-190}px;width:120px;height:170px;border-radius:16px;border:5px solid #fff;background:url({A}/{P[idx[i]][0]}.jpg) center/cover;box-shadow:0 10px 30px #0005"></div><div style="position:absolute;left:{x-28}px;top:{y-28}px;width:56px;height:56px;border-radius:50%;background:{BR};border:5px solid #fff;display:grid;place-items:center;font:800 26px Inter;color:#fff">{i+1}</div>' for i,(x,y) in enumerate(pins))
lab=f'<div style="position:absolute;left:60px;top:60px;font:800 44px Inter;color:#fff;background:#1d1d1f;padding:12px 28px;border-radius:40px">DAY 1</div>'
J.append(page('07_routegrow','',f'<div class="L bg" style="background-image:url({A}/bg_me_point.jpg)"></div>{svg}{pn}{lab}<img class=cut src="{A}/cut_me_point.png">'+cap('built around','your reels')))
# 9 cover story
J.append(page('09_coverstory','',f'<div class="L bg" style="background-image:url({A}/bg_me_talk.jpg)"></div><div style="position:absolute;left:0;right:0;top:250px;text-align:center;font:900 250px \'Playfair Display\',serif;color:#fff;letter-spacing:.02em;line-height:.9;text-shadow:0 10px 40px #0003">YOUR<br>TRIP</div><img class=cut src="{A}/cut_me_talk.png">'))
# 10 frame break
icons=''.join(f'<div style="font:600 30px Inter;color:#fff;text-align:center;margin-bottom:34px;text-shadow:0 2px 8px #000"><div style="font-size:56px">{i}</div>{n}</div>' for i,n in [('♡','12.4K'),('💬','1,024'),('➤','')])
fb=f'''<div class="L bg" style="background-image:url({A}/bg_me_reach.jpg);filter:blur(18px) brightness(.45);transform:scale(1.1)"></div>
<div style="position:absolute;left:150px;top:300px;width:780px;height:1300px;border-radius:44px;overflow:hidden;border:6px solid #fff;box-shadow:0 30px 90px #000a"><div style="position:absolute;left:-150px;top:-300px;width:1080px;height:1920px;background:url({A}/bg_me_reach.jpg) center/cover"></div>
<div style="position:absolute;right:24px;bottom:150px">{icons}</div><div style="position:absolute;left:30px;bottom:40px;display:flex;align-items:center;gap:14px;font:700 32px Inter;color:#fff;text-shadow:0 2px 8px #000"><span style="width:56px;height:56px;border-radius:50%;background:{BR};display:grid;place-items:center">C</span>steven_chinapal <span style="border:3px solid #fff;border-radius:14px;padding:4px 16px;font-size:26px">Follow</span></div></div>
<img class=cut src="{A}/cut_me_reach.png" style="clip-path:polygon(0 0,100% 0,100% 1600px,0 1600px)">'''
J.append(page('10_framebreak','.cap{top:1640px}',fb+cap('comment','TRIP')))
json.dump(J,open('tools/jobs_frames.json','w'))
