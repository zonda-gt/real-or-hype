# Real or Hype — 1000 Trees trial-reel variants. Only the hook / angle changes.
V='VID_20260910_'
OUT=[('O1','clip',('IMG_4775',13.0,0.0),2.35,'station'),
     ('O2','clip',(V+'162824_003',0.4,0.15),0.75,'bike'),
     ('O3','clip',(V+'162824_003',4.9,0.15),1.55,None)]
MID=[('O5','panel',(V+'164346_011',0,4.4),2.6,'green'),
     ('O6','clip',(V+'173344_017',15.4,0.15),1.45,'pillar'),
     ('O7','clip',(V+'164338_010',0,0.15),1.5,None),
     ('O8','clip',(V+'173429_020',19,0.15),2.0,'close'),
     ('M1','clip',('IMG_4806',0.4,0.3),1.0,None),
     ('E1','talk',('IMG_4837',1.6,1.0,1.4),2.76,None),
     ('A1','clip',('IMG_4854',5.4,0.15),1.0,'inside'),
     ('A3','talk',('IMG_4855',33.86,1.0,1.4),0.99,None),
     ('A3b','talk',('IMG_4855',25.50,1.0,1.4),1.286,None),
     ('I2','clip',(V+'173521_022',15,0.15),1.6,'gorilla2')]
END=[('R1','clip',(V+'173552_023',9.5,0.1),2.9,'far'),
     ('R2','clip',(V+'175052_051',2.5,0.1),2.75,'skip'),
     ('V1','clip',('IMG_4793',0,0.15),3.2,'verdict')]
HOOK=[('H1','hook',None,5.3,None),('H2','react',(10.6,),2.0,None)]
S={
 # A: claim hook (the posted v14 edit)
 'A': HOOK+OUT+MID+[('I3','clip',('IMG_4842',35,0.1),0.95,'thisbike'),('I4','price',('IMG_4842',50.3,57.2),1.5,None)]+END,
 # B: price-shock hook -- open on the $20,000 price tag, then the claim
 'B': [('B1','price',('IMG_4842',50.3,57.2),1.5,None)]+HOOK+OUT+MID+[('I6','clip',(V+'173621_024',23.5,0.15),1.2,None)]+END,
 # C: how-to-get-there guide -- exact route + best photo spot, then the verdict
 'C': HOOK+[('O1','clip',('IMG_4775',13.0,0.0),3.4,'station_c')]+OUT[1:]+[('P1','talk',('IMG_4815',3.30,1.0,1.4),3.04,None)]
      +[x for x in MID if x[0] not in ('I2',)]+END,
}
VODIR='vo_liam'   # narration voice: ElevenLabs 'Liam' (TX3LPaxmHKxFdv7VOQHJ), eleven_multilingual_v2, atempo 1.12
HOOKVO={'A':VODIR+'/hook.wav','B':VODIR+'/hook_b.wav','C':VODIR+'/hook_c.wav'}
def ovs(var,st,total):
    o=[('p1.png',st['H2'],st['H2']+0.45),('p2.png',st['H2']+0.45,st['H2']+0.93),('p3.png',st['H2']+0.93,st['O1']),
       ('bar.png',st['O1'],st['V1']),('l_station.png',st['O1'],st['O2']),
       ('v1.png',st['V1']+TICKS[var][0],total),('v2.png',st['V1']+TICKS[var][1],total)]
    if 'I4' in st: o.append(('p20k.png',st['I4']+0.1,st['R1']))
    if 'B1' in st: o.append(('p20k.png',st['B1']+0.1,st['H1']))
    if 'P1' in st: o.append(('l_photo.png',st['P1'],st['O5']))
    return o

# D: A's edit with a script in the "you-hook + open loops + closing question" formula (another creator's style, adapted)
_D_KEYS={'station':'d_station','bike':'d_bike','green':'d_green','pillar':'d_pillar','close':'d_close','inside':'d_inside',
         'thisbike':'d_thisbike','far':'d_far','skip':'d_skip','verdict':'d_verdict'}
_D_DUR={'O1':3.02,'O7':2.3,'O8':2.4,'A1':1.08,'I3':1.0,'R1':3.28,'R2':2.8,'V1':3.85}
S['D']=[(sid,k,a,_D_DUR.get(sid,d),_D_KEYS.get(key,key)) for sid,k,a,d,key in S['A'] if sid not in ('M1','I2')]
HOOKVO['D']=VODIR+'/d_hook.wav'

# when the green REAL and red HYPE ticks appear, seconds after V1 starts (on the spoken words)
TICKS={'A':(1.1,2.0),'B':(1.1,2.0),'C':(1.1,2.0),'D':(1.0,2.26)}

# D2: D's body with a minimal hook line that only names the place (the reaction + sting are the hook)
S['D2']=list(S['D']); HOOKVO['D2']=VODIR+'/d2_hook.wav'; TICKS['D2']=TICKS['D']
