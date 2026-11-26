import json,sys
E=sys.argv[1]; W=json.load(open(f'{E}/words.json')); TL=json.load(open(f'{E}/timeline.json'))
DUR=round(TL[-1]['start']+TL[-1]['dur'],3)
FIX={30:'a',57:'alone'}                       # Whisper mishears; captions follow what he says
def txt(i): return FIX.get(i,W[i][2])
def t(i): return W[i][0]
EM={4,15,34,51}                               # red serif accent words
GROUPS=[[0,1,2],[3,4],[11,12,13],[14,15,16],[17,18,19,20],[23,24],[25,26],[27,28,29],[30,31,32],[33,34],
        [37,38,39],[40],[41,42,43],[44],[45,46,47],[48,49,50],[51,52,53],[63,64,65],[66,67,68,69]]
BLOCK=[(2.13,3.93),(6.55,7.42),(11.68,12.43),(18.03,21.13)]   # full cards / titles: no captions
br=[("skyline",1.50,2.13),("jhotel",5.20,5.88),("ritz",5.88,6.55),("train",12.80,13.38),("bund",13.38,14.18),("hotpot",14.18,15.33)]
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
scale={'A':1.0,'B':1.14,'C':1.0,'D':1.1,'E':1.0,'F':1.15,'G':1.0,'H':1.12,'I':1.0}
whip={'B','F','E','G','H'}
aroll=[{"k":s['k'],"start":s['start'],"dur":s['dur'],"scale":scale[s['k']],"whip":s['k'] in whip} for s in TL]
br=[("skyline",1.50,2.13),("jhotel",5.20,5.88),("ritz",5.88,6.55),("train",12.80,13.38),("bund",13.38,14.18),("hotpot",14.18,15.33)]
broll=[{"id":n,"src":n,"start":a,"dur":round(b-a,3)} for n,a,b in br]
cards=[
 {"kind":"title","start":2.13,"dur":1.80,"top":1030,"lines":[
   {"style":"heavy","size":134,"words":[["Don't",t(5)],["book",t(6)]]},
   {"style":"heavy","size":134,"words":[["your",t(7)],["hotel",t(8)]]},
   {"style":"serif-red","size":124,"words":[["just",t(9)],["yet.",t(10)]]}]},
 {"kind":"cream","start":6.55,"dur":0.87,"words":[["best",t(21)],["price",t(22)]]},
 {"kind":"navy","start":11.68,"dur":0.75,"words":[["your",t(35)],["habits,",t(36)]]},
 {"kind":"title","start":18.03,"dur":3.10,"top":958,"lines":[
   {"style":"serif-red","size":78,"words":[["your",t(54)],["hotel",t(55)],["saving",t(56)],["alone",t(57)]]},
   {"style":"heavy","size":104,"words":[["can",t(58)],["cover",t(59)],["our",t(60)]]},
   {"style":"heavy-red","size":104,"words":[["concierge",t(61)],["fee.",t(62)]]}]},
 {"kind":"pill","start":t(64)-0.02,"dur":round(DUR-t(64)+0.02,3),"top":1010,"text":"HOTEL"}]
sfx=[["whoosh_es.wav",1.38,0.35],["whoosh_es.wav",5.10,0.3],["whoosh_es.wav",12.72,0.3],
     ["pop_es.wav",2.36,0.35],["pop_es.wav",6.52,0.35],["pop_es.wav",11.65,0.35],["pop_es.wav",18.26,0.35],["pop_es.wav",t(64)-0.05,0.45]]
json.dump({"duration":DUR,"aroll":aroll,"broll":broll,"captions":caps,"cards":cards,"sfx":sfx,"cap_top":1060,
           "music":{"file":"music_marimba_el.mp3","vol":0.25}},open(f'{E}/plan.json','w'),indent=1)
for c in caps: print(f"{c['start']:6.2f}-{c['end']:6.2f}  "+' '.join(w[0] for w in c['words']))
print('duration',DUR)
