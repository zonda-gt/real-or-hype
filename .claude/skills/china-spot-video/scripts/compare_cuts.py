# Do the versions FEEL like different videos? usage: compare_cuts.py <workdirA> <workdirB> [<workdirC>]
# Sharing clips is fine (creator's rule); what must differ is the feel: the opening, the order, the rhythm.
# Reads each workdir's timeline.json (written by render_cut.py) and prints, for every pair:
#   opening: whether the first 1.5 s (the hook) use the same source moments; the hook must look different
#   order:   how similar the order of on-screen moments is (source + 4 s window; 0 = unrelated, 1 = same order); must be <= 0.5
#   rhythm:  average shot length of each; two versions within 15% of each other cut at the same pace
#   shared:  seconds of the same source moments used in both (information only, never a failure)
import json,sys,os,itertools
def load(w):
    t=json.load(open(os.path.join(w,'timeline.json'))); shots=t.get('shots')
    if shots is None: sys.exit(f'{w}: timeline.json has no shots; re-run render_cut.py')
    # the collage shows its tiles at the same time: each tile counts for its share of the screen
    col=[dict(c,start=0.0,end=t['collage_end'],w=1/len(t['collage'])) for c in t.get('collage',[])]
    return {'name':os.path.basename(os.path.normpath(w)),'T':t['T'],'shots':shots,'all':col+[dict(s,w=1.0) for s in shots]}
def inter(a,b):
    return max(0.0,min(a['out'],b['out'])-max(a['in'],b['in'])) if a['src']==b['src'] else 0.0
def shared(A,B):
    # time in the video covered by source moments that the other version also uses
    tot=0.0
    for a in A['all']:
        ov=sum(inter(a,b) for b in B['all']); span=a['out']-a['in']
        if span>0: tot+=min(ov,span)/span*(a['end']-a['start'])*a['w']
    return tot
def opening(V,secs=1.5): return [s for s in V['all'] if s['start']<secs]
def lcs(x,y):
    m=[[0]*(len(y)+1) for _ in range(len(x)+1)]
    for i,a in enumerate(x):
        for j,b in enumerate(y): m[i+1][j+1]=m[i][j]+1 if a==b else max(m[i][j+1],m[i+1][j])
    return m[-1][-1]
def order(A,B):
    # compare what's on screen, not which file: the same source 4 s apart is a different scene
    x=[(s['src'],int(s['in']//4)) for s in A['shots']]; y=[(s['src'],int(s['in']//4)) for s in B['shots']]
    x=[s for i,s in enumerate(x) if i==0 or s!=x[i-1]]; y=[s for i,s in enumerate(y) if i==0 or s!=y[i-1]]
    return lcs(x,y)/max(1,min(len(x),len(y)))
V=[load(w) for w in sys.argv[1:]]
if len(V)<2: sys.exit(__doc__ if __doc__ else 'give 2 or 3 workdirs')
ok=True
for v in V: print(f"{v['name']}: {v['T']:.1f} s, {len(v['shots'])} shots, avg {v['T']/max(1,len(v['shots'])):.2f} s/shot")
for A,B in itertools.combinations(V,2):
    sh=max(shared(A,B),shared(B,A)); pct=min(100.0,sh/min(A["T"],B["T"])*100)
    op=any(inter(a,b)>0 for a in opening(A) for b in opening(B)); od=order(A,B)
    pa,pb=A['T']/max(1,len(A['shots'])),B['T']/max(1,len(B['shots']))
    same_pace=abs(pa-pb)/max(pa,pb)<0.15
    bad=[w for w,c in [('same opening',op),('same order',od>0.5),('same rhythm',same_pace)] if c]
    ok&=not bad
    print(f"{A['name']} vs {B['name']}: opening {'SAME' if op else 'different'}, order {od:.2f}, rhythm {pa:.2f} vs {pb:.2f} s/shot, shared clips {sh:.1f} s ({pct:.0f}%)"+(f"  <-- feels the same: {', '.join(bad)}" if bad else "  ok"))
sys.exit(0 if ok else 1)
