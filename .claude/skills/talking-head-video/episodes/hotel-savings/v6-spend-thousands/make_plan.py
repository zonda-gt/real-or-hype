import json,sys,os
E=sys.argv[1]; W=json.load(open(f'{E}/words.json')); TL=json.load(open(f'{E}/timeline.json'))
DUR=round(TL[-1]['start']+TL[-1]['dur'],3)
FIX={37:'bookings'}                           # Whisper mishears; captions follow what he says
def txt(i): return FIX.get(i,W[i][2])
def t(i): return W[i][0]
SEG={s['k']:s['start'] for s in TL}
MUSIC=json.load(open(f'{E}/music.json')) if os.path.exists(f'{E}/music.json') else {"file":"music_marimba_el.mp3","vol":0}
# every time below hangs off a word onset or a segment start, so re-cuts move everything with the speech
br=[("jview",t(6)-0.04,t(10)-0.04),("ritz",t(17)-0.04,t(19)),
    ("train",t(37)-0.04,SEG['E']),("hotpot",t(43)-0.04,t(45)-0.04),("localrest",t(45)-0.04,SEG['F']),
    ("bund",t(70)-0.04,SEG['H'])]
HOOK=(SEG['A'],br[0][1])
NAVY=(t(10)-0.04,SEG['B']); CREAM1=(t(21)-0.03,t(23)-0.02); CREAM2=(t(64)-0.03,t(66)-0.02)
EM={9,17,20,34,43,69}                         # accent words (red serif on the shirt, white serif over B-roll)
GROUPS=[[6,7],[8,9],[13,14,15],[16,17,18],[19,20],[23,24],[25,26,27,28],[29,30,31],[32,33,34],
        [35,36],[37,38],[39,40,41],[42,43],[44,45],[46,47,48,49],[60,61,62,63],[66,67,68,69],[70,71]]
BLOCK=[HOOK,NAVY,CREAM1,(SEG['F'],SEG['G']),CREAM2,(t(72)-0.05,DUR)]   # full cards / titles: no captions
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
scale={'A':1.0,'B':1.12,'C':1.0,'D':1.08,'E':1.0,'F':1.0,'G':1.12,'H':1.0}
whip={'B','D','E','F','G','H'}
aroll=[{"k":s['k'],"start":s['start'],"dur":s['dur'],"scale":scale[s['k']],"whip":s['k'] in whip} for s in TL]
broll=[{"id":n,"src":n,"start":round(a,3),"dur":round(b-a,3)} for n,a,b in br]
cards=[
 {"kind":"title","start":HOOK[0],"dur":round(HOOK[1]-HOOK[0],3),"top":975,"lines":[
   {"style":"small-ink","size":60,"words":[["before",t(0)],["you",t(1)],["spend",t(2)]]},
   {"style":"heavy-red","size":140,"slam":True,"words":[["thousands",t(3)]]},
   {"style":"heavy","size":84,"words":[["of",t(4)],["dollars",t(5)]]}]},
 {"kind":"navy","start":round(NAVY[0],3),"dur":round(NAVY[1]-NAVY[0],3),"words":[["hear",t(10)],["me",t(11)],["out.",t(12)]]},
 {"kind":"cream","start":round(CREAM1[0],3),"dur":round(CREAM1[1]-CREAM1[0],3),"words":[["better",t(21)],["prices",t(22)]]},
 {"kind":"title","start":SEG["F"],"dur":round(SEG["G"]-SEG["F"],3),"top":1012,"lines":[
   {"style":"small-ink","size":56,"words":[["we",t(50)],["will",t(51)],["pass",t(52)],["down",t(53)]]},
   {"style":"serif-ink","size":70,"words":[["the",t(54)],["hotel",t(55)],["savings",t(56)]]},
   {"style":"heavy-red","size":108,"slam":True,"words":[["all",t(57)],["to",t(58)],["you.",t(59)]]}]},
 {"kind":"cream","start":round(CREAM2[0],3),"dur":round(CREAM2[1]-CREAM2[0],3),"words":[["less",t(64)],["money,",t(65)]]},
 {"kind":"title","hold":True,"start":round(t(72)-0.05,3),"dur":round(DUR-t(72)+0.05,3),"top":925,"lines":[
   {"style":"small-ink","size":64,"words":[["comment",t(72)]]},
   {"style":"heavy-red","size":190,"slam":True,"words":[["hotel",t(75)]]},
   {"style":"small-ink","size":50,"words":[["below",t(76)],["and",t(77)],["we",t(78)],["will",t(79)],["check",t(80)],["how",t(81)],["much",t(82)]]},
   {"style":"small-ink","size":50,"words":[["you",t(83)],["can",t(84)],["save",t(85)],["on",t(86)],["your",t(87)],["China",t(88)],["trip.",t(89)]]}]}]
sfx=[["whoosh_es.wav",br[0][1]-0.12,0.35],["whoosh_es.wav",br[1][1]-0.10,0.3],["whoosh_es.wav",br[2][1]-0.08,0.3],["whoosh_es.wav",br[5][1]-0.08,0.3],
     ["pop_es.wav",t(3)-0.02,0.4],["pop_es.wav",NAVY[0]-0.03,0.35],["pop_es.wav",CREAM1[0]-0.03,0.35],["pop_es.wav",t(57)-0.02,0.4],
     ["pop_es.wav",CREAM2[0]-0.03,0.35],["pop_es.wav",t(75)-0.05,0.55]]
sfx=[[f,round(a,3),v] for f,a,v in sfx]
json.dump({"logo":True,"duration":DUR,"aroll":aroll,"broll":broll,"captions":caps,"cards":cards,"sfx":sfx,"cap_top":1060,
           "music":MUSIC},open(f'{E}/plan.json','w'),indent=1)
for c in caps: print(f"{c['start']:6.2f}-{c['end']:6.2f}  "+' '.join(w[0]+('*' if w[2] else '') for w in c['words']))
print('broll',[(b['id'],b['start'],b['dur']) for b in broll]); print('duration',DUR)
