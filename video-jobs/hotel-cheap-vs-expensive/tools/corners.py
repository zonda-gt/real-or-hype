import subprocess,os,glob
from PIL import Image,ImageDraw,ImageFont
os.makedirs("work/corner_frames",exist_ok=True)
finals=sorted(glob.glob("final_*.mp4")); times=[0.3+i*2 for i in range(15)]+[29.9,30.7]
F=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",18)
blocks=[]
for fn in finals:
    rows=[]
    for t in times:
        p=f"work/corner_frames/{fn[:-4]}_{t:.1f}.png"
        subprocess.run(["ffmpeg","-v","error","-y","-ss",str(t),"-i",fn,"-frames:v","1",p],check=True)
        im=Image.open(p).convert("RGB")
        c=[im.crop(b).resize((160,160)) for b in [(0,0,300,300),(780,0,1080,300),(0,1620,300,1920),(780,1620,1080,1920)]]
        top=im.crop((0,0,1080,220)).resize((540,110)); bot=im.crop((0,1540,1080,1920)).resize((540,190))
        row=Image.new("RGB",(160*4+540+10,330),"white")
        for i,x in enumerate(c): row.paste(x,(i*160,22))
        row.paste(top,(650,22)); row.paste(bot,(650,138))
        d=ImageDraw.Draw(row); d.text((4,0),f"{fn} t={t:.1f}s  TL | TR | BL | BR   top 220px band / bottom 380px band",fill="red",font=F)
        rows.append(row)
    blocks.append(rows)
H=sum(r.height for r in blocks[0]); Wd=blocks[0][0].width
sheet=Image.new("RGB",(Wd*len(blocks)+20*(len(blocks)-1),H),"white")
for i,rows in enumerate(blocks):
    y=0
    for r in rows: sheet.paste(r,(i*(Wd+20),y)); y+=r.height
sheet.save("qa/final_contact_sheet.jpg",quality=85); print(sheet.size)
