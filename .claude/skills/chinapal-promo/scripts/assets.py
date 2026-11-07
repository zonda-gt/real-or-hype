# Pre-render overlay assets at 720x1280 scale
from PIL import Image,ImageDraw,ImageFont,ImageFilter
import json,subprocess
P=json.load(open('tools/places.json')); BR=(255,90,54); Y=(255,212,59)
def font(name,sz): return ImageFont.truetype(name,sz)
INTER_B=subprocess.run(['fc-match','-f','%{file}','Inter:bold'],capture_output=True,text=True).stdout
INTER_X=subprocess.run(['fc-match','-f','%{file}','Inter:extrabold'],capture_output=True,text=True).stdout
MX='a/Montserrat-ExtraBold.ttf'
def rounded(im,r):
    m=Image.new('L',im.size,0); ImageDraw.Draw(m).rounded_rectangle((0,0,im.size[0]-1,im.size[1]-1),r,fill=255); o=im.convert('RGBA'); o.putalpha(m); return o
def card(i,w,views=True,border=4):
    h=int(w*1.5); th=Image.open(f'a/{P[i][0]}.jpg').convert('RGB').resize((w,h),Image.LANCZOS)
    if views:
        d=ImageDraw.Draw(th); f=font(INTER_B,max(12,w//9)); d.text((8,h-8),'▶ '+P[i][2],font=f,fill='white',anchor='ld',stroke_width=2,stroke_fill=(0,0,0))
    c=rounded(th,max(8,w//10)); pad=border; b=Image.new('RGBA',(w+2*pad,h+2*pad),(0,0,0,0))
    ImageDraw.Draw(b).rounded_rectangle((0,0,w+2*pad-1,h+2*pad-1),max(8,w//10)+pad,fill='white'); b.alpha_composite(c,(pad,pad))
    sh=Image.new('RGBA',(b.size[0]+40,b.size[1]+40),(0,0,0,0)); sm=Image.new('L',sh.size,0); ImageDraw.Draw(sm).rounded_rectangle((20,28,20+b.size[0],28+b.size[1]),20,fill=110)
    sh.putalpha(sm.filter(ImageFilter.GaussianBlur(10))); sh.alpha_composite(b,(20,20)); return sh
for i in range(10):
    card(i,120).save(f'ed/card_{i}.png'); card(i,90,views=False).save(f'ed/cardS_{i}.png')
# caption renderer
def caption(small,big,show_big=True,W=720):
    im=Image.new('RGBA',(W,240),(0,0,0,0)); d=ImageDraw.Draw(im)
    fs=font(MX,36); fb=font(MX,64)
    if small: d.text((W//2,50),small,font=fs,fill='white',anchor='mm',stroke_width=4,stroke_fill=(0,0,0))
    if big and show_big: d.text((W//2,120),big,font=fb,fill=Y,anchor='mm',stroke_width=5,stroke_fill=(0,0,0))
    return im
import pickle
CAPS={'01':("you've saved","hundreds of reels"),'02':("rooftop bars, dumpling spots,","that café…"),'03':("and you've been to","none of them."),
'04':("so just send them","all to us"),'10':("comment","TRIP")}
for k,(s,b) in CAPS.items():
    caption(s,b,False).save(f'ed/cap_{k}_a.png'); caption(s,b,True).save(f'ed/cap_{k}_b.png')
# checklist panel states
items=['Save the reel','Send it to @steven_chinapal','Get your trip']
for st in range(4):
    W,H=620,300; im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.rounded_rectangle((0,0,W-1,H-1),28,fill=(22,22,26,215),outline=(255,255,255,40),width=2)
    d.text((32,40),'ALL YOU NEED TO DO',font=font(INTER_B,20),fill=(255,255,255,170),anchor='lm'); d.text((W-32,40),f'{st} of 3',font=font(INTER_B,20),fill=(255,255,255,170),anchor='rm')
    for j,t in enumerate(items):
        y=105+j*68; on=j<st
        if on: d.ellipse((32,y-19,70,y+19),fill=BR); d.text((51,y),'✓',font=font('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',24),fill='white',anchor='mm')
        else: d.ellipse((32,y-19,70,y+19),outline=(255,255,255,110),width=3)
        d.text((90,y),t,font=font(INTER_B,31),fill=(255,255,255,255 if on else 150),anchor='lm')
    im.save(f'ed/check_{st}.png')
# phone frames from screens
for n in ['dm_sending','dm']:
    s=Image.open(f'out/screen_{n}.png').convert('RGB').resize((280,606),Image.LANCZOS); s=rounded(s,30)
    b=Image.new('RGBA',(296,622),(0,0,0,0)); ImageDraw.Draw(b).rounded_rectangle((0,0,295,621),38,fill=(17,17,17)); b.alpha_composite(s,(8,8)); b.save(f'ed/phone_{n}.png')
print('assets ok')
