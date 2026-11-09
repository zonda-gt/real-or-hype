import json,subprocess,io,sys
from PIL import Image,ImageDraw,ImageFont
S='/home/user/videos/promo1/Ang/reel promo1/'; P='/home/user/videos/promo1/prev/'
A,B,C='20261109_120846.mp4','20261109_121206.mp4','20261109_121401.mp4'
L={
'A1_saved':(A,[(1.34,4.10),(7.98,11.92),(17.76,19.42),(41.02,42.40)]),
'A2_rooftop':(A,[(19.68,21.28),(22.04,24.30),(34.36,36.32),(42.76,45.06)]),
'A3_none':(A,[(45.42,46.24),(53.26,57.58)]),
'A4_send':(A,[(63.82,64.84),(71.94,73.70),(80.46,82.10),(85.42,87.04),(109.80,111.84)]),
'A5_check':(A,[(96.98,99.16),(101.74,104.54),(112.12,114.88)]),
'A6_plan':(A,[(115.04,116.70),(123.28,126.78),(127.72,130.05),(134.16,136.38)]),
'A7_route':(A,[(146.6,147.4),(147.9,157.0),(157.5,158.4),(159.2,163.7)]),
'A9_A10':(A,[(170.40,172.18),(179.40,181.52)]),
'B1_hold':(B,[(0.0,4.02),(4.44,8.18),(50.46,54.12)]),
'B2_check':(B,[(14.82,17.24),(20.76,22.26),(54.48,57.82)]),
'B3_food':(B,[(33.5,34.74),(38.06,41.14),(43.26,46.58),(58.06,64.22)]),
'B4_map':(B,[(73.76,76.62),(80.78,85.12)]),
'B5_B6':(B,[(89.76,91.74),(94.5,96.32)]),
'C1_offer':(C,[(8.16,12.28),(13.76,21.26)]),
'C2_places':(C,[(24.54,27.20),(29.52,32.16),(34.90,38.52),(41.80,43.34)]),
'C3_dm':(C,[(43.60,45.22),(47.50,49.38),(49.90,51.36)]),
'C4_plan':(C,[(61.98,63.5),(68.10,70.00),(72.80,74.82),(78.22,81.78)]),
'C5_C6':(C,[(93.78,97.32),(99.36,100.88),(101.16,103.18),(106.68,110.08)]),
}
fn=ImageFont.load_default(size=13); TW=96; STEP=0.4
for name,(f,rs) in L.items():
    if len(sys.argv)>1 and name not in sys.argv[1:]: continue
    W=[w for s in json.load(open(S+f+'.json')) for w in s['w']]
    rows=[]
    for a,b in rs:
        ts=[a-0.2+k*STEP for k in range(int((b-a+0.4)/STEP)+1)]
        ims=[]
        for t in ts:
            im=Image.open(io.BytesIO(subprocess.run(['ffmpeg','-loglevel','error','-ss',f'{t:.2f}','-i',P+f,'-frames:v','1','-vf',f'scale={TW}:-2','-f','image2pipe','-vcodec','png','-'],capture_output=True).stdout)).convert('RGB')
            wd=[w[2].strip() for w in W if w[0]<=t+0.2 and w[1]>=t-0.2]
            d=ImageDraw.Draw(im); d.rectangle((0,im.height-30,TW,im.height),fill=(0,0,0)); d.text((2,im.height-29),f'{t:.1f}',fill='yellow',font=fn); d.text((2,im.height-15),(wd[0] if wd else '')[:12],fill='white',font=fn)
            ims.append(im)
        rows.append((a,b,ims))
    H=rows[0][2][0].height; maxn=max(len(r[2]) for r in rows); maxn=min(maxn,24)
    pg=Image.new('RGB',(maxn*TW,len(rows)*(H+16)),'#222'); d=ImageDraw.Draw(pg)
    for r,(a,b,ims) in enumerate(rows):
        d.text((2,r*(H+16)+1),f'take {r+1}: {a}-{b}',fill='cyan',font=fn)
        for c,im in enumerate(ims[:maxn]): pg.paste(im,(c*TW,r*(H+16)+16))
    pg.save(f'takes/{name}.jpg',quality=82); print(name,len(rows))
