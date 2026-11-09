# usage: precut.py src.mp4 out.mp4 a1 b1 [a2 b2 ...]  -> joins time ranges of src (video+audio) into out, and writes out.json words (shifted)
import json,subprocess,sys,os
src,out=sys.argv[1],sys.argv[2]; r=list(map(float,sys.argv[3:])); R=list(zip(r[::2],r[1::2]))
parts=''.join(f'[0:v]trim={a}:{b},setpts=PTS-STARTPTS[v{i}];[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS[a{i}];' for i,(a,b) in enumerate(R))
fc=parts+''.join(f'[v{i}][a{i}]' for i in range(len(R)))+f'concat=n={len(R)}:v=1:a=1[v][a]'
subprocess.run(['ffmpeg','-loglevel','error','-y','-i',src,'-filter_complex',fc,'-map','[v]','-map','[a]','-c:v','libx264','-crf','14','-preset','fast','-pix_fmt','yuv420p','-c:a','aac','-b:a','256k',out],check=True)
W=[w for s in json.load(open(src+'.json')) for w in s['w']]; off=0; segs=[]
for a,b in R:
    ws=[[x-a+off,y-a+off,t] for x,y,t in W if a<=x<b]
    if ws: segs.append({'s':ws[0][0],'e':ws[-1][1],'t':' '.join(w[2] for w in ws),'w':ws})
    off+=b-a
json.dump(segs,open(out+'.json','w')); print(out,round(off,2),'s')
