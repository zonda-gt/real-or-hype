import json,sys
E=sys.argv[1]; W=json.load(open(f'{E}/words.json')); TL=json.load(open(f'{E}/timeline.json'))
DUR=round(TL[-1]['start']+TL[-1]['dur'],3)
FIX={4:'China?',26:'family-friendly',30:'your',68:'savings'}   # what he says (Whisper splits / mishears)
TFIX={29:9.98}                                                  # onset from the envelope (Whisper put "design" 0.26 s late)
def txt(i): return FIX.get(i,W[i][2])
def t(i): return TFIX.get(i,W[i][0])
SEG={s['k']:s['start'] for s in TL}
T_COMMENT,T_HOTEL=25.99,26.50                                   # J: "Comment hotel" (Whisper heard "Come to the hotel"), envelope onsets
MUSIC=json.load(open(f'{E}/music.json'))
br=[("shoulders",t(2)-0.04,t(5)-0.08),("jhotel",t(15)-0.04,t(17)),("ritz",t(17),t(21)-0.03),
    ("kidsuite",t(26)-0.04,t(28)),("slideroom",t(28),SEG['D']),("fireworks",t(38)-0.03,t(40)),("hotpot",t(40),SEG['F']),
    ("buswave",t(57)-0.04,t(60)),("running",t(60),SEG['I'])]
CREAM=(t(21)-0.03,SEG['C']); NAVY=(t(34)-0.04,SEG['E']); HOOK=(t(5)-0.08,SEG['B'])
EM={2,15,26,45,53,57}
GROUPS=[[0,1],[2],[3,4],[11,12,13],[14,15,16],[17,18,19,20],[23,24,25],[26,28],[29,30,31],[32,33],
        [36,37,38],[39,40],[41],[42,43,44,45],[46,47],[48,49],[50,51,52],[53],[54,55,56],[57],[58,59],[60,61,62],[63,64]]
BLOCK=[HOOK,CREAM,NAVY,(SEG['I'],SEG['J']),(SEG['J'],DUR)]
caps=[]
for gi,g in enumerate(GROUPS):
    st=max(0.1,t(g[0])-0.05)
    nxt=t(GROUPS[gi+1][0])-0.05 if gi+1<len(GROUPS) else DUR
    en=min(nxt, W[g[-1]][1]+0.35) if nxt-W[g[-1]][1]>0.5 else nxt
    for a,b in BLOCK:
        if st<a<en: en=a
        if a<=st<b: st=b
    en=min(en,DUR)
    onb=lambda i: any(a-0.05<=t(i)<b for _,a,b in br)
    caps.append({"start":round(st,3),"end":round(en,3),"words":[[txt(i),t(i),('emw' if onb(i) else 'em') if i in EM else ''] for i in g]})
scale={'A':1.0,'B':1.14,'C':1.0,'D':1.1,'E':1.0,'F':1.12,'G':1.0,'H':1.1,'I':1.0,'J':1.0}
whip={'B','E','F','H','I','J'}
aroll=[{"k":s['k'],"start":s['start'],"dur":s['dur'],"scale":scale[s['k']],"whip":s['k'] in whip} for s in TL]
broll=[{"id":n,"src":n,"start":round(a,3),"dur":round(b-a,3)} for n,a,b in br]
cards=[
 {"kind":"title","start":round(HOOK[0],3),"dur":round(HOOK[1]-HOOK[0],3),"top":1030,"lines":[
   {"style":"heavy","size":134,"words":[["Don't",t(5)],["book",t(6)]]},
   {"style":"heavy","size":134,"words":[["your",t(7)],["hotel",t(8)]]},
   {"style":"serif-red","size":124,"words":[["just",t(9)],["yet.",t(10)]]}]},
 {"kind":"cream","start":round(CREAM[0],3),"dur":round(CREAM[1]-CREAM[0],3),"words":[["better",t(21)],["price.",t(22)]]},
 {"kind":"navy","start":round(NAVY[0],3),"dur":round(NAVY[1]-NAVY[0],3),"words":[["children's",t(34)],["needs,",t(35)]]},
 {"kind":"title","start":SEG["I"],"dur":round(SEG["J"]-SEG["I"],3),"top":990,"lines":[
   {"style":"serif-red","size":72,"words":[["your",t(66)],["hotel",t(67)],["savings",t(68)],["alone",t(69)]]},
   {"style":"heavy","size":96,"words":[["can",t(70)],["cover",t(71)],["our",t(72)]]},
   {"style":"heavy-red","size":96,"words":[["concierge",t(73)],["fee.",t(74)]]}]},
 {"kind":"title","hold":True,"start":round(T_COMMENT-0.05,3),"dur":round(DUR-T_COMMENT+0.05,3),"top":960,"lines":[
   {"style":"small-ink","size":62,"words":[["comment",T_COMMENT]]},
   {"style":"heavy-red","size":200,"slam":True,"words":[["hotel",T_HOTEL]]},
   {"style":"small-ink","size":52,"words":[["and",t(79)],["I'll",t(80)],["send",t(81)],["you",t(82)],["the",t(83)],["details.",t(84)]]}]}]
sfx=[["whoosh_es.wav",br[0][1]-0.12,0.35],["whoosh_es.wav",br[1][1]-0.10,0.3],["whoosh_es.wav",br[3][1]-0.10,0.3],
     ["whoosh_es.wav",br[5][1]-0.08,0.3],["whoosh_es.wav",br[7][1]-0.10,0.3],
     ["pop_es.wav",t(5)-0.02,0.35],["pop_es.wav",CREAM[0]-0.03,0.35],["pop_es.wav",NAVY[0]-0.03,0.35],["pop_es.wav",t(66)-0.02,0.35],["pop_es.wav",T_HOTEL-0.05,0.55]]
sfx=[[f,round(a,3),v] for f,a,v in sfx]
json.dump({"logo":True,"duration":DUR,"aroll":aroll,"broll":broll,"captions":caps,"cards":cards,"sfx":sfx,"cap_top":1060,
           "music":MUSIC},open(f'{E}/plan.json','w'),indent=1)
for c in caps: print(f"{c['start']:6.2f}-{c['end']:6.2f}  "+' '.join(w[0]+('*' if w[2] else '') for w in c['words']))
print('broll',[(n,round(a,2),round(b-a,2)) for n,a,b in br]); print('duration',DUR)
