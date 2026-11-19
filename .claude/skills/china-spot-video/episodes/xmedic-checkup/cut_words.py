# Remove whole narration phrases from vo.wav / words.json (cut in the middle of the gaps around them).
# usage: cut_words.py <workdir> "<first word>|<last word>" ...   (first matching occurrence; keeps vo_full.wav / words_full.json)
import sys,os,json,re,subprocess,numpy as np
W=sys.argv[1]; os.chdir(W); SR=48000
if not os.path.exists('vo_full.wav'): os.rename('vo.wav','vo_full.wav'); os.rename('words.json','words_full.json')
ws=json.load(open('words_full.json')); a=np.frombuffer(subprocess.run(['ffmpeg','-loglevel','error','-i','vo_full.wav','-ac','1','-ar',str(SR),'-f','f32le','-'],capture_output=True,check=True).stdout,np.float32).copy()
n=lambda w: re.sub(r'[^a-z]','',w.lower()); cuts=[]
for spec in sys.argv[2:]:
    f,l=spec.split('|'); i=next(k for k,w in enumerate(ws) if n(w[2])==n(f)); j=next(k for k in range(i,len(ws)) if n(ws[k][2])==n(l))
    t0=(ws[i-1][1]+ws[i][0])/2 if i>0 else 0; t1=(ws[j][1]+ws[j+1][0])/2 if j+1<len(ws) else len(a)/SR
    cuts.append((t0,t1,i,j)); print('cut',round(t0,2),'-',round(t1,2),' '.join(w[2] for w in ws[i:j+1]))
cuts.sort(); keep=[]; prev=0; fd=int(0.008*SR)
for t0,t1,_,_ in cuts:
    s=a[int(prev*SR):int(t0*SR)].copy(); s[-fd:]*=np.linspace(1,0,fd); s[:fd]*=np.linspace(0,1,fd) if prev>0 else 1; keep.append(s); prev=t1
s=a[int(prev*SR):].copy(); s[:fd]*=np.linspace(0,1,fd); keep.append(s)
subprocess.run(['ffmpeg','-loglevel','error','-y','-f','f32le','-ar',str(SR),'-ac','1','-i','-','vo.wav'],input=np.concatenate(keep).tobytes(),check=True)
out=[]
for k,(x,y,t) in enumerate(ws):
    if any(i<=k<=j for _,_,i,j in cuts): continue
    sh=sum(t1-t0 for t0,t1,i,j in cuts if t1<=x+1e-6); out.append([round(x-sh,3),round(y-sh,3),t])
json.dump(out,open('words.json','w')); print('new length',round(sum(len(k) for k in keep)/SR,2),'s')
