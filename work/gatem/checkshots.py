import subprocess,io,sys
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,'.'); from edl import shots
font=ImageFont.truetype('/home/user/real-or-hype/.claude/skills/real-or-hype-video/scripts/Montserrat-ExtraBold.ttf',16)
S=shots(); TW=150; tiles=[]
for s in S:
    fr=[]
    for t in [s['inn']+0.05, s['inn']+s['dur']/2, s['inn']+s['dur']-0.08]:
        r=subprocess.run(['ffmpeg','-loglevel','error','-ss',f'{t:.2f}','-i',f"src/{s['src']}.mp4",'-frames:v','1','-vf',f'scale={TW}:{int(TW*16/9)}','-f','image2pipe','-vcodec','png','-'],capture_output=True)
        fr.append(Image.open(io.BytesIO(r.stdout)).convert('RGB') if r.stdout else Image.new('RGB',(TW,int(TW*16/9)),'red'))
    tiles.append((s,fr))
H=int(TW*16/9); cols=4
rows=(len(tiles)+cols-1)//cols
img=Image.new('RGB',(cols*(TW*3+8),rows*(H+22)),(20,20,20)); d=ImageDraw.Draw(img)
for k,(s,fr) in enumerate(tiles):
    x=(k%cols)*(TW*3+8); y=(k//cols)*(H+22)
    for j,f in enumerate(fr): img.paste(f,(x+j*TW,y))
    d.text((x+2,y+H+2),f"#{s['i']} {s['t0']:.2f} {s['src']}@{s['inn']} ({s['dur']:.2f})",fill='yellow',font=font)
img.save('shotcheck.jpg',quality=80); print(img.size)
