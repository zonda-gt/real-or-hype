import os,json
D=os.getcwd(); A=f'file://{D}/a'
P=[("p01_wukang","Wukang Mansion","1.2M","travel.creator"),("p02_dumplings","Soup dumpling spot","860K","food.creator"),
("p03_rooftop","Rooftop bar on the Bund","2.4M","nightlife.creator"),("p04_yugarden","Yu Garden at night","3.1M","travel.creator"),
("p05_trees","The 1000 Trees mall","5.6M","city.creator"),("p06_catcafe","Cat café","410K","cafe.creator"),
("p07_anfu","Anfu Road","720K","style.creator"),("p08_jazz","Jazz bar","298K","nightlife.creator"),
("p09_ferry","Huangpu river ferry","1.9M","travel.creator"),("p10_market","Night market","1.1M","food.creator")]
json.dump(P,open('tools/places.json','w'))
HEAD=f"""<!doctype html><html><head><meta charset=utf-8><link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@800;900&display=swap" rel=stylesheet>
<style>@font-face{{font-family:MX;src:url({A}/Montserrat-ExtraBold.ttf)}}*{{box-sizing:border-box;margin:0;padding:0}}body{{font-family:Inter,sans-serif;-webkit-font-smoothing:antialiased}}"""
BRAND='#FF5A36'
def page(name,css,body): open(f'html/{name}.html','w').write(HEAD+css+'</style></head><body>'+body+'</body></html>'); return f'{D}/html/{name}.html'
status='<div class=sb><span>9:41</span><span style="letter-spacing:2px">●●●● 5G ▮</span></div>'
SB_CSS='.sb{height:44px;display:flex;justify-content:space-between;align-items:center;padding:0 26px;font-weight:600;font-size:15px}'
jobs=[]
# A. Saved grid (light)
tiles=''.join(f'<div class=t style="background-image:url({A}/{p[0]}.jpg)"><span class=v>▶ {p[2]}</span><span class=r>⧉</span></div>' for p in P+P[:2])
css=SB_CSS+f"""body{{width:390px;height:844px;background:#fff;color:#000;overflow:hidden}}.hd{{display:flex;align-items:center;gap:14px;padding:6px 16px 10px;font-size:17px;font-weight:700}}
.hd small{{display:block;font-weight:400;color:#737373;font-size:12px}}.g{{display:grid;grid-template-columns:repeat(3,1fr);gap:2px}}.t{{aspect-ratio:3/4;background-size:cover;background-position:center;position:relative}}
.v{{position:absolute;left:6px;bottom:5px;color:#fff;font-size:12px;font-weight:600;text-shadow:0 1px 3px #000a}}.r{{position:absolute;right:6px;top:4px;color:#fff;font-size:14px;text-shadow:0 1px 3px #000a}}
.tabs{{display:flex;justify-content:space-around;padding:10px 0;font-size:13px;color:#737373;border-bottom:1px solid #eee;margin-bottom:2px}}.tabs b{{color:#000}}"""
body=status+'<div class=hd><span style="font-size:26px">‹</span><div>Shanghai trip ideas 🇨🇳<small>247 saved posts</small></div></div><div class=tabs><b>All</b><span>Reels</span><span>Posts</span></div><div class=g>'+tiles+'</div>'
jobs.append(dict(html=page('saved',css,body),w=390,h=844,s=3,out=f'{D}/out/screen_saved.png'))
# B. DM thread (dark)
def reelcard(p,cls='me'):
    return f'<div class="row {cls}"><div class=rc><div class=rh><i></i>{p[3]}</div><div class=ri style="background-image:url({A}/{p[0]}.jpg)"><span>⧉</span></div><div class=rt>{p[1]}</div></div></div>'
def dm(n,extra='',reply=True):
    css=SB_CSS+f"""body{{width:390px;height:844px;background:#000;color:#fff;overflow:hidden;position:relative}}
.hd{{display:flex;align-items:center;gap:10px;padding:4px 14px 10px;border-bottom:1px solid #222}}.av{{width:34px;height:34px;border-radius:50%;background:{BRAND};display:grid;place-items:center;font-weight:800;font-size:15px}}
.hd b{{font-size:15px}}.hd small{{display:block;color:#a8a8a8;font-size:12px}}.th{{padding:10px 12px;display:flex;flex-direction:column;gap:8px;justify-content:flex-end;height:688px;overflow:hidden}}
.row{{display:flex}}.me{{justify-content:flex-end}}.rc{{width:168px;border-radius:16px;overflow:hidden;background:#262626}}.rh{{display:flex;align-items:center;gap:6px;font-size:11px;font-weight:600;padding:7px 9px}}
.rh i{{width:18px;height:18px;border-radius:50%;background:linear-gradient(45deg,#f9ce34,#ee2a7b,#6228d7)}}.ri{{height:200px;background-size:cover;background-position:center;position:relative}}.ri span{{position:absolute;right:8px;top:6px;font-size:14px}}
.rt{{font-size:11px;padding:6px 9px 8px;color:#ddd}}.bub{{max-width:255px;background:#262626;border-radius:20px;padding:10px 14px;font-size:15px;line-height:1.35}}
.link{{width:255px;border-radius:18px;overflow:hidden;background:#262626}}.link .im{{height:120px;background-size:cover;background-position:center}}.link .tx{{padding:10px 12px;font-size:14px;font-weight:700}}.link .tx small{{display:block;font-weight:400;color:#a8a8a8;font-size:12px;margin-top:2px}}
.seen{{text-align:right;color:#a8a8a8;font-size:11px}}.in{{display:flex;gap:8px;align-items:flex-end}}.in .av{{width:26px;height:26px;font-size:11px}}
.bar{{position:absolute;left:10px;right:10px;bottom:22px;height:44px;border-radius:22px;background:#262626;display:flex;align-items:center;padding:0 16px;color:#a8a8a8;font-size:15px}}"""
    msgs=''.join(reelcard(p) for p in P[:n])
    if reply: msgs+=f'''<div class=seen>Seen</div><div class=in><div class=av>C</div><div style="display:flex;flex-direction:column;gap:6px"><div class=bub>Got 10 places 🙌 Building your Shanghai trip…</div>
<div class=link><div class=im style="background-image:url({A}/p04_yugarden.jpg)"></div><div class=tx>Your 3-day Shanghai trip<small>Built from your 10 saved reels · ChinaPal</small></div></div></div></div>'''
    body=status+f'<div class=hd><span style="font-size:26px">‹</span><div class=av>C</div><div><b>steven_chinapal</b><small>ChinaPal · send us your saved reels ✈️</small></div></div><div class=th>{msgs}</div><div class=bar>Message…</div>'
    return page(f'dm{n}{"r" if reply else ""}',css,body)
jobs.append(dict(html=dm(10,reply=True),w=390,h=844,s=3,out=f'{D}/out/screen_dm.png'))
jobs.append(dict(html=dm(4,reply=False),w=390,h=844,s=3,out=f'{D}/out/screen_dm_sending.png'))
# D. Itinerary page (light)
stops=[("10:00","Wukang Mansion",P[0],"Go early, before the crowds","12 min walk"),("10:45","Anfu Road",P[6],"Coffee and shops under the plane trees","8 min walk"),
("12:30","Soup dumpling spot",P[1],"Order the crab xiaolongbao","15 min walk"),("14:30","Cat café",P[5],"Opens 11:00, closed Tuesdays","Metro line 10 · 20 min"),
("18:00","Huangpu river ferry",P[8],"2 yuan, catch it at sunset","6 min walk"),("19:30","Rooftop bar on the Bund",P[2],"Book a window seat","")]
cards=''.join(f'''<div class=st><div class=tm>{t}</div><div class=dot><b>{i+1}</b></div><div class=cd><div class=th2 style="background-image:url({A}/{p[0]}.jpg)"></div><div><div class=nm>{n}</div><div class=fr>from @{p[3]}'s reel</div><div class=tp>{tip}</div></div></div></div>{f'<div class=wk>{w}</div>' if w else ''}''' for i,(t,n,p,tip,w) in enumerate(stops))
pins=[(70,150),(120,190),(170,160),(205,230),(300,120),(330,175)]
path='M'+' L'.join(f'{x},{y}' for x,y in pins)
svgpins=''.join(f'<g><circle cx={x} cy={y} r=12 fill="{BRAND}" stroke="#fff" stroke-width="3"/><text x={x} y={y+4.5} font-size=12 font-weight=800 fill="#fff" text-anchor=middle font-family=Inter>{i+1}</text></g>' for i,(x,y) in enumerate(pins))
MAP=f'''<svg viewBox="0 0 390 270" width=390 height=270><rect width=390 height=270 fill="#EEE9DF"/>
<path d="M255,0 C240,60 290,110 270,160 C250,210 300,240 290,270 L330,270 C340,230 290,200 310,155 C330,105 285,60 295,0Z" fill="#A9CBE3"/>
<g stroke="#fff" stroke-width=6 fill=none><path d="M0,95 L390,70"/><path d="M0,210 L250,180"/><path d="M90,0 L140,270"/><path d="M190,0 L170,270"/><path d="M0,140 L250,130"/></g>
<g stroke="#fff" stroke-width=2.5 fill=none opacity=.8><path d="M0,40 L250,30"/><path d="M40,0 L60,270"/><path d="M0,250 L250,240"/><path d="M230,0 L215,270"/></g>
<rect x=20 y=225 width=60 height=26 rx=6 fill="#cfe3c4"/><path d="{path}" stroke="{BRAND}" stroke-width=4 fill=none stroke-dasharray="8 6" stroke-linecap="round"/>{svgpins}
<text x=342 y=40 font-size=10 fill="#5b7f99" font-family=Inter font-weight=600>Pudong</text><text x=60 y=120 font-size=10 fill="#8a8172" font-family=Inter font-weight=600>Former French Concession</text><text x=268 y=255 font-size=9 fill="#5b7f99" font-family=Inter font-style=italic>Huangpu</text></svg>'''
css=SB_CSS+f"""body{{width:390px;height:844px;background:#FAF8F4;color:#1d1d1f;overflow:hidden}}.top{{padding:6px 18px 10px}}.br{{font-size:12px;font-weight:700;color:{BRAND};letter-spacing:.08em}}
h1{{font-size:26px;font-weight:800;letter-spacing:-.02em;margin-top:4px}}.sub{{font-size:13px;color:#6e6e73;margin-top:3px}}.tabs{{display:flex;gap:8px;padding:12px 18px}}.tabs span{{padding:7px 14px;border-radius:18px;background:#ece8e1;font-size:13px;font-weight:600}}
.tabs .on{{background:#1d1d1f;color:#fff}}.st{{display:grid;grid-template-columns:46px 26px 1fr;align-items:center;padding:0 14px 0 12px}}.tm{{font-size:12px;font-weight:700;color:#6e6e73}}.dot b{{display:grid;place-items:center;width:22px;height:22px;border-radius:50%;background:{BRAND};color:#fff;font-size:11px}}
.cd{{display:flex;gap:10px;background:#fff;border-radius:14px;padding:8px;box-shadow:0 1px 4px #0001;align-items:center}}.th2{{width:46px;height:62px;border-radius:9px;background-size:cover;background-position:center;flex:none}}
.nm{{font-size:14px;font-weight:700}}.fr{{font-size:11px;color:{BRAND};font-weight:600;margin-top:1px}}.tp{{font-size:11.5px;color:#6e6e73;margin-top:2px}}.wk{{font-size:10.5px;color:#9a9aa0;padding:3px 0 3px 84px}}"""
body=status+f'<div class=top><div class=br>CHINAPAL</div><h1>Your Shanghai trip</h1><div class=sub>3 days · 10 places · built from your saved reels</div></div>{MAP}<div class=tabs><span class=on>Day 1</span><span>Day 2</span><span>Day 3</span></div>{cards}'
jobs.append(dict(html=page('itin',css,body),w=390,h=844,s=3,out=f'{D}/out/screen_itinerary.png'))
# C. Building screen
steps=[("Watched your 10 reels",1),("Found 10 places",1),("Grouped them by area",1),("Checking opening hours",0),("Building 3 days",0)]
li=''.join(f'<li class={"ok" if d else "no"}><i>{"✓" if d else ""}</i>{s}</li>' for s,d in steps)
css=SB_CSS+f"""body{{width:390px;height:844px;background:#FAF8F4;color:#1d1d1f;overflow:hidden}}.wrap{{padding:30px 22px}}.br{{font-size:12px;font-weight:700;color:{BRAND};letter-spacing:.08em}}
h1{{font-size:24px;font-weight:800;margin:6px 0 4px}}.pct{{font-size:84px;font-weight:900;letter-spacing:-.04em;margin:18px 0 4px}}.pb{{height:10px;border-radius:5px;background:#e6e1d8;overflow:hidden}}.pb i{{display:block;height:100%;width:62%;background:{BRAND}}}
ul{{list-style:none;margin-top:26px;display:flex;flex-direction:column;gap:14px}}li{{display:flex;gap:12px;align-items:center;font-size:16px;font-weight:600}}li i{{width:24px;height:24px;border-radius:50%;display:grid;place-items:center;font-style:normal;font-size:13px;color:#fff;background:{BRAND}}}
li.no{{color:#a5a5aa}}li.no i{{background:none;border:2px solid #cfcac1}}.strip{{display:flex;gap:6px;margin-top:30px}}.strip div{{width:58px;height:78px;border-radius:9px;background-size:cover;background-position:center}}"""
strip=''.join(f'<div style="background-image:url({A}/{p[0]}.jpg)"></div>' for p in P[:5])
body=status+f'<div class=wrap><div class=br>CHINAPAL</div><h1>Building your trip…</h1><div class=pct>62%</div><div class=pb><i></i></div><ul>{li}</ul><div class=strip>{strip}</div></div>'
jobs.append(dict(html=page('build',css,body),w=390,h=844,s=3,out=f'{D}/out/screen_building.png'))
json.dump(jobs,open('tools/jobs_screens.json','w'))
