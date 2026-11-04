import sys,os
from PIL import Image, ImageDraw, ImageFont, ImageOps
files=[l.strip() for l in open(sys.argv[1]) if l.strip()]
out=sys.argv[2]; per=24; cols=6; W=300
font=ImageFont.load_default(size=22) if hasattr(ImageFont,'load_default') else None
for s in range(0,len(files),per):
    chunk=files[s:s+per]; tiles=[]
    for f in chunk:
        im=ImageOps.exif_transpose(Image.open(f)).convert('RGB')
        im.thumbnail((W,W)); t=Image.new('RGB',(W,W+30),'black'); t.paste(im,((W-im.width)//2,30+(W-im.height)//2))
        d=ImageDraw.Draw(t); d.text((4,2),os.path.basename(f)[:-4].replace('VID_20260910_',''),fill='yellow',font=font); tiles.append(t)
    rows=(len(tiles)+cols-1)//cols; sh=Image.new('RGB',(cols*W,rows*(W+30)),'gray')
    for i,t in enumerate(tiles): sh.paste(t,((i%cols)*W,(i//cols)*(W+30)))
    sh.save(f'{out}/sheet_{s//per+1:02d}.jpg',quality=80)
print('ok')
