import subprocess,json,math,sys,os
import numpy as np, cv2
from PIL import Image,ImageDraw,ImageFont,ImageFilter
from rembg import remove,new_session
W,H,FPS=720,1280,24; BR=(255,90,54); Y=(255,212,59)
SES=new_session('u2net_human_seg')
INTER_B=subprocess.run(['fc-match','-f','%{file}','Inter:bold'],capture_output=True,text=True).stdout
INTER_X=subprocess.run(['fc-match','-f','%{file}','Inter:extrabold'],capture_output=True,text=True).stdout
DJ='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
F=lambda p,s: ImageFont.truetype(p,s)
L=lambda n: Image.open(f'ed/{n}.png').convert('RGBA')
def clamp(x,a=0,b=1): return max(a,min(b,x))
def eo(x): x=clamp(x); return 1-(1-x)**3
def eio(x): x=clamp(x); return 3*x*x-2*x*x*x
def eback(x):
    x=clamp(x); c=1.7; return 1+(c+1)*(x-1)**3+c*(x-1)**2
def put(cv,img,cx,cy,s=1.0,rot=0,alpha=1.0):
    if s<=0.01 or alpha<=0.01: return
    im=img
    if s!=1: im=im.resize((max(1,int(im.width*s)),max(1,int(im.height*s))),Image.BILINEAR)
    if rot: im=im.rotate(rot,expand=True,resample=Image.BILINEAR)
    if alpha<1:
        a=im.getchannel('A').point(lambda v:int(v*alpha)); im=im.copy(); im.putalpha(a)
    cv.alpha_composite(im,(int(cx-im.width/2),int(cy-im.height/2))) if (0<=int(cx-im.width/2) and 0<=int(cy-im.height/2) and int(cx-im.width/2)+im.width<=W and int(cy-im.height/2)+im.height<=H) else paste_clip(cv,im,int(cx-im.width/2),int(cy-im.height/2))
def paste_clip(cv,im,x,y):
    x0,y0=max(0,x),max(0,y); x1,y1=min(W,x+im.width),min(H,y+im.height)
    if x1<=x0 or y1<=y0: return
    cv.alpha_composite(im.crop((x0-x,y0-y,x1-x,y1-y)),(x0,y0))
def frames(src,tin,dur):
    cmd=['ffmpeg','-loglevel','error','-ss',str(tin),'-t',str(dur),'-i',src,'-vf','scale=-2:1280,crop=720:1280,fps=24','-f','rawvideo','-pix_fmt','rgb24','-']
    p=subprocess.Popen(cmd,stdout=subprocess.PIPE); n=0
    while True:
        b=p.stdout.read(W*H*3)
        if len(b)<W*H*3: break
        yield n,Image.frombytes('RGB',(W,H),b); n+=1
class Masker:
    def __init__(s): s.prev=None
    def __call__(s,im):
        m=np.asarray(remove(im,session=SES,only_mask=True)).astype(np.float32)
        s.prev=m if s.prev is None else 0.55*m+0.45*s.prev
        return Image.fromarray(np.clip(s.prev,0,255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))
def writer(out):
    return subprocess.Popen(['ffmpeg','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-crf','18','-preset','medium','-pix_fmt','yuv420p',out],stdin=subprocess.PIPE)
def cap(cv,k,t,tb,y=900):
    im=L(f'cap_{k}_b') if t>=tb else L(f'cap_{k}_a'); cv.alpha_composite(im,(0,y))
SFX=[]  # (seg, local t, name, vol)
def sfx(seg,t,n,v): SFX.append((seg,t,n,v))
# ---------------- segments ----------------
def s01(n,fr,m,t):
    cv=fr.convert('RGBA')
    pos=[(30,120,190,-6),(250,40,170,4),(690,60,180,-3),(880,190,170,7),(20,560,180,5),(860,560,190,-5),(130,330,160,-2),(760,340,150,3),(450,-20,170,-4)]
    for i,(x,y,w,r) in enumerate(pos):
        t0=0.15+i*0.28; sc=eback((t-t0)/0.3)*(w*2/3/128)
        if n==0: sfx('01',t0+0.05,'pop',0.25)
        put(cv,L(f'card_{i}'),(x+w/2)*2/3,min(560,(y+w*0.75)*2/3+40),sc,r)
    cv.paste(fr,(0,0),m); cap(cv,'01',t,1.40-0.08); return cv
def s02(n,fr,m,t):
    cv=fr.convert('RGBA'); grow=eo(t/0.5); front=[]
    for i in range(10):
        a=2*math.pi*i/10+0.2+0.95*t; x=360+330*grow*math.cos(a); y=690+85*grow*math.sin(a); d=(math.sin(a)+1)/2
        item=(L(f'cardS_{i}'),x,y,(0.6+0.55*d)*grow,-math.cos(a)*10,0.65+0.35*d)
        if math.sin(a)>0: front.append((d,item))
        else: put(cv,*item)
    cv.paste(fr,(0,0),m)
    for d,item in sorted(front,key=lambda z:z[0]): put(cv,*item)
    cap(cv,'02',t,3.38-0.08) if t>=0.46-0.08 else None; return cv
PLATE={}
def s03(n,fr,m,t):
    if n==0:
        a=np.asarray(fr); mk=(np.asarray(m)>40).astype(np.uint8)*255; mk=cv2.dilate(mk,np.ones((41,41),np.uint8))
        PLATE['p']=Image.fromarray(cv2.inpaint(a,mk,12,cv2.INPAINT_TELEA)).filter(ImageFilter.GaussianBlur(3))
    s=1+0.42*eio(t/3.4); p=PLATE['p']; cx,cy=360,560
    z=p.resize((int(W*s),int(H*s)),Image.BILINEAR); x0=int(cx*s-cx); y0=int(cy*s-cy)
    cv=z.crop((x0,y0,x0+W,y0+H)).convert('RGBA'); vg=Image.new('RGBA',(W,H),(0,0,0,int(70*eio(t/3.4)))); cv.alpha_composite(vg)
    cv.paste(fr,(0,0),m); cap(cv,'03',t,1.38-0.08); return cv
def s04(n,fr,m,t):
    cv=fr.convert('RGBA'); e=eo(t/0.4); ph=L('phone_dm' if t>=1.95 else 'phone_dm_sending')
    if n==0: sfx('04',0.0,'whoosh',0.35); sfx('04',1.95,'ding',0.35)
    put(cv,ph,560,-420+(860)*e,0.9,6-2*e)
    for k,(ci,t0) in enumerate([(4,0.45),(6,0.85),(1,1.25)]):
        if n==0: sfx('04',t0,'whoosh',0.18)
        q=(t-t0)/0.45
        if 0<=q<=1:
            qe=eio(q); x=-40+(560+40)*qe; y=760-330*qe-120*math.sin(math.pi*qe)
            put(cv,L(f'card_{ci}'),x,y,0.9*(1-0.7*qe),-18*(1-qe),1-0.6*max(0,qe-0.6)/0.4)
    if t>=0.9-0.08: cap(cv,'04',t,1.72-0.08)
    return cv
def s05(n,fr,m,t):
    cv=fr.convert('RGBA'); st=0 if t<1.11 else 1 if t<2.03 else 2 if t<2.30 else 3
    if n==0:
        for tt in (1.11,2.03,2.30): sfx('05',tt,'ding',0.3)
        sfx('05',0.0,'whoosh',0.3)
    e=eo(t/0.35); put(cv,L(f'check_{st}'),360,-200+(380)*e,1.0); return cv
def s06(n,fr,m,t):
    p=eio((t-0.45)/0.8)
    cv=Image.new('RGBA',(W,H),(233,228,218,255)); d=ImageDraw.Draw(cv)
    wx0,wy0,wx1,wy1=47,190,673,1235
    win=Image.new('RGBA',(W,H),(0,0,0,0)); dw=ImageDraw.Draw(win)
    dw.rounded_rectangle((wx0,wy0,wx1,wy1),28,fill=(250,248,244,255))
    for i,c in enumerate([(255,95,87),(254,188,46),(40,200,64)]): dw.ellipse((wx0+22+i*24,wy0+20,wx0+36+i*24,wy0+34),fill=c)
    dw.text((wx0+110,wy0+27),'ChinaPal · building your trip',font=F(INTER_B,18),fill=(140,140,140),anchor='lm'); dw.line((wx0,wy0+52,wx1,wy0+52),fill=(235,235,235),width=2)
    steps=['Watched your 10 reels','Found 10 places','Grouped them by area','Checked opening hours','Built 3 days']
    for i,s in enumerate(steps):
        y=800+i*50; on=t>=1.4+i*0.62
        if n==0: sfx('06',1.4+i*0.62,'click',0.35)
        if on: dw.ellipse((wx0+40,y-15,wx0+70,y+15),fill=BR); dw.text((wx0+55,y),'✓',font=F(DJ,18),fill='white',anchor='mm')
        else: dw.ellipse((wx0+40,y-15,wx0+70,y+15),outline=(207,202,193),width=3)
        dw.text((wx0+86,y),s,font=F(INTER_B,26),fill=(29,29,31) if on else (165,165,170),anchor='lm')
    pc=clamp((t-1.2)/3.3); dw.rounded_rectangle((wx0+40,1052,wx1-40,1066),7,fill=(230,225,216)); dw.rounded_rectangle((wx0+40,1052,wx0+40+int((wx1-wx0-80)*pc),1066),7,fill=BR)
    for i in range(5):
        th=Image.open(f'a/{json.load(open("tools/places.json"))[i][0]}.jpg').convert('RGB').resize((100,140)); win.paste(th,(wx0+40+i*112,1080))
    if p>0:
        a=win.getchannel('A').point(lambda v:int(v*p)); win.putalpha(a); cv.alpha_composite(win)
        d.text((40,30),f'{int(round(pc*100))}%',font=F(INTER_X,120),fill=(29,29,31,int(255*p)))
    # video rect
    tx0,ty0,tx1,ty1=wx0+20,wy0+72,wx1-20,742
    rx0,ry0,rx1,ry1=[a+(b-a)*p for a,b in zip((0,0,W,H),(tx0,ty0,tx1,ty1))]
    rw,rh=int(rx1-rx0),int(ry1-ry0); asp=rw/rh
    ch=min(H,W/asp); cw=ch*asp; cy0=max(0,min(H-ch,380-ch*0.42))
    crop=fr.crop((int((W-cw)/2),int(cy0),int((W+cw)/2),int(cy0+ch))).resize((rw,rh),Image.BILINEAR).convert('RGBA')
    mk=Image.new('L',(rw,rh),0); ImageDraw.Draw(mk).rounded_rectangle((0,0,rw-1,rh-1),int(24*p),fill=255)
    cv.paste(crop,(int(rx0),int(ry0)),mk); return cv
def s07(n,fr,m,t):
    cv=fr.convert('RGBA'); d=ImageDraw.Draw(cv)
    pts=[(80,470),(230,330),(380,250),(530,300),(650,440)]; pin_t=[0.3,1.42,2.10,2.80,3.78]
    pins=[(0,None,'Start'),(1,5,'Cat café'),(2,None,''),(3,3,'Yu Garden'),(4,2,'Rooftop bar')]
    if n==0:
        for k,(pi,ci,lab) in enumerate(pins):
            if ci is not None or k==0: sfx('07',pin_t[k],'pop',0.3)
    # progress along path
    seg=0; f=0
    for k in range(len(pts)-1):
        if t>=pin_t[k]: seg=k; f=clamp((t-pin_t[k])/(pin_t[k+1]-pin_t[k]))
    if t>=pin_t[-1]: seg=len(pts)-2; f=1
    lay=Image.new('RGBA',(W,H),(0,0,0,0)); dl=ImageDraw.Draw(lay)
    def dashed(a,b,frac):
        L_=math.dist(a,b); nseg=int(L_/22)
        for i in range(nseg):
            s0=i/nseg; s1=(i+0.6)/nseg
            if s0>frac: break
            s1=min(s1,frac); dl.line((a[0]+(b[0]-a[0])*s0,a[1]+(b[1]-a[1])*s0,a[0]+(b[0]-a[0])*s1,a[1]+(b[1]-a[1])*s1),fill=BR,width=8)
    if t>=pin_t[0]:
        for k in range(seg): dashed(pts[k],pts[k+1],1)
        dashed(pts[seg],pts[seg+1],f)
    for k,(pi,ci,lab) in enumerate(pins):
        sc=eback((t-pin_t[k])/0.3)
        if sc<=0.01: continue
        x,y=pts[pi]
        if ci is not None:
            put(lay,L(f'cardS_{ci}'),x,y-110,0.95*sc)
            if lab:
                tl=Image.new('RGBA',(200,40),(0,0,0,0)); dt=ImageDraw.Draw(tl); dt.rounded_rectangle((0,0,199,39),20,fill=(29,29,31,230)); dt.text((100,20),lab,font=F(INTER_B,20),fill='white',anchor='mm')
                put(lay,tl,x,y+42,0.8*sc)
        pn=Image.new('RGBA',(46,46),(0,0,0,0)); dp=ImageDraw.Draw(pn); dp.ellipse((0,0,45,45),fill='white'); dp.ellipse((4,4,41,41),fill=BR); dp.text((23,23),str(k+1),font=F(INTER_X,20),fill='white',anchor='mm')
        put(lay,pn,x,y,sc)
    pill=Image.new('RGBA',(150,52),(0,0,0,0)); dq=ImageDraw.Draw(pill); dq.rounded_rectangle((0,0,149,51),26,fill=(29,29,31)); dq.text((75,26),'DAY 1',font=F(INTER_X,26),fill='white',anchor='mm')
    put(lay,pill,110,90,eback(t/0.3))
    cv.alpha_composite(lay); cv.paste(fr,(0,0),m); return cv
CAFE_CARD=None
def zoomblur(img,s0,s1,nn=8):
    acc=None
    for i in range(nn):
        s=s0+(s1-s0)*i/(nn-1); z=img.resize((int(W*s),int(H*s)),Image.BILINEAR); x=(z.width-W)//2; y=(z.height-H)//2; c=np.asarray(z.crop((x,y,x+W,y+H))).astype(np.float32)
        acc=c if acc is None else acc+c
    return Image.fromarray((acc/nn).astype(np.uint8))
def s08a(n,fr,m,t):
    # zoom into cafe reel card
    base=Image.new('RGB',(W,H),(20,20,20)); cc=Image.open('a/p06_catcafe.jpg').convert('RGB').resize((W,int(W*1.5)))
    p=eio(t/0.45); s=0.45+2.2*p
    full=Image.new('RGB',(W,H),(25,25,25)); full.paste(cc,(0,(H-cc.height)//2))
    return zoomblur(full,s,s*(1+0.25*p)).convert('RGBA')
def s08(n,fr,m,t):
    q=clamp(t/0.25)
    return (zoomblur(fr,1.35-0.35*q,1.0) if q<1 else fr).convert('RGBA')
def s09(n,fr,m,t):
    cv=fr.convert('RGBA'); f=F('a/Playfair-Black.ttf',190)
    for word,t0,y in (('YOUR',0.23,300),('TRIP',1.43,480)):
        e=eo((t-t0)/0.3)
        if e<=0: continue
        lay=Image.new('RGBA',(W,H),(0,0,0,0)); dl=ImageDraw.Draw(lay); dl.text((360,y+40*(1-e)),word,font=f,fill=(255,255,255,int(255*e)),anchor='mm')
        sh=lay.filter(ImageFilter.GaussianBlur(12)); sa=sh.getchannel('A').point(lambda v:int(v*0.25)); shd=Image.new('RGBA',(W,H),(0,0,0,255)); shd.putalpha(sa)
        cv.alpha_composite(shd); cv.alpha_composite(lay)
        if n==0: pass
    cv.paste(fr,(0,0),m); return cv
def s10(n,fr,m,t):
    p=eio(t/0.5); x0,y0,x1,y1=[a+(b-a)*p for a,b in zip((0,0,W,H),(95,150,625,1060))]
    out=fr.filter(ImageFilter.GaussianBlur(16)).point(lambda v:int(v*0.42)).convert('RGBA')
    inner=fr.crop((int(x0),int(y0),int(x1),int(y1))).convert('RGBA')
    mk=Image.new('L',inner.size,0); ImageDraw.Draw(mk).rounded_rectangle((0,0,inner.width-1,inner.height-1),int(30*p),fill=255)
    out.paste(inner,(int(x0),int(y0)),mk)
    if p>0.02:
        d=ImageDraw.Draw(out); d.rounded_rectangle((x0,y0,x1,y1),int(30*p),outline=(255,255,255,int(255*p)),width=5)
        ui=Image.new('RGBA',(W,H),(0,0,0,0)); du=ImageDraw.Draw(ui); a=int(255*p)
        for i,(ic,lab) in enumerate([('♥','12.4K'),('●','1,024'),('➤','')]):
            yy=y1-330+i*90; du.text((x1-45,yy),ic,font=F(DJ,40),fill=(255,255,255,a),anchor='mm',stroke_width=2,stroke_fill=(0,0,0,a//2)); du.text((x1-45,yy+38),lab,font=F(INTER_B,18),fill=(255,255,255,a),anchor='mm')
        du.ellipse((x0+24,y1-80,x0+70,y1-34),fill=BR+(a,)); du.text((x0+47,y1-57),'C',font=F(INTER_X,22),fill=(255,255,255,a),anchor='mm')
        du.text((x0+82,y1-57),'steven_chinapal',font=F(INTER_B,22),fill=(255,255,255,a),anchor='lm',stroke_width=1,stroke_fill=(0,0,0,a//3))
        fol='Following' if t>=4.6 else 'Follow'; du.rounded_rectangle((x0+282,y1-74,x0+282+(118 if fol=='Following' else 88),y1-40),10,outline=(255,255,255,a),width=2,fill=(255,255,255,60) if fol=='Following' else None)
        du.text((x0+282+(59 if fol=='Following' else 44),y1-57),fol,font=F(INTER_B,18),fill=(255,255,255,a),anchor='mm')
        out.alpha_composite(ui)
    mm=m.copy(); ImageDraw.Draw(mm).rectangle((0,int(y1),W,H),fill=0)
    out.paste(fr,(0,0),mm)
    if n==0: sfx('10',4.6,'click',0.4)
    if t>=2.32-0.08: cap(out,'10',t,3.14-0.08,y=1035)
    return out
SEGS=[('01','sd/shots/01_couchwall.mp4',0.0,4.5,s01,True),('02','sd/shots/02_orbit.mp4',0.9,3.95,s02,True),('03','sd/shots/03_vertigo.mp4',0.0,3.4,s03,True),
('04','sd/shots/04_uiworld.mp4',1.4,2.45,s04,False),('05','sd/shots/05_checklist.mp4',1.85,3.15,s05,False),('06','sd/shots/06_pullback.mp4',0.0,4.75,s06,False),
('07','sd/shots/07_route.mp4',0.0,4.6,s07,True),('08a','sd/shots/08_cafe.mp4',0.0,0.45,s08a,False),('08','sd/shots/08_cafe.mp4',0.3,2.0,s08,False),
('09','sd/shots/09_cover.mp4',1.55,2.05,s09,True),('10','sd/shots/10_framebreak.mp4',0.0,5.85,s10,True)]
only=sys.argv[1:] 
for name,src,tin,dur,fn,needm in SEGS:
    if only and name not in only: continue
    mk=Masker(); w=writer(f'ed/seg_{name}.mp4'); cnt=0
    for n,fr in frames(src,tin,dur):
        m=mk(fr) if needm else None
        out=fn(n,fr,m,n/FPS).convert('RGB'); w.stdin.write(out.tobytes()); cnt+=1
    w.stdin.close(); w.wait(); print(name,cnt,'frames',flush=True)
old=json.load(open('ed/sfx.json')) if (only and os.path.exists('ed/sfx.json')) else []
old=[s for s in old if s[0] not in only] if only else []
json.dump(old+SFX,open('ed/sfx.json','w'))
