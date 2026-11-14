import json,subprocess,numpy as np,re,sys
SR=44100; TEMPO=float(sys.argv[1]) if len(sys.argv)>1 else 1.08
TAKE=sys.argv[2] if len(sys.argv)>2 else 'take1'
x=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',f'vo/{TAKE}.mp3','-ac','1','-ar',str(SR),'-f','f32le','-'],capture_output=True).stdout,np.float32).copy()
al=json.load(open(f'vo/{TAKE}.align.json')); ch=al['characters']; st=al['character_start_times_seconds']; en=al['character_end_times_seconds']
# words from alignment (skip [tags])
txt=''.join(ch); words=[]
for m in re.finditer(r'\[[^\]]*\]|[^\s\[]+',txt):
    if m.group().startswith('['): continue
    i,j=m.start(),m.end()-1; words.append([m.group(),st[i],en[j]])
# silence runs via 10ms RMS
h=441; rms=np.array([np.sqrt(np.mean(x[i:i+h]**2)) for i in range(0,len(x)-h,h)]); db=20*np.log10(rms+1e-9)
q=db<-42; runs=[];i=0
while i<len(q):
    if q[i]:
        j=i
        while j<len(q) and q[j]: j+=1
        runs.append((i*h/SR,j*h/SR)); i=j
    else: i+=1
# keep segments: shrink runs >0.30s to 0.24s (leading silence -> 0.03)
keep=[];prev=0.0
for a,b in runs:
    L=b-a
    if a<0.01: keep.append((b-0.03,None)); prev=b-0.03; continue
    if L>0.30:
        keep.append((prev,a+0.12)); prev=b-0.12
keep=[k for k in keep if k[1] is not None]+[(prev,len(x)/SR)]
# trailing: cut at last word end+0.25
last=words[-1][2]+0.25
segs=[];
for a,b in keep:
    b=min(b,last)
    if b>a: segs.append((a,b))
out=np.concatenate([x[int(a*SR):int(b*SR)] for a,b in segs])
# time map
def tmap(t):
    acc=0
    for a,b in segs:
        if t<a: return acc
        if t<=b: return acc+(t-a)
        acc+=b-a
    return acc
for w in words: w[1]=tmap(w[1])/TEMPO; w[2]=tmap(w[2])/TEMPO
# 5ms fades at joins handled by writing then atempo
out.astype(np.float32).tofile('vo/tight.f32')
subprocess.run(['ffmpeg','-v','error','-y','-f','f32le','-ar',str(SR),'-ac','1','-i','vo/tight.f32','-af',f'atempo={TEMPO},highpass=f=70,loudnorm=I=-16:TP=-2:LRA=7','-ar','48000','vo/narr.wav'])
json.dump(words,open('vo/words.json','w'),ensure_ascii=False)
d=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0','vo/narr.wav'],capture_output=True,text=True).stdout)
gaps=[words[i+1][1]-words[i][2] for i in range(len(words)-1)]
print(f'narration {d:.2f}s, {len(words)} words, {len(words)/(words[-1][2]-words[0][1])*60:.0f} wpm, max gap {max(gaps):.2f}s, gaps>0.3: {sum(g>0.3 for g in gaps)}')
