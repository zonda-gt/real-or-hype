# Insert the creator's real on-camera line into vo.wav after a given narration word, and add caption tokens.
# usage: insert_real.py <workdir> <after_word> <src_clip> <clip_in> <clip_out> "<Caption words>"
# Keeps vo_orig.wav / words_orig.json; rewrites vo.wav + words.json; writes real.json {start, clip_in, clip_out, idx}.
import sys,os,json,subprocess,re,numpy as np
W,after,src,ci,co,cap=sys.argv[1],sys.argv[2],sys.argv[3],float(sys.argv[4]),float(sys.argv[5]),sys.argv[6]
os.chdir(W); SR=48000
if not os.path.exists('vo_orig.wav'): os.rename('vo.wav','vo_orig.wav'); os.rename('words.json','words_orig.json')
words=json.load(open('words_orig.json'))
def pcm(f,ss=None,t=None,af=None):
    c=['ffmpeg','-loglevel','error']+(['-ss',str(ss),'-t',str(t)] if ss is not None else [])+['-i',f]+(['-af',af] if af else [])+['-ac','1','-ar',str(SR),'-f','f32le','-']
    return np.frombuffer(subprocess.run(c,capture_output=True,check=True).stdout,np.float32).copy()
vo=pcm('vo_orig.wav')
k=next(i for i,w in enumerate(words) if re.sub(r'[^a-z]','',w[2].lower())==after.lower())
cut=min(words[k][1]+0.12,(words[k][1]+words[k+1][0])/2)
real=pcm(f'broll/{src}.mp4',ci,co-ci,'highpass=f=80')
rms=lambda x: np.sqrt(np.mean(x[np.abs(x)>np.abs(x).max()*0.1]**2))   # loudness of the voiced part
real*=rms(vo)/rms(real)*0.95; real=np.clip(real,-0.95,0.95)
f=int(0.015*SR); real[:f]*=np.linspace(0,1,f); real[-f:]*=np.linspace(1,0,f)
gap=np.zeros(int(0.12*SR),np.float32); c=int(cut*SR)
out=np.concatenate([vo[:c],gap,real,gap,vo[c:]])
subprocess.run(['ffmpeg','-loglevel','error','-y','-f','f32le','-ar',str(SR),'-ac','1','-i','-','vo.wav'],input=out.tobytes(),check=True)
start=cut+0.12; shift=0.24+(co-ci)
# caption tokens spread over the voiced part of the clip (measured: speech 18.75-19.50 in clip 061)
v0,v1=float(os.environ.get('VOICED0',ci)),float(os.environ.get('VOICED1',co)); toks=cap.split(); dur=(v1-v0)/len(toks)
new=[(round(start+(v0-ci)+j*dur,3),round(start+(v0-ci)+(j+1)*dur,3),t) for j,t in enumerate(toks)]
ws=[w for w in words if w[0]<cut]+new+[(round(a+shift,3),round(b+shift,3),t) for a,b,t in words if a>=cut]
json.dump(ws,open('words.json','w'))
json.dump({'start':start,'clip_in':ci,'clip_out':co,'voiced0':v0,'idx':len([w for w in words if w[0]<cut])},open('real.json','w'))
print('inserted at',round(start,2),'s; caption token index',len([w for w in words if w[0]<cut]),'; new length',round(len(out)/SR,2))
