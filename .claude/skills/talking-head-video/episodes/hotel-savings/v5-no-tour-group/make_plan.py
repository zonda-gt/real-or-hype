import json,sys,os
E=sys.argv[1]; W=json.load(open(f'{E}/words.json')); TL=json.load(open(f'{E}/timeline.json'))
DUR=round(TL[-1]['start']+TL[-1]['dur'],3)
FIX={20:'personalize',22:'itinerary,',44:'traveling',49:'organize',51:'yourself.',66:'already',69:'concierge'}  # Whisper spelling/mishears; captions follow what he says
def txt(i): return FIX.get(i,W[i][2])
def t(i): return W[i][0]
SEG={s['k']:s['start'] for s in TL}
CUT={s['k']:s['src_in'] for s in TL}
T_FEE=SEG['G']+(93.04-CUT['G'])               # "fee": Whisper folds it into "concierge"; onset from the envelope (source 93.04 s)
MUSIC=json.load(open(f'{E}/music.json')) if os.path.exists(f'{E}/music.json') else {"file":"music_marimba_el.mp3","vol":0}
# every time hangs off a word onset or a segment start
br=[("tourgroup",t(5)-0.04,t(9)-0.05),("hotpot",t(31)-0.05,t(33)),("solo",t(42)-0.05,SEG['E']),("jhotel",t(56)-0.04,t(58))]
TITLE_A=(t(9)-0.05,SEG['B']); CREAM=(SEG['B'],t(19)-0.03); NAVY=(t(50)-0.04,SEG['F'])
EM={3,31,34,42,55}                            # accent words (red serif on the shirt, white serif over B-roll)
GROUPS=[[0,1,2],[3],[4,5],[6,7,8],[19,20],[21,22],[23,24,25],[26,27],[28,29,30],[31,32],[33,34,35],[36,37,38],
        [39,40,41],[42],[43,44],[45],[46,47,48],[49],[52,53,54],[55,56,57],[58,59]]
BLOCK=[TITLE_A,CREAM,NAVY,(SEG['G'],SEG['H']),(SEG['H'],DUR)]
caps=[]
for gi,g in enumerate(GROUPS):
    st=max(0.1,t(g[0])-0.05)
    nxt=t(GROUPS[gi+1][0])-0.05 if gi+1<len(GROUPS) else DUR
    en=min(nxt, W[g[-1]][1]+0.35) if nxt-W[g[-1]][1]>0.5 else nxt
    for a,b in BLOCK:
        if st<a<en: en=a
        if a<=st<b: st=b
    en=min(en,DUR)
    onb=any(min(en,b)-max(st,a)>0.2 for _,a,b in br)    # caption over B-roll for > 0.2 s: white serif accent
    caps.append({"start":round(st,3),"end":round(en,3),"words":[[txt(i),t(i),('emw' if onb else 'em') if i in EM else ''] for i in g]})
scale={'A':1.0,'B':1.12,'C':1.0,'D':1.1,'E':1.0,'F':1.12,'G':1.0,'H':1.0}
whip={'B','D','E','F','G','H'}
aroll=[{"k":s['k'],"start":s['start'],"dur":s['dur'],"scale":scale[s['k']],"whip":s['k'] in whip} for s in TL]
broll=[{"id":n,"src":n,"start":round(a,3),"dur":round(b-a,3)} for n,a,b in br]
cards=[
 {"kind":"title","start":round(TITLE_A[0],3),"dur":round(TITLE_A[1]-TITLE_A[0],3),"top":960,"lines":[
   {"style":"heavy","size":104,"words":[["or",t(9)],["spend",t(10)]]},
   {"style":"heavy-red","size":118,"words":[["thousands",t(11)]]},
   {"style":"serif-red","size":80,"words":[["on",t(12)],["a",t(13)],["private",t(14)],["tour?",t(15)]]}]},
 {"kind":"cream","start":round(CREAM[0],3),"dur":round(CREAM[1]-CREAM[0],3),"words":[["for",t(16)],["just",t(17)],["$89",t(18),300]]},
 {"kind":"navy","start":round(NAVY[0],3),"dur":round(NAVY[1]-NAVY[0],3),"words":[["everything",t(50)],["yourself.",t(51)]]},
 {"kind":"title","start":SEG["G"],"dur":round(SEG["H"]-SEG["G"],3),"top":990,"lines":[
   {"style":"serif-red","size":76,"words":[["so",t(60)],["your",t(61)],["hotel",t(62)],["savings",t(63)],["alone",t(64)]]},
   {"style":"heavy","size":92,"words":[["can",t(65)],["already",t(66)],["cover",t(67)]]},
   {"style":"heavy-red","size":92,"words":[["our",t(68)],["concierge",t(69)],["fee.",T_FEE]]}]},
 {"kind":"title","hold":True,"start":round(t(70)-0.05,3),"dur":round(DUR-t(70)+0.05,3),"top":925,"lines":[
   {"style":"small-ink","size":68,"words":[["comment",t(70)]]},
   {"style":"heavy-red","size":218,"slam":True,"words":[["hotel",t(71)]]},
   {"style":"small-ink","size":58,"words":[["below",t(72)],["to",t(73)],["find",t(74)],["out",t(75)],["more.",t(76)]]}]}]
sfx=[["whoosh_es.wav",br[0][1]-0.12,0.35],["whoosh_es.wav",br[1][1]-0.10,0.3],["whoosh_es.wav",br[2][1]-0.10,0.3],
     ["pop_es.wav",t(9)-0.02,0.35],["pop_es.wav",CREAM[0]-0.03,0.4],["pop_es.wav",NAVY[0]-0.03,0.35],["pop_es.wav",t(60)-0.02,0.35],["pop_es.wav",t(71)-0.05,0.55]]
sfx=[[f,round(max(0,a),3),v] for f,a,v in sfx]
json.dump({"logo":True,"duration":DUR,"aroll":aroll,"broll":broll,"captions":caps,"cards":cards,"sfx":sfx,"cap_top":1060,
           "music":MUSIC},open(f'{E}/plan.json','w'),indent=1)
for c in caps: print(f"{c['start']:6.2f}-{c['end']:6.2f}  "+' '.join(w[0] for w in c['words']))
print('broll',broll); print('fee',round(T_FEE,2),'duration',DUR)
