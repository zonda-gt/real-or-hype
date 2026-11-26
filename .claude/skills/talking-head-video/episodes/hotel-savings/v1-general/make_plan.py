import json,sys
E=sys.argv[1]; W=json.load(open(f'{E}/words.json')); TL=json.load(open(f'{E}/timeline.json'))
DUR=round(TL[-1]['start']+TL[-1]['dur'],3)
FIX={30:'a',57:'alone'}                       # Whisper mishears; captions follow what he says
def txt(i): return FIX.get(i,W[i][2])
def t(i): return W[i][0]
SEG={s['k']:s['start'] for s in TL}
MUSIC=json.load(open(f'{E}/music.json')) if __import__('os').path.exists(f'{E}/music.json') else {"file":"music_marimba_el.mp3","vol":0.25}
# every time below hangs off a word onset or a segment start, so re-cuts move everything with the speech
br=[("skyline",t(4)-0.04,SEG['B']),("jhotel",t(15)-0.04,t(17)),("ritz",t(17),t(21)-0.03),
    ("train",t(37)-0.02,t(40)),("bund",t(40),t(42)),("hotpot",t(42),SEG['F'])]
CREAM=(t(21)-0.03,t(23)-0.02); NAVY=(t(35)-0.04,SEG['E'])
EM={4,15,34,51}                               # red serif accent words
GROUPS=[[0,1,2],[3,4],[11,12,13],[14,15,16],[17,18,19,20],[23,24],[25,26],[27,28,29],[30,31,32],[33,34],
        [37,38,39],[40],[41,42,43],[44],[45,46,47],[48,49,50],[51,52,53]]   # 63-69 "Comment hotel below to find out more" is told by the CTA itself
BLOCK=[(SEG['B'],SEG['C']),CREAM,NAVY,(SEG['G'],SEG['H'])]   # full cards / titles: no captions
caps=[]
for gi,g in enumerate(GROUPS):
    st=max(0.1,t(g[0])-0.05)
    nxt=t(GROUPS[gi+1][0])-0.05 if gi+1<len(GROUPS) else DUR
    en=min(nxt, W[g[-1]][1]+0.35) if nxt-W[g[-1]][1]>0.5 else nxt
    for a,b in BLOCK:
        if st<a<en: en=a
        if a<=st<b: st=b
    en=min(en,DUR)
    onb=lambda i: any(a-0.05<=t(i)<b for _,a,b in br)    # accent word over B-roll: white serif, red only on the black shirt
    cap={"start":round(st,3),"end":round(en,3),"words":[[txt(i),t(i),('emw' if onb(i) else 'em') if i in EM else ''] for i in g]}
    if g[0]>=63: cap["top"]=1150          # under the comment pill
    caps.append(cap)
scale={'A':1.0,'B':1.14,'C':1.0,'D':1.1,'E':1.0,'F':1.15,'G':1.0,'H':1.0,'I':1.06}
whip={'B','F','E','G','H'}
aroll=[{"k":s['k'],"start":s['start'],"dur":s['dur'],"scale":scale[s['k']],"whip":s['k'] in whip} for s in TL]
broll=[{"id":n,"src":n,"start":round(a,3),"dur":round(b-a,3)} for n,a,b in br]
cards=[
 {"kind":"title","start":SEG["B"],"dur":round(SEG["C"]-SEG["B"],3),"top":1030,"lines":[
   {"style":"heavy","size":134,"words":[["Don't",t(5)],["book",t(6)]]},
   {"style":"heavy","size":134,"words":[["your",t(7)],["hotel",t(8)]]},
   {"style":"serif-red","size":124,"words":[["just",t(9)],["yet.",t(10)]]}]},
 {"kind":"cream","start":round(CREAM[0],3),"dur":round(CREAM[1]-CREAM[0],3),"words":[["best",t(21)],["price",t(22)]]},
 {"kind":"navy","start":round(NAVY[0],3),"dur":round(NAVY[1]-NAVY[0],3),"words":[["your",t(35)],["habits,",t(36)]]},
 {"kind":"title","start":SEG["G"],"dur":round(SEG["H"]-SEG["G"],3),"top":958,"lines":[
   {"style":"serif-red","size":78,"words":[["your",t(54)],["hotel",t(55)],["saving",t(56)],["alone",t(57)]]},
   {"style":"heavy","size":104,"words":[["can",t(58)],["cover",t(59)],["our",t(60)]]},
   {"style":"heavy-red","size":104,"words":[["concierge",t(61)],["fee.",t(62)]]}]},
 {"kind":"cta","start":round(t(63)-0.2,3),"dur":round(DUR-t(63)+0.2,3),"top":1080,"keyword":"HOTEL",
  "t_type":round(t(64)+0.02,3),"t_send":round(t(65)+0.10,3),"t_dm":round(t(66)+0.05,3),
  "brand":"ChinaPal Travel","reward":"We'll check how much you can save on your hotels \U0001F3E8"}]
CTA=cards[-1]
sfx=[["whoosh_es.wav",br[0][1]-0.12,0.35],["whoosh_es.wav",br[1][1]-0.10,0.3],["whoosh_es.wav",br[3][1]-0.08,0.3],
     ["pop_es.wav",t(5)-0.02,0.35],["pop_es.wav",CREAM[0]-0.03,0.35],["pop_es.wav",NAVY[0]-0.03,0.35],["pop_es.wav",t(54)-0.02,0.35],["whoosh_es.wav",CTA["start"]-0.05,0.18],["pop_es.wav",CTA["t_send"]-0.02,0.45],["pop_es.wav",CTA["t_dm"]-0.02,0.5]]
sfx=[[f,round(a,3),v] for f,a,v in sfx]
json.dump({"duration":DUR,"aroll":aroll,"broll":broll,"captions":caps,"cards":cards,"sfx":sfx,"cap_top":1060,
           "music":MUSIC},open(f'{E}/plan.json','w'),indent=1)
for c in caps: print(f"{c['start']:6.2f}-{c['end']:6.2f}  "+' '.join(w[0] for w in c['words']))
print('duration',DUR)
