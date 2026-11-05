# Collect everything the A0 edit uses into one media folder + a manifest (times in seconds)
import sys,os,json,ast,re,shutil,subprocess
os.chdir(sys.argv[1]); VAR=sys.argv[2]; M=sys.argv[3]
sys.path.insert(0,'scripts'); import variants
st=ast.literal_eval(open(f'vr/{VAR}/starts.txt').read()); S=variants.S[VAR]
def dur(p): return float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',p],capture_output=True,text=True).stdout)
man={'video':[],'overlays':[],'narration':[],'sfx':[],'sting':None}
# 1) shots (already colour-converted, cropped, sped; with their own audio)
for i,(sid,kind,args,d,key) in enumerate(S):
    dst=f'{i:02d}_{sid}.mp4'; shutil.copy(f'vr/{VAR}/seg/{sid}.mp4',f'{M}/{dst}')
    man['video'].append({'file':dst,'start':st[sid],'dur':dur(f'{M}/{dst}')})
total=st[S[-1][0]]+dur(f'{M}/{len(S)-1:02d}_{S[-1][0]}.mp4')
# 2) graphics
for png,a,b in variants.ovs(VAR,st,total):
    if not os.path.exists(f'{M}/{png}'): shutil.copy(f'v13/ov/{png}',f'{M}/{png}')
    man['overlays'].append({'file':png,'start':round(a,3),'end':round(b,3)})
# 3) narration (loudness-normalised like the render)
for sid,kind,args,d,key in S:
    if not key: continue
    out=f'nar_{key}.wav'
    subprocess.run(['ffmpeg','-loglevel','error','-y','-i',f'{variants.VODIR}/{key}.wav','-af','loudnorm=I=-15:TP=-1.5','-ar','48000','-ac','2',f'{M}/{out}'],check=True)
    man['narration'].append({'file':out,'start':round(st[sid]+(0.25 if key.endswith('verdict') else 0.08),3),'dur':dur(f'{M}/{out}')})
# 4) sting
subprocess.run(['ffmpeg','-loglevel','error','-y','-i','gd/sting.mp3','-af','loudnorm=I=-14:TP=-1.5,afade=t=out:st=1.95:d=0.4','-t','2.4','-ar','48000','-ac','2',f'{M}/sting.wav'],check=True)
man['sting']={'file':'sting.wav','start':st['H2'],'dur':dur(f'{M}/sting.wav')}
# 5) sound effects, gain and trim baked in (same placement as add_sfx.py)
import numpy as np
T1,T2=variants.TICKS.get(VAR,(1.1,2.0))
ev=[('whoosh_es',0.310,st['O1'],0.45,None),('whoosh_es',0.310,st['A1'],0.45,None),('whoosh_es',0.310,st['R1'],0.45,None),
    ('pop_es',0.0,st['O5']+0.03,0.40,None),('real_es',0.335,st['V1']+T1,0.45,None),('buzz_el',0.345,st['V1']+T2,0.40,None)]
if 'I4' in st: ev.append(('ding',0.05,st['I4']+0.13,0.55,(0,0.45)))
for j,(n,po,t,v,tr) in enumerate(ev):
    a=np.frombuffer(subprocess.run(['ffmpeg','-loglevel','error','-i',f'sfx/{n}.wav','-ac','1','-f','f32le','-'],capture_output=True).stdout,dtype=np.float32)
    g=10**((-6-20*np.log10(np.abs(a).max()+1e-9))/20)*v
    af=(f'atrim={tr[0]}:{tr[1]},afade=t=out:st={tr[1]-tr[0]-0.08:.2f}:d=0.08,' if tr else '')+f'volume={g:.4f}'
    out=f'sfx_{j}_{n}.wav'; subprocess.run(['ffmpeg','-loglevel','error','-y','-i',f'sfx/{n}.wav','-af',af,'-ar','48000','-ac','2',f'{M}/{out}'],check=True)
    man['sfx'].append({'file':out,'start':round(max(0,t-po),3),'dur':dur(f'{M}/{out}')})
# 6) subtitles: merge the word-highlight ASS events back into phrases -> SRT
ev=[]
for ln in open(f'vr/{VAR}/subs.ass',encoding='utf-8'):
    if not ln.startswith('Dialogue:'): continue
    p=ln.rstrip('\n').split(',',9); txt=re.sub(r'\{[^}]*\}','',p[9])
    hms=lambda x: (lambda h,m,s: int(h)*3600+int(m)*60+float(s))(*x.split(':'))
    a,b=hms(p[1]),hms(p[2])
    if ev and ev[-1][2]==txt and abs(ev[-1][1]-a)<0.02: ev[-1][1]=b
    else: ev.append([a,b,txt])
ev.sort(key=lambda e:e[0])
for k in range(len(ev)-1): ev[k][1]=min(ev[k][1],ev[k+1][0])   # never overlap the next phrase
def srt(t): ms=int(round(t*1000)); return f'{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}'
open(f'{M}/subtitles.srt','w',encoding='utf-8').write(''.join(f'{i+1}\n{srt(a)} --> {srt(b)}\n{t}\n\n' for i,(a,b,t) in enumerate(ev)))
man['total']=total; man['subtitles']='subtitles.srt'
json.dump(man,open(f'{M}/../manifest.json','w'),indent=1)
print('shots',len(man['video']),'overlays',len(man['overlays']),'narration',len(man['narration']),'sfx',len(man['sfx']),'subtitle phrases',len(ev),'total',round(total,2))
