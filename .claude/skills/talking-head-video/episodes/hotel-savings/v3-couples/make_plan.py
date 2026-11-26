import json,sys,os
E=sys.argv[1]; W=json.load(open(f'{E}/words.json')); TL=json.load(open(f'{E}/timeline.json'))
DUR=round(TL[-1]['start']+TL[-1]['dur'],3)
# caption text comes from the script by position (Whisper hears "Common" for "Comment", "ship" for "trip")
TOK=[w for s in TL for w in s['text'].split()]
assert len(TOK)==len(W), (len(TOK),len(W))
def txt(i): return TOK[i]
def t(i): return W[i][0]
SEG={s['k']:s['start'] for s in TL}
MUSIC=json.load(open(f'{E}/music.json')) if os.path.exists(f'{E}/music.json') else {"file":"music_marimba_el.mp3","vol":0}
# every time hangs off a word onset or a segment start, so a re-cut moves everything with the speech
br=[("couple",t(4)-0.04,SEG['B']),
    ("jhotel",t(19)-0.04,t(20)+0.15),("ritz",t(20)+0.15,SEG['C']),
    ("waterfall",t(31)-0.04,SEG['E']),
    ("dinner",t(36)-0.04,SEG['F']),
    ("hanfu",t(41)-0.04,t(43)-0.02),
    ("bund",t(59)-0.04,SEG['I'])]
CREAM=(t(26)-0.03,SEG['D']); NAVY=(SEG['G'],SEG['H'])
EM={6,19,29,31,36,41,55}                      # accent words (red serif on the shirt, white serif over B-roll)
GROUPS=[[0,1,2,3],[4,5,6],
        [18,19,20],
        [21,22,23],[24,25],
        [30],[31,32],
        [33,34,35],[36,37,38],
        [39,40],[41,42],[43,44,45],
        [48,49,50,51],[52,53,54,55],[56,57,58],[59,60,61]]   # B title, cream, navy, fee title and the HOTEL ending carry the rest
TITLE_B=(SEG['B'],t(18)-0.05); TITLE_I=(SEG['I'],SEG['J'])   # hook title holds through 'by directly working' so PRICES reads
BLOCK=[TITLE_B,CREAM,NAVY,TITLE_I]
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
scale={'A':1.0,'B':1.06,'C':1.0,'D':1.1,'E':1.0,'F':1.12,'G':1.0,'H':1.1,'I':1.0,'J':1.0}
whip={'B','C','D','E','F','H','I'}
aroll=[{"k":s['k'],"start":s['start'],"dur":s['dur'],"scale":scale[s['k']],"whip":s['k'] in whip} for s in TL]
broll=[{"id":n,"src":n,"start":round(a,3),"dur":round(b-a,3)} for n,a,b in br]
def W_(i,s=None): return [s or txt(i).lower(),t(i)]
cards=[
 {"kind":"title","start":round(TITLE_B[0],3),"dur":round(TITLE_B[1]-TITLE_B[0],3),"top":1050,"lines":[
   {"style":"serif-red","size":78,"words":[W_(7),W_(8),W_(9),W_(10),W_(11)]},
   {"style":"heavy","size":90,"words":[W_(12),W_(13),W_(14)]}]},
 {"kind":"cream","start":round(CREAM[0],3),"dur":round(CREAM[1]-CREAM[0],3),"words":[[txt(i),t(i)] for i in (26,27,28,29)]},
 {"kind":"navy","start":round(NAVY[0],3),"dur":round(NAVY[1]-NAVY[0],3),"words":[[txt(i),t(i)] for i in (46,47)]},
 {"kind":"title","start":round(TITLE_I[0],3),"dur":round(TITLE_I[1]-TITLE_I[0],3),"top":950,"lines":[
   {"style":"serif-red","size":72,"words":[W_(62),W_(63),W_(64)]},
   {"style":"heavy","size":100,"words":[W_(65),W_(66),W_(67)]},
   {"style":"heavy-red","size":100,"words":[W_(68),W_(69)]},
   {"style":"small-ink","size":56,"words":[W_(70)]}]},
 {"kind":"title","hold":True,"start":round(t(71)-0.05,3),"dur":round(DUR-t(71)+0.05,3),"top":925,"lines":[
   {"style":"small-ink","size":68,"words":[["comment",t(71)]]},
   {"style":"heavy-red","size":218,"slam":True,"words":[["hotel",t(72)]]},
   {"style":"small-ink","size":58,"words":[W_(73),W_(74),W_(75),W_(76)]}]}]
sfx=[["whoosh_es.wav",a-0.10,0.3] for n,a,b in br if n!="ritz"]
sfx+=[["pop_es.wav",t(7)-0.02,0.35],["pop_es.wav",CREAM[0]-0.03,0.35],["pop_es.wav",NAVY[0]-0.03,0.35],["pop_es.wav",t(62)-0.02,0.35],["pop_es.wav",t(72)-0.05,0.55]]
sfx=[[f,round(a,3),v] for f,a,v in sfx]
json.dump({"logo":True,"duration":DUR,"aroll":aroll,"broll":broll,"captions":caps,"cards":cards,"sfx":sfx,"cap_top":1060,
           "music":MUSIC},open(f'{E}/plan.json','w'),indent=1)
for c in caps: print(f"{c['start']:6.2f}-{c['end']:6.2f}  "+' '.join(w[0]+('*' if w[2] else '') for w in c['words']))
print('broll',[(n,round(a,2),round(b-a,2)) for n,a,b in br]); print('duration',DUR)
