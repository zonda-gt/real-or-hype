import json,sys
# Hotel savings v4 (solo traveller). Modelled on ep1's plan; every time hangs off a word onset or segment start.
E=sys.argv[1]; W=json.load(open(f'{E}/words.json')); TL=json.load(open(f'{E}/timeline.json'))
DUR=round(TL[-1]['start']+TL[-1]['dur'],3)
FIX={}                                        # words.json already carries the script text (per-segment timing)
def txt(i): return FIX.get(i,W[i][2])
def t(i): return W[i][0]
SEG={s['k']:s['start'] for s in TL}
MUSIC=json.load(open(f'{E}/music.json')) if __import__('os').path.exists(f'{E}/music.json') else {"file":"music_marimba_el.mp3","vol":0.25}
br=[("clouds",t(3)-0.04,SEG['B']),                       # "alone?"  - backpacker alone above a sea of clouds
    ("jhotel",t(16)-0.04,t(17)),("ritz",t(17),t(20)-0.03),  # "hotels to get you"
    ("train",t(34)-0.04,t(36)),("bund",t(36),SEG['F']),     # "trains and" / "attractions."
    ("station",t(42)-0.04,t(45)),                           # "lost, confused or" - packed Hangzhou East hall
    ("phone",t(55)-0.04,SEG['I']),                          # "send us a message."
    ("backpack",SEG['I'],SEG['J'])]                         # "Travel independently,"
CREAM=(t(20)-0.03,SEG['D']); NAVY=(t(29)-0.04,SEG['E'])
EM={3,16,42,52,60,64}                         # accent words: alone?, hotels, lost, support, independently, local
GROUPS=[[0,1],[2,3],[12,13,14],[15,16],[17,18,19],[22,23,24],[25,26,27],[28],
        [31,32,33],[34,35],[36],[37,38,39],[40,41,42],[43,44],[45,46],[47,48],
        [49,50,51],[52,53],[54,55,56],[57,58],[59,60],[61,62,63],[64,65],[66,67,68]]
BLOCK=[(SEG['B'],SEG['C']),CREAM,NAVY,(SEG['K'],SEG['L'])]   # full cards / titles: no captions
caps=[]
for gi,g in enumerate(GROUPS):
    st=max(0.1,t(g[0])-0.05)
    nxt=t(GROUPS[gi+1][0])-0.05 if gi+1<len(GROUPS) else SEG['K']
    en=min(nxt, W[g[-1]][1]+0.35) if nxt-W[g[-1]][1]>0.5 else nxt
    for a,b in BLOCK:
        if st<a<en: en=a
        if a<=st<b: st=b
    en=min(en,DUR)
    onb=lambda i: any(a-0.05<=t(i)<b for _,a,b in br)
    caps.append({"start":round(st,3),"end":round(en,3),"words":[[txt(i),t(i),('emw' if onb(i) else 'em') if i in EM else ''] for i in g]})
scale={'A':1.0,'B':1.14,'C':1.0,'D':1.1,'E':1.0,'F':1.0,'G':1.15,'H':1.0,'I':1.0,'J':1.06,'K':1.0,'L':1.0,'M':1.06}
whip={'B','D','E','F','G','J','K'}
aroll=[{"k":s['k'],"start":s['start'],"dur":s['dur'],"scale":scale[s['k']],"whip":s['k'] in whip} for s in TL]
broll=[{"id":n,"src":n,"start":round(a,3),"dur":round(b-a,3)} for n,a,b in br]
cards=[
 {"kind":"title","start":SEG["B"],"dur":round(SEG["C"]-SEG["B"],3),"top":1000,"lines":[
   {"style":"small-ink","size":72,"words":[["you",t(4)],["don't",t(5)],["need",t(6)],["to",t(7)]]},
   {"style":"heavy","size":138,"words":[["figure",t(8)],["out",t(9)]]},
   {"style":"serif-red","size":96,"words":[["everything",t(10)],["yourself.",t(11)]]}]},
 {"kind":"cream","start":round(CREAM[0],3),"dur":round(CREAM[1]-CREAM[0],3),"words":[["better",t(20)],["prices.",t(21)]]},
 {"kind":"navy","start":round(NAVY[0],3),"dur":round(NAVY[1]-NAVY[0],3),"words":[["your",t(29)],["interest.",t(30)]]},
 {"kind":"title","start":SEG["K"],"dur":round(SEG["L"]-SEG["K"],3),"top":935,"lines":[
   {"style":"serif-red","size":72,"words":[["your",t(70)],["hotel",t(71)],["savings",t(72)],["could",t(73)]]},
   {"style":"heavy","size":112,"words":[["cover",t(74)],["our",t(75)]]},
   {"style":"heavy-red","size":104,"words":[["concierge",t(76)],["fee",t(77)]]},
   {"style":"serif-red","size":62,"words":[["alone.",t(78)]]}]},
 {"kind":"title","hold":True,"start":round(max(t(79)-0.05,SEG['L']),3),"dur":round(DUR-max(t(79)-0.05,SEG['L']),3),"top":925,"lines":[
   {"style":"small-ink","size":68,"words":[["comment",t(79)]]},
   {"style":"heavy-red","size":218,"slam":True,"words":[["hotel",t(80)]]},
   {"style":"small-ink","size":58,"words":[["to",t(81)],["get",t(82)],["more",t(83)],["info.",t(84)]]}]}]
sfx=[["whoosh_es.wav",br[0][1]-0.12,0.35],["whoosh_es.wav",br[1][1]-0.10,0.3],["whoosh_es.wav",br[3][1]-0.08,0.3],
     ["whoosh_es.wav",br[5][1]-0.08,0.3],["whoosh_es.wav",br[6][1]-0.08,0.25],
     ["pop_es.wav",t(4)-0.02,0.35],["pop_es.wav",CREAM[0]-0.03,0.35],["pop_es.wav",NAVY[0]-0.03,0.35],["pop_es.wav",t(70)-0.02,0.35],["pop_es.wav",t(80)-0.05,0.55]]
sfx=[[f,round(a,3),v] for f,a,v in sfx]
json.dump({"logo":True,"duration":DUR,"aroll":aroll,"broll":broll,"captions":caps,"cards":cards,"sfx":sfx,"cap_top":1060,
           "music":MUSIC},open(f'{E}/plan.json','w'),indent=1)
for c in caps: print(f"{c['start']:6.2f}-{c['end']:6.2f}  "+' '.join(w[0]+('*' if w[2] else '') for w in c['words']))
for b in broll: print('broll',b['id'],b['start'],b['dur'])
print('duration',DUR)
