from PIL import Image,ImageDraw,ImageFont
import glob,subprocess,textwrap
def F(sz,b=True): return ImageFont.truetype(subprocess.run(['fc-match','-f','%{file}','Inter:'+('bold' if b else 'regular')],capture_output=True,text=True).stdout,sz)
L=[("01","Couch wall","0–2 s","\"You've saved hundreds of reels…\"","Your saved reels pin to the wall behind you"),
("02","Orbit","2–4 s","\"…rooftop bars, dumpling spots, that café…\"","The reels lift off and circle you"),
("03","Vertigo","4–5.5 s","\"And you've been to none of them.\"","Room stretches, you stay still (dolly zoom)"),
("04","UI world","5.5–8 s","\"So just send them all to us.\"","Reels fly into the DM with @steven_chinapal"),
("05","Checklist","8–10 s","\"Save the reel. Send it to us. That's it.\"","Items tick off as you count"),
("06","Pull-back reveal","10–14 s","\"We turn them into a day-by-day plan…\"","Your shot shrinks into the trip being built, 0→100%"),
("07","Route grow","14–18 s","\"…built around your reels.\"","Day 1 route draws across the wall, pins drop"),
("08","Zoom-through cut","18–19 s","(no line)","Zoom into the café reel → land on you AT the café"),
("09","Cover story","19–21 s","\"Your trip.\"","Big title behind your head"),
("10","Frame break","21–25 s","\"Comment TRIP and I'll send you the link.\"","You reach out of the reel frame")]
fs=sorted(glob.glob('out/frame_*.png')); TW,TH,C,PAD,LH=360,640,5,24,150
pg=Image.new('RGB',(C*(TW+PAD)+PAD,90+2*(TH+LH+PAD)),'#111'); d=ImageDraw.Draw(pg)
d.text((PAD,24),'ChinaPal · storyboard (AI stand-in, placeholder app screens)',fill='#fff',font=F(34))
for i,f in enumerate(fs):
    x=PAD+(i%C)*(TW+PAD); y=90+(i//C)*(TH+LH+PAD); pg.paste(Image.open(f).convert('RGB').resize((TW,TH),Image.LANCZOS),(x,y))
    n,e,t,line,what=L[i]; d.text((x,y+TH+10),f'{n}  {e}',fill='#FFD43B',font=F(26)); d.text((x+TW,y+TH+14),t,fill='#aaa',font=F(20,False),anchor='ra')
    d.text((x,y+TH+48),line,fill='#fff',font=F(17,False))
    for k,w in enumerate(textwrap.wrap(what,38)): d.text((x,y+TH+78+k*24),w,fill='#bbb',font=F(17,False))
pg.save('storyboard.jpg',quality=90)
names=[('saved','1 · Saved reels'),('dm_sending','2 · Sending reels in DM'),('dm','3 · Our reply + trip link'),('building','4 · Building the trip'),('itinerary','5 · Itinerary page')]
W,H=int(390*1.6),int(844*1.6); sc=Image.new('RGB',(5*(W+PAD)+PAD,H+120),'#111'); d=ImageDraw.Draw(sc)
for i,(n,t) in enumerate(names):
    x=PAD+i*(W+PAD); sc.paste(Image.open(f'out/screen_{n}.png').convert('RGB').resize((W,H),Image.LANCZOS),(x,80)); d.text((x,24),t,fill='#FFD43B',font=F(30))
sc.save('screens.jpg',quality=90)
