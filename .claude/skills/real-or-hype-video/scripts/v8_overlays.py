import os,sys
from PIL import Image,ImageDraw,ImageFont
os.chdir(sys.argv[1]); W,H=1080,1920; O='v8/ov/'
ANTON='fonts/Anton-Regular.ttf'; MONT='fonts/Montserrat[wght].ttf'; EMO='/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf'
YEL=(255,226,26,255)
def canvas(): return Image.new('RGBA',(W,H),(0,0,0,0))
def emoji(ch,size):
    f=ImageFont.truetype(EMO,109); im=Image.new('RGBA',(140,140),(0,0,0,0))
    ImageDraw.Draw(im).text((4,4),ch,font=f,embedded_color=True); im=im.crop(im.getbbox())
    return im.resize((size,int(size*im.height/im.width)),Image.LANCZOS)
def slanted(text,size,fill,stroke,sw,shear=0.18):
    f=ImageFont.truetype(ANTON,size); d=ImageDraw.Draw(Image.new('RGBA',(1,1)))
    b=d.textbbox((0,0),text,font=f,stroke_width=sw); w,h=b[2]-b[0]+40,b[3]-b[1]+40
    im=Image.new('RGBA',(w+int(h*shear),h),(0,0,0,0))
    ImageDraw.Draw(im).text((20-b[0]+int(h*shear),20-b[1]),text,font=f,fill=fill,stroke_width=sw,stroke_fill=stroke)
    return im.transform(im.size,Image.AFFINE,(1,shear,-h*shear*0.5,0,1,0),Image.BICUBIC)
def put(c,im,cx,cy): c.alpha_composite(im,(int(cx-im.width/2),int(cy-im.height/2)))
# pill
c=canvas(); f=ImageFont.truetype(MONT,58)
try: f.set_variation_by_name('SemiBold')
except Exception: pass
d=ImageDraw.Draw(c); t='Real or Hype?'; b=d.textbbox((0,0),t,font=f); pw,ph=b[2]-b[0]+70,b[3]-b[1]+52
x0,y0=int(W*0.30-pw/2+60),int(H*0.17); d.rounded_rectangle((x0,y0,x0+pw,y0+ph),radius=26,fill=(255,255,255,255))
d.text((x0+35-b[0],y0+26-b[1]),t,font=f,fill=(10,10,10,255)); c.save(O+'pill.png')
# credit
c=canvas(); f2=ImageFont.truetype(MONT,34)
try: f2.set_variation_by_name('SemiBold')
except Exception: pass
ImageDraw.Draw(c).text((70,1700),'@imrachelr_',font=f2,fill=(255,255,255,235),stroke_width=3,stroke_fill=(0,0,0,200)); c.save(O+'credit.png')
# punch
c=canvas(); put(c,slanted('IS IT',190,YEL,(0,0,0,255),10),W*0.42,H*0.47); c.save(O+'isit.png')
put(c,slanted('REAL?',300,YEL,(0,0,0,255),13),W*0.47,H*0.60); c.save(O+'isitfact.png')
c=canvas(); put(c,slanted('$20,000',250,YEL,(0,0,0,255),12),W*0.5,H*0.40); c.save(O+'p20k.png')
# checkbox bar
def bar(c,y,items,size=104):
    f=ImageFont.truetype(ANTON,size); d=ImageDraw.Draw(c)
    parts=[]
    for kind,val in items:
        if kind=='box':
            s=int(size*0.82); im=Image.new('RGBA',(s+12,s+12),(0,0,0,0)); dd=ImageDraw.Draw(im)
            dd.rectangle((6,6,s+6,s+6),fill=(255,255,255,255),outline=(0,0,0,255),width=6)
            dd.rectangle((18,18,s-6,s-6),fill=(0,0,0,0))
            dd.rectangle((14,14,s-2,s-2),outline=(255,255,255,255),width=0)
            # hollow white box with black outline
            im=Image.new('RGBA',(s+12,s+12),(0,0,0,0)); dd=ImageDraw.Draw(im)
            dd.rectangle((4,4,s+8,s+8),outline=(0,0,0,255),width=14); dd.rectangle((8,8,s+4,s+4),outline=(255,255,255,255),width=7)
            if val:
                dd.line([(s*0.22+6,s*0.52+6),(s*0.43+6,s*0.74+6),(s*0.84+6,s*0.2+6)],fill=(0,0,0,255),width=24,joint='curve')
                dd.line([(s*0.22+6,s*0.52+6),(s*0.43+6,s*0.74+6),(s*0.84+6,s*0.2+6)],fill=(40,220,90,255),width=13,joint='curve')
            parts.append(im)
        elif kind=='txt':
            b=d.textbbox((0,0),val,font=f,stroke_width=7); im=Image.new('RGBA',(b[2]-b[0]+10,b[3]-b[1]+10),(0,0,0,0))
            ImageDraw.Draw(im).text((5-b[0],5-b[1]),val,font=f,fill=(255,255,255,255),stroke_width=7,stroke_fill=(0,0,0,255)); parts.append(im)
        elif kind=='emo': parts.append(emoji(val,int(size*0.7)))
        elif kind=='gap': parts.append(Image.new('RGBA',(val,10),(0,0,0,0)))
    tw=sum(p.width for p in parts)+14*(len(parts)-1); x=int(W/2-tw/2)
    for p in parts:
        c.alpha_composite(p,(x,int(y-p.height/2))); x+=p.width+14
c=canvas(); bar(c,H*0.115,[('box',0),('txt','REAL'),('gap',50),('txt','OR'),('gap',50),('box',0),('txt','HYPE'),('emo','💩')]); c.save(O+'bar.png')
c=canvas(); bar(c,H*0.40,[('txt','TREES'),('gap',20),('box',1),('txt','REAL')],130); c.save(O+'v1.png')
bar(c,H*0.50,[('txt','MALL'),('gap',20),('box',1),('txt','HYPE'),('emo','💩')],130); c.save(O+'v2.png')
# labels
def label(name,text,y):
    c=canvas(); f=ImageFont.truetype(MONT,46)
    try: f.set_variation_by_name('Bold')
    except Exception: pass
    d=ImageDraw.Draw(c); b=d.textbbox((0,0),text,font=f); pw,ph=b[2]-b[0]+50,b[3]-b[1]+36; x0=int(W/2-pw/2)
    d.rounded_rectangle((x0,y,x0+pw,y+ph),radius=20,fill=(255,255,255,240)); d.text((x0+25-b[0],y+18-b[1]),text,font=f,fill=(10,10,10,255)); c.save(O+name)
label('l_online.png','ONLINE',1010); label('l_real.png','REAL LIFE',330); label('l_heather.png','Heatherwick Studio',330); label('l_price.png','¥149,800',330); label('l_station.png','Line 3 / 4 · Zhongtan Rd',330)
# rounded masks
def mask(name,w,h,r):
    m=Image.new('L',(w,h),0); ImageDraw.Draw(m).rounded_rectangle((0,0,w-1,h-1),radius=r,fill=255); m.save(O+name)
mask('m_card.png',594,1056,34); mask('m_panel.png',760,700,34)
print('ok')
# captions for his real lines (white, black outline, lower third)
def cap(name,text):
    c=canvas(); f=ImageFont.truetype(MONT,60)
    try: f.set_variation_by_name('ExtraBold')
    except Exception: pass
    d=ImageDraw.Draw(c); words=text.split(); lines=[]; cur=''
    for w in words:
        t=(cur+' '+w).strip()
        if d.textlength(t,font=f)>900 and cur: lines.append(cur); cur=w
        else: cur=t
    lines.append(cur); y=1380
    for ln in lines:
        w=d.textlength(ln,font=f); d.text(((W-w)/2,y),ln,font=f,fill=(255,255,255,255),stroke_width=7,stroke_fill=(0,0,0,255)); y+=78
    c.save(O+name)
cap('c_entrance.png','We are at the entrance of the 1000 tree mall.')
cap('c_floors.png','Six floors here. Absolutely huge.')
cap('c_verdict.png',"If you're in Shanghai for only two, three days, do not come here.")
print('caps ok')
