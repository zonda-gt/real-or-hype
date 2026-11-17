# usage: finish.py <workdir> [VAR] -> out/final.mp4 (1080p) + out/preview540.mp4
# Subtitles (≤3 words, current word yellow, Montserrat ExtraBold 66 / 6px outline, MarginV 430), title card, narration, SFX, loudness.
import os,sys,json,subprocess,numpy as np
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import importlib
VAR=sys.argv[2] if len(sys.argv)>2 else ''
_m=importlib.import_module('segs'+('_'+VAR if VAR else '')); globals().update({k:v for k,v in vars(_m).items() if not k.startswith('__')})
OUT='out'+('_'+VAR if VAR else ''); VOD='vo'+('_'+VAR if VAR else ''); HK='hook'+('_'+VAR if VAR else '')
OVL=globals().get('OVL',[])
W=sys.argv[1]; os.chdir(W); J=json.load(open(OUT+'/starts.json')); st=J['starts']; total=st['_end']
SK='/home/user/real-or-hype/.claude/skills/real-or-hype-video/'
lines=json.load(open(VOD+'/lines.json'))
from faster_whisper import WhisperModel
m=WhisperModel('small.en',device='cpu',compute_type='int8')
def pcm(f,ss=None,t=None):
    pre=['-ss',str(ss),'-t',str(t)] if ss is not None else []
    return np.frombuffer(subprocess.run(['ffmpeg','-loglevel','error']+pre+['-i',f,'-ar','16000','-ac','1','-f','f32le','-'],capture_output=True).stdout,dtype=np.float32)
def align(text,f,off,ss=None,t=None):
    tw=text.split(); segs,_=m.transcribe(pcm(f,ss,t),language='en',word_timestamps=True,beam_size=5)
    ww=[(w.start,w.end) for s in segs for w in s.words]
    if len(ww)==len(tw): return [(off+a,off+b,w) for (a,b),w in zip(ww,tw)]
    print('  word count differs, spreading by letters:',f,len(ww),len(tw))
    s0,s1=ww[0][0],ww[-1][1]; L=sum(len(w) for w in tw); acc=0; res=[]
    for w in tw:
        a=s0+(s1-s0)*acc/L; acc+=len(w); res.append((off+a,off+s0+(s1-s0)*acc/L,w))
    return res
allw=[]
hs=HOOK[0]; he=HOOK[2] if len(HOOK)>2 else hs; HOOK_END=st[SEGS[[x[0] for x in SEGS].index(he)+1][0]]
for k,s,e in J['vo']:
    import re; txt=re.sub(r'\s+',' ',re.sub(r'\[[^\]]*\]','',VOTXT.get(k,lines[k]))).strip().replace('Hey Tea','Heytea')   # drop v3 audio tags
    ws=align(txt,f'{VOD}/{k}.wav',s)
    allw.append([w for w in ws if w[0]>=HOOK_END-0.05])   # hook text already says it; subtitles start after the hook
for sid,txt in REAL.items(): allw.append(align(txt,f'{OUT}/seg/{sid}.mov',st[sid]))
allw=[w for w in allw if w]
def ts(x): return f'{int(x//3600)}:{int(x%3600//60):02d}:{x%60:05.2f}'
ass=open(SK+'episodes/heytea_cupnoodle/ass_head.txt').read()
EVS=[]
for ws in allw:
    chunks=[];cur=[]
    for w in ws:
        cur.append(w)
        if len(cur)==3 or w[2][-1] in '.,?!:': chunks.append(cur);cur=[]
    if cur: chunks.append(cur)
    for ci,ch in enumerate(chunks):
        endc=min(chunks[ci+1][0][0] if ci+1<len(chunks) else ch[-1][1]+0.25, total)
        for wi,(a,b,w) in enumerate(ch):
            e=ch[wi+1][0] if wi+1<len(ch) else endc
            txt=' '.join(('{\\c&H1AE2FF&}'+x[2]+'{\\c&HFFFFFF&}') if j==wi else x[2] for j,x in enumerate(ch))
            EVS.append([a,max(e,a+0.05),txt])
EVS.sort(key=lambda x:x[0])          # never two subtitle events on screen at once
for i in range(len(EVS)-1): EVS[i][1]=min(EVS[i][1],EVS[i+1][0])
for a,e,txt in EVS:
    if e-a>0.02: ass+=f'Dialogue: 0,{ts(a)},{ts(e)},main,,0,0,0,,{txt}\n'
open(OUT+'/subs.ass','w').write(ass)
# audio: base (room sound + his lines) + narration + effects
def peak_db(f): return 20*np.log10(np.abs(pcm(f)).max()+1e-9)
inp=['-i',OUT+'/base.mov']+sum([['-loop','1','-t',f'{HOOK_END:.2f}','-i',f'{HK}/{k}.png'] for k in ('kgrad','k0','k1','k2')],[])+sum([['-loop','1','-t',f'{total:.2f}','-i',f'{HK}/{o[0]}'] for o in OVL],[]); fc=''; mix=['[0:a]']; n=5+len(OVL)
for k,s,e in J['vo']:
    ms=int(s*1000); inp+=['-i',f'{VOD}/{k}.wav']
    fc+=f'[{n}:a]aresample=48000,aformat=channel_layouts=stereo,loudnorm=I=-15:TP=-1.5:LRA=11,aresample=48000,adelay={ms}|{ms}[v{n}];'; mix.append(f'[v{n}]'); n+=1
fx=[('whoosh_es',0.31,st[s],0.45) for s in WHOOSH]
for name,po,t,vol in fx:
    f=SK+f'sfx/{name}.wav'; g=10**((-6-peak_db(f))/20)*vol; ms=max(0,int((t-po)*1000)); inp+=['-i',f]
    fc+=f'[{n}:a]aresample=48000,aformat=channel_layouts=stereo,volume={g:.4f},adelay={ms}|{ms}[x{n}];'; mix.append(f'[x{n}]'); n+=1
T0,T1=st[hs],HOOK_END; R=HOOK[1]
fc+=f"[1:v]format=rgba,fade=t=in:st=0:d=0.3:alpha=1,fade=t=out:st={T1-0.35:.2f}:d=0.35:alpha=1[g];[0:v][g]overlay=0:0:eof_action=pass[v0];"
for i,rt in enumerate(R):
    fc+=(f"[{i+2}:v]format=rgba,fade=t=in:st={rt}:d=0.45:alpha=1,fade=t=out:st={T1-0.35:.2f}:d=0.35:alpha=1[h{i}];"
         f"[v{i}][h{i}]overlay=x=0:y='if(lt(t,{rt}),24,if(lt(t,{rt+0.45}),24*(1-(t-{rt})/0.45),0))':eof_action=pass[v{i+1}];")
last='v3'
for j,(png,sid,off,dd) in enumerate(OVL):
    t0=st[sid]+off; t1=t0+dd
    fc+=(f"[{5+j}:v]format=rgba,fade=t=in:st={t0:.2f}:d=0.3:alpha=1,fade=t=out:st={t1-0.3:.2f}:d=0.3:alpha=1[o{j}];"
         f"[{last}][o{j}]overlay=x=0:y='if(lt(t,{t0}),18,if(lt(t,{t0+0.35}),18*(1-(t-{t0})/0.35),0))':enable='between(t,{t0},{t1})'[w{j}];"); last=f'w{j}'
fc+=(f"[{last}]subtitles={OUT}/subs.ass:fontsdir={SK}scripts[v];")
MUSIC=os.environ.get('MUSIC'); MDB=float(os.environ.get('MUSICDB','-13'))
if MUSIC:   # background music: loudnormed, set MDB below, sidechain-ducked under every voice, faded in/out
    inp+=['-stream_loop','-1','-i',MUSIC]; mi=n; n+=1
    vmix=[x for x in mix if x.startswith('[v') or x=='[0:a]']; fxm=[x for x in mix if x not in vmix]
    fc+=(f"{''.join(vmix)}amix=inputs={len(vmix)}:normalize=0:duration=first,asplit=2[vbus][vkey];"
         f"[{mi}:a]atrim=0:{total:.3f},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,loudnorm=I=-16:TP=-2:LRA=11,aresample=48000,"
         f"volume={MDB}dB,volume='if(lt(t,{HOOK_END:.2f}),0.56,1)':eval=frame,afade=t=in:d=0.4,afade=t=out:st={total-1.6:.2f}:d=1.6[mus];"
         f"[mus][vkey]sidechaincompress=threshold=0.03:ratio=6:attack=15:release=350:makeup=1[mduck];"
         f"[vbus][mduck]{''.join(fxm)}amix=inputs={2+len(fxm)}:normalize=0:duration=first,loudnorm=I=-15:TP=-1.5:LRA=11,aresample=48000,alimiter=limit=0.84:level=false[a]")
else:
    fc+=f"{''.join(mix)}amix=inputs={len(mix)}:normalize=0:duration=first,loudnorm=I=-15:TP=-1.5:LRA=11,aresample=48000,alimiter=limit=0.84:level=false[a]"
subprocess.run(['ffmpeg','-loglevel','error','-y']+inp+['-filter_complex',fc,'-map','[v]','-map','[a]','-t',f'{total:.3f}',
  '-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709',
  '-c:a','aac','-b:a','192k','-movflags','+faststart',OUT+'/final.mp4'],check=True)
subprocess.run(['ffmpeg','-loglevel','error','-y','-i',OUT+'/final.mp4','-vf','scale=540:-2','-c:v','libx264','-crf','24','-preset','medium','-c:a','aac','-b:a','128k','-movflags','+faststart',OUT+'/preview540.mp4'],check=True)
print('final',total)
