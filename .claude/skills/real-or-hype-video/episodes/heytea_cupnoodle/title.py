# Hook title card (PNG 1080x1920, transparent): white Montserrat ExtraBold with black outline + colour emoji.
import sys
from PIL import Image,ImageDraw,ImageFont
SK='/home/user/real-or-hype/.claude/skills/real-or-hype-video/scripts/'
out=sys.argv[1]; lines=[('Heytea made a',72,'white'),('CUP NOODLE',104,'#FFE21A'),('drink?!',72,'white')]
EMO='🍜🧋'
W,H=1080,1920; im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
y=200
for txt,sz,col in lines:
    f=ImageFont.truetype(SK+'Montserrat-ExtraBold.ttf',sz)
    tw=d.textlength(txt,font=f)
    extra=0
    if txt=='drink?!':
        extra=2*sz+40
    x=(W-tw-extra)/2
    d.text((x,y),txt,font=f,fill=col,stroke_width=7,stroke_fill='black')
    if extra:
        ef=ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf',109)
        for k,ch in enumerate(EMO):
            e=Image.new('RGBA',(140,140),(0,0,0,0)); ImageDraw.Draw(e).text((0,0),ch,font=ef,embedded_color=True)
            e=e.crop(e.getbbox()).resize((sz,sz),Image.LANCZOS)
            im.alpha_composite(e,(int(x+tw+20+k*(sz+12)),int(y+sz*0.12)))
        # re-centre: emoji appended after text
    y+=int(sz*1.18)
im.save(out); print('title',out)
