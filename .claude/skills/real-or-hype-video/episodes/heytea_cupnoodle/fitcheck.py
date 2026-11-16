# Dry-run timing check from nominal shot lengths (no render): each narration line must end >=0.05 s before the next event.
import sys,os,subprocess
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); from segs import *
vod=sys.argv[1]
def dur(f): return float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f],capture_output=True,text=True).stdout)
st={};t=0
for s in SEGS: st[s[0]]=t; t+=s[3]/s[4]
ev=[(st[sid]+off,st[sid]+off+dur(f'{vod}/{k}.wav'),k) for k,sid,off in VO]
ev+=[(st[s[0]]+(SPEECH[s[0]][0]-s[2])/s[4],st[s[0]]+(SPEECH[s[0]][1]-s[2])/s[4],s[0]) for s in SEGS if s[5]=='real']
ev.sort(); bad=0
for (a,b,k),(a2,b2,k2) in zip(ev,ev+[(t+0.25,0,'END')][1:] if False else ev[1:]+[(t-0.25,0,'END')]):
    slack=a2-0.05-b; bad+=slack<0
    print(f'{k:4s} {a:6.2f}-{b:6.2f}  next {k2:4s} @{a2:6.2f}  slack {slack:+.2f}' + ('  <-- TOO LONG' if slack<0 else ''))
print(f'total {t:.2f}s', 'OK' if not bad else f'{bad} FAIL')
