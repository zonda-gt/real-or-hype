# Reference-style graphics: serif title on highlight boxes (like "SHANGHAI'S / Basement Seafood"),
# handwritten object labels (like "crispy pork belly"), serif info cards.
from PIL import Image,ImageDraw,ImageFont
SERIF='../fonts/dm-serif-display-latin-400-normal.ttf'; HAND='../fonts/chewy-latin-400-normal.ttf'
YEL=(255,240,150); WHITE=(255,255,255); INK=(20,20,20)
def boxline(im,text,size,cx,y,bg,fg=INK,font=SERIF,padx=26,pady=10,rot=0):
    f=ImageFont.truetype(font,size); d=ImageDraw.Draw(im)
    l,t,r,b=d.textbbox((0,0),text,font=f); w,h=r-l,b-t
    tile=Image.new('RGBA',(w+2*padx,h+2*pady),bg+(255,)); td=ImageDraw.Draw(tile)
    td.text((padx-l,pady-t),text,font=f,fill=fg)
    if rot: tile=tile.rotate(rot,expand=True,resample=Image.BICUBIC)
    # soft shadow
    sh=Image.new('RGBA',tile.size,(0,0,0,0)); sh.paste((0,0,0,90),mask=tile.split()[3])
    x=int(cx-tile.width/2); im.alpha_composite(sh,(x+6,y+8)); im.alpha_composite(tile,(x,y))
    return y+tile.height
def hand(im,text,size,cx,y,rot=-5,col=WHITE):
    f=ImageFont.truetype(HAND,size); tmp=Image.new('RGBA',(1080,400),(0,0,0,0)); d=ImageDraw.Draw(tmp)
    w=d.textlength(text,font=f); d.text(((1080-w)/2,100),text,font=f,fill=col,stroke_width=6,stroke_fill=(40,30,20))
    tmp=tmp.rotate(rot,resample=Image.BICUBIC); im.alpha_composite(tmp,(int(cx-540),y-100))
def new(): return Image.new('RGBA',(1080,1920),(0,0,0,0))
im=new(); y=boxline(im,"CHINA'S",108,500,760,YEL); boxline(im,"Giraffe Hotel",132,580,y-6,YEL)
hand(im,"breakfast included",62,640,1105,rot=-6); im.save('ov/title.png')
for name,txt in [('l_manor','Giraffe Manor'),('l_capy','capybara'),('l_racc','raccoons'),('l_crane','red-crowned cranes'),('l_630','6:30 AM')]:
    im=new(); hand(im,txt,74,540,1260,rot=-4); im.save(f'ov/{name}.png')
im=new(); y=boxline(im,"1 night + breakfast",62,540,560,WHITE); y=boxline(im,"¥1,000",150,540,y+4,YEL); boxline(im,"about $140",62,540,y+4,WHITE); im.save('ov/price.png')
im=new(); y=boxline(im,"the one in Kenya",62,540,560,WHITE); y=boxline(im,"$1,400+",150,540,y+4,YEL); boxline(im,"a night, per person",58,540,y+4,WHITE); im.save('ov/kenya.png')
print('ok')
