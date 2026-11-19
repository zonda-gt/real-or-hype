# Shared helpers for the XMEDIC plans: look up cue words by text instead of hard-coded indices.
import json,os,re
def _norm(w): return re.sub(r"[^a-z0-9]","",w.lower())
def loader(workdir):
    words=json.load(open(os.path.join(workdir,'words.json')))
    def idx(word,n=1,after=-1):
        k=0
        for i,(a,b,w) in enumerate(words):
            if i>after and _norm(w).startswith(_norm(word)):
                k+=1
                if k==n: return i
        raise SystemExit(f'cue word not found: {word} (n={n}, after={after})')
    return words,idx
