import sys; sys.argv=[sys.argv[0]]; exec(open('hook_mock.py').read().split("bg,top,big,out=sys.argv[1:5]")[0])
def opt1(bg,top,big,cy,tsz=86,bsz=136):
    im=Image.open(bg).convert('RGBA').resize((1080,1920))
    y=boxed(im,top,SERIF,tsz,cy,WHITE,padx=30,pady=14); boxed(im,big,SERIF,bsz,y+int(bsz*0.62),YEL,padx=32,pady=14); return im.convert('RGB')
def cur(bg,lines,tag,y0=760):
    im=Image.open(bg).convert('RGBA').resize((1080,1920)); y=y0
    for k,l in enumerate(lines): y=boxed(im,l,SERIF,108 if k==0 else 132,y+60,YEL)
    d=ImageDraw.Draw(im); f=F(HAND,62); w=d.textlength(tag,font=f); d.text((640-w/2,y+70),tag,font=f,fill=WHITE,stroke_width=6,stroke_fill=(40,30,20)); return im.convert('RGB')
def sheet(ims,labels,out):
    W=Image.new('RGB',(len(ims)*550,1030),(30,30,30)); d=ImageDraw.Draw(W)
    for k,(im,l) in enumerate(zip(ims,labels)): W.paste(im.resize((540,960)),(k*550,60)); d.text((k*550+10,10),l,font=F(POP,32),fill=WHITE)
    W.save(out)
TB,BB="My health check-up in China","Expected vs Reality"
sheet([cur('hookB.png',["WHAT I EXPECTED","vs What I Got"],"health check-up in Shanghai")]+[opt1(f,TB,BB,1150) for f in ['hookB.png','hookB_2.6.png','hookB_3.6.png','hookB_5.0.png']],
      ['B now','B new 0.0s','B new 2.6s','B new 3.6s','B new 5.0s'],'mockB2.png')
TA,BA="My health check-up in Shanghai","6 Doctors, 1 Morning"
sheet([cur('hookA.png',["6 DOCTORS","One Morning Check-up"],"in Shanghai"),opt1('hookA.png',TA,BA,800),opt1('hookA.png',TA,BA,880)],['A now','A new (y 800)','A new (y 880)'],'mockA2.png')
