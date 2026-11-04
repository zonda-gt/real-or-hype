import os,sys
from PIL import Image,ImageDraw,ImageFont
os.chdir(sys.argv[1]); W,H=1080,1920; O='v9/ov/'
ANTON='fonts/Anton-Regular.ttf'; MONT='fonts/Montserrat[wght].ttf'; ZH='/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
YEL=(255,226,26,255)
def canvas(): return Image.new('RGBA',(W,H),(0,0,0,0))
def slanted(text,size,fill=YEL,sw=12,shear=0.18):
    f=ImageFont.truetype(ANTON,size); d=ImageDraw.Draw(Image.new('RGBA',(1,1)))
    b=d.textbbox((0,0),text,font=f,stroke_width=sw); w,h=b[2]-b[0]+40,b[3]-b[1]+40
    im=Image.new('RGBA',(w+int(h*shear),h),(0,0,0,0))
    ImageDraw.Draw(im).text((20-b[0]+int(h*shear),20-b[1]),text,font=f,fill=fill,stroke_width=sw,stroke_fill=(0,0,0,255))
    return im.transform(im.size,Image.AFFINE,(1,shear,-h*shear*0.5,0,1,0),Image.BICUBIC)
def put(c,im,cx,cy): c.alpha_composite(im,(int(cx-im.width/2),int(cy-im.height/2)))
# punch synced to the sung sting: IS IT -> REAL -> OR HYPE?
c=canvas(); put(c,slanted('IS IT',190),W*0.42,H*0.44); c.save(O+'p1.png')
put(c,slanted('REAL',300),W*0.47,H*0.56); c.save(O+'p2.png')
put(c,slanted('OR HYPE?',170,(255,255,255,255),10),W*0.50,H*0.67); c.save(O+'p3.png')
# Chinese word labels above the inset (he points up at them)
def word(name,zh,py,en):
    c=canvas(); d=ImageDraw.Draw(c)
    fz=ImageFont.truetype(ZH,150); fp=ImageFont.truetype(MONT,54); fe=ImageFont.truetype(MONT,58)
    for f,v in ((fp,'SemiBold'),(fe,'ExtraBold')):
        try: f.set_variation_by_name(v)
        except Exception: pass
    cx=W*0.70; y=640
    w=d.textlength(zh,font=fz); d.text((cx-w/2,y),zh,font=fz,fill=YEL,stroke_width=9,stroke_fill=(0,0,0,255))
    w=d.textlength(py,font=fp); d.text((cx-w/2,y+170),py,font=fp,fill=(255,255,255,255),stroke_width=6,stroke_fill=(0,0,0,255))
    w=d.textlength(en,font=fe); d.text((cx-w/2,y+240),en,font=fe,fill=(255,255,255,255),stroke_width=7,stroke_fill=(0,0,0,255))
    c.save(O+name)
word('w_metro.png','地铁','dìtiě','= METRO')
word('w_mall.png','商场','shāngchǎng','= SHOPPING MALL')
m=Image.new('L',(460,818),0); ImageDraw.Draw(m).rounded_rectangle((0,0,459,817),radius=34,fill=255); m.save(O+'m_ins.png')
print('ok')
