import subprocess, numpy as np
W,H,Y=720,150,570
raw = subprocess.run(["ffmpeg","-v","error","-i","reel.mp4","-vf",f"crop={W}:{H}:0:{Y},format=rgb24","-f","rawvideo","-"],capture_output=True).stdout
fr = np.frombuffer(raw,np.uint8).reshape(-1,H,W,3).astype(np.int16)
r,g,b = fr[...,0],fr[...,1],fr[...,2]
mask = (b - r > 25) & (r < 110)   # dark navy text
cols = mask.sum(1).astype(np.float32)  # per-column profile (n, W)
rows = mask.sum(2)
refs = {"A":30,"B":90,"C":300,"D":339,"E":387,"F":435}
def sig(i): return cols[i]
lab=[]
for i in range(len(fr)):
    if mask[i].sum() < 400: lab.append("-"); continue
    best=None
    for k,j in refs.items():
        a,bb = cols[i],cols[j]
        # allow horizontal shift +-15
        sc=max(np.corrcoef(np.roll(a,s),bb)[0,1] for s in range(-15,16,3))
        if best is None or sc>best[1]: best=(k,sc)
    lab.append(best[0] if best[1]>0.6 else "?")
segs=[]
for i,l in enumerate(lab):
    if segs and segs[-1][0]==l: segs[-1][2]=i
    else: segs.append([l,i,i])
for l,a,b in segs: print(l, round(a/30,3), round((b+1)/30,3))
