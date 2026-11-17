# After a re-voiced take, move every word index in plan.py (CUES, LABELS, CARDS, CTA) to the same word in the new words.json.
# usage: remap_cues.py <workdir> <old_words.json>      (aligns old vs new transcript with difflib; prints each move)
import sys,json,re,difflib,os
W,old=sys.argv[1],sys.argv[2]
norm=lambda w: re.sub(r"[^a-z0-9]","",w.lower())
a=[norm(w[2]) for w in json.load(open(old))]; b=[norm(w[2]) for w in json.load(open(os.path.join(W,'words.json')))]
m={}
for blk in difflib.SequenceMatcher(None,a,b,autojunk=False).get_matching_blocks():
    for k in range(blk.size): m[blk.a+k]=blk.b+k
def mp(i):
    j=i
    while j not in m and j<len(a): j+=1     # unmatched (reworded) word: use the next matched one
    return m.get(j,len(b)-1)
p=os.path.join(W,'plan.py'); out=[]; sec=None
for line in open(p).read().split('\n'):
    s=line.lstrip()
    for k in ('CUES','LABELS','CARDS','CTA','TAIL','TITLE','CAPTION_FIX','COLLAGE','SRC'):
        if s.startswith(k+'='): sec=k
    if sec=='CUES' and re.match(r"\s*\((\d+),\s*\[",line):
        i=int(re.match(r"\s*\((\d+),",line).group(1)); line=re.sub(r"^(\s*\()(\d+)",lambda g:g.group(1)+str(mp(i)),line,count=1)
        print('cue',i,'->',mp(i),a[i],'->',b[mp(i)])
    elif sec=='CARDS':
        line=re.sub(r",(\d+),(\d+)\)",lambda g:f',{mp(int(g.group(1)))},{mp(int(g.group(2)))})',line)
    elif sec in ('LABELS','CTA'):
        line=re.sub(r",\s*(\d+)\)",lambda g:','+str(mp(int(g.group(1))))+')',line)
    out.append(line)
open(p,'w').write('\n'.join(out)); print('remapped',p)
