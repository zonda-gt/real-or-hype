K49='7683856501748182399'; KR='7703171104194397775'; KS='7627736289027109499'; YT='7706818090939798258'
BUB='7524980074819456302'; SCR='7500456784822652179'; DUO='7699420697072950626'; GAB='7635405931203746225'; HU='7490131673993022770'
SRC={K49:{'cut':0.37},KR:{'cut':0.27},KS:{'cut':0.25},YT:{'cut':0.25},BUB:{},SCR:{},DUO:{'cut':0.30},GAB:{'cut':0.24},HU:{'cut':0.24}}
import json,os,re
_N={'1':'one','2':'two','3':'three','4':'four','one':'one','two':'two','three':'three','four':'four'}
def _norm(w):
    w=re.sub(r"[^a-z0-9'$-]","",w.lower()).replace('$','')
    return _N.get(w,w)
def finder(words_path):
    toks=[_norm(w[2]) for w in json.load(open(words_path))]
    def idx(phrase,nth=1):
        p=[_norm(x) for x in phrase.split()]; n=0
        for i in range(len(toks)-len(p)+1):
            if toks[i:i+len(p)]==p:
                n+=1
                if n==nth: return i
        raise ValueError(f'phrase not found: {phrase} #{nth}')
    return idx
