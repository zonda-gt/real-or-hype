# Episode 2 (Manner Coffee, North Bund) overlays. Same styles as episode 1 (v8/v9 overlays).
import os,sys
from PIL import Image,ImageDraw,ImageFont
os.chdir(sys.argv[1]); W,H=1080,1920; O='ov/'
ANTON='fonts/Anton-Regular.ttf'; MONT='fonts/Montserrat[wght].ttf'; EMO='/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf'
YEL=(255,226,26,255)
def canvas(): return Image.new('RGBA',(W,H),(0,0,0,0))
def mont(size,var):
    f=ImageFont.truetype(MONT,size)
    try: f.set_variation_by_name(var)
    except Exception: pass
    return f
def emoji(ch,size):
    f=ImageFont.truetype(EMO,109); im=Image.new('RGBA',(140,140),(0,0,0,0))
    ImageDraw.Draw(im).text((4,4),ch,font=f,embedded_color=True); im=im.crop(im.getbbox())
    return im.resize((size,int(size*im.height/im.width)),Image.LANCZOS)
def slanted(text,size,fill=YEL,sw=12,shear=0.18):
    f=ImageFont.truetype(ANTON,size); d=ImageDraw.Draw(Image.new('RGBA',(1,1)))
    b=d.textbbox((0,0),text,font=f,stroke_width=sw); w,h=b[2]-b[0]+40,b[3]-b[1]+40
    im=Image.new('RGBA',(w+int(h*shear),h),(0,0,0,0))
    ImageDraw.Draw(im).text((20-b[0]+int(h*shear),20-b[1]),text,font=f,fill=fill,stroke_width=sw,stroke_fill=(0,0,0,255))
    return im.transform(im.size,Image.AFFINE,(1,shear,-h*shear*0.5,0,1,0),Image.BICUBIC)
def put(c,im,cx,cy): c.alpha_composite(im,(int(cx-im.width/2),int(cy-im.height/2)))
# pill
c=canvas(); f=mont(58,'SemiBold'); d=ImageDraw.Draw(c); t='Real or Hype?'; b=d.textbbox((0,0),t,font=f); pw,ph=b[2]-b[0]+70,b[3]-b[1]+52
x0,y0=int(W*0.30-pw/2+60),int(H*0.17); d.rounded_rectangle((x0,y0,x0+pw,y0+ph),radius=26,fill=(255,255,255,255))
d.text((x0+35-b[0],y0+26-b[1]),t,font=f,fill=(10,10,10,255)); c.save(O+'pill.png')
# credit (bottom-left of the card)
c=canvas(); ImageDraw.Draw(c).text((70,1700),'@mikechinavlog_2',font=mont(34,'SemiBold'),fill=(255,255,255,235),stroke_width=3,stroke_fill=(0,0,0,200)); c.save(O+'credit.png')
# punch synced to the sung sting
c=canvas(); put(c,slanted('IS IT',190),W*0.42,H*0.44); c.save(O+'p1.png')
put(c,slanted('REAL',300),W*0.47,H*0.56); c.save(O+'p2.png')
put(c,slanted('OR HYPE?',170,(255,255,255,255),10),W*0.50,H*0.67); c.save(O+'p3.png')
# checkbox bar
def box(s,state):
    im=Image.new('RGBA',(s+12,s+12),(0,0,0,0)); dd=ImageDraw.Draw(im)
    col={0:(255,255,255,255),'real':(40,220,90,255),'hype':(235,50,50,255)}[state]
    dd.rectangle((4,4,s+8,s+8),outline=(0,0,0,255),width=14); dd.rectangle((8,8,s+4,s+4),outline=col,width=7)
    if state=='real':
        p=[(s*0.22+6,s*0.52+6),(s*0.43+6,s*0.74+6),(s*0.84+6,s*0.2+6)]
        dd.line(p,fill=(0,0,0,255),width=24,joint='curve'); dd.line(p,fill=col,width=13,joint='curve')
    if state=='hype':
        for p in ([(s*0.24+6,s*0.24+6),(s*0.80+6,s*0.80+6)],[(s*0.80+6,s*0.24+6),(s*0.24+6,s*0.80+6)]):
            dd.line(p,fill=(0,0,0,255),width=24); dd.line(p,fill=col,width=13)
    return im
def bar(c,y,items,size=104):
    f=ImageFont.truetype(ANTON,size); d=ImageDraw.Draw(c); parts=[]
    for kind,val,*col in items:
        if kind=='box': parts.append(box(int(size*0.82),val))
        elif kind=='txt':
            fill=col[0] if col else (255,255,255,255)
            b=d.textbbox((0,0),val,font=f,stroke_width=7); im=Image.new('RGBA',(b[2]-b[0]+10,b[3]-b[1]+10),(0,0,0,0))
            ImageDraw.Draw(im).text((5-b[0],5-b[1]),val,font=f,fill=fill,stroke_width=7,stroke_fill=(0,0,0,255)); parts.append(im)
        elif kind=='emo': parts.append(emoji(val,int(size*0.7)))
        elif kind=='gap': parts.append(Image.new('RGBA',(val,10),(0,0,0,0)))
    tw=sum(p.width for p in parts)+14*(len(parts)-1); x=int(W/2-tw/2)
    for p in parts: c.alpha_composite(p,(x,int(y-p.height/2))); x+=p.width+14
c=canvas(); bar(c,H*0.115,[('box',0),('txt','REAL'),('gap',50),('txt','OR'),('gap',50),('box',0),('txt','HYPE'),('emo','💩')]); c.save(O+'bar.png')
# labels + masks
def label(name,text,y):
    c=canvas(); f=mont(46,'Bold'); d=ImageDraw.Draw(c); b=d.textbbox((0,0),text,font=f); pw,ph=b[2]-b[0]+50,b[3]-b[1]+36; x0=int(W/2-pw/2)
    d.rounded_rectangle((x0,y,x0+pw,y+ph),radius=20,fill=(255,255,255,240)); d.text((x0+25-b[0],y+18-b[1]),text,font=f,fill=(10,10,10,255)); c.save(O+name)
label('l_online.png','ONLINE',1010); label('l_real.png','REAL LIFE',330)
def mask(name,w,h,r):
    m=Image.new('L',(w,h),0); ImageDraw.Draw(m).rounded_rectangle((0,0,w-1,h-1),radius=r,fill=255); m.save(O+name)
mask('m_card.png',594,1056,34); mask('m_panel.png',760,700,34)
print('ok')
