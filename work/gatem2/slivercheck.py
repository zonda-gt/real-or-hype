# Flags shots whose source window starts/ends within 0.15 s of a source cut (a 1-4 frame "sliver" of another shot).
import subprocess,json,os,sys
sys.path.insert(0,'.'); from edl import shots
cache={}
def cuts(src):
    if src not in cache:
        r=subprocess.run(['ffmpeg','-hide_banner','-i',f'src/{src}.mp4','-vf',"select='gt(scene,0.25)',showinfo",'-an','-f','null','-'],capture_output=True,text=True).stderr
        cache[src]=[float(x.split(':')[1]) for x in r.split() if x.startswith('pts_time:')]
    return cache[src]
bad=0
for s in shots():
    a,b=s['inn'],s['inn']+s['dur']
    for c in cuts(s['src']):
        if a<c<b and (c-a<0.15 or b-c<0.15):
            bad+=1; print(f"SLIVER #{s['i']} {s['src']} window {a:.2f}-{b:.2f} crosses cut at {c:.2f} ({'start' if c-a<0.15 else 'end'}, {min(c-a,b-c):.2f}s)")
print('ALL OK' if not bad else f'{bad} slivers'); sys.exit(1 if bad else 0)
