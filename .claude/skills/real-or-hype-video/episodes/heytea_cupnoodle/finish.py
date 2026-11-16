# usage: finish.py <workdir> -> out/final.mp4 (1080p) + out/preview540.mp4
# Subtitles (≤3 words, current word yellow, Montserrat ExtraBold 66 / 6px outline, MarginV 430), title card, narration, SFX, loudness.
import os,sys,json,subprocess,numpy as np
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); from segs import *
W=sys.argv[1]; os.chdir(W); J=json.load(open('out/starts.json')); st=J['starts']; total=st['_end']
SK='/home/user/real-or-hype/.claude/skills/real-or-hype-video/'
lines=json.load(open('vo/lines.json'))
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
for k,s,e in J['vo']: allw.append(align(VOTXT.get(k,lines[k]),f'vo/{k}.wav',s))
for sid,txt in REAL.items(): allw.append(align(txt,f'out/seg/{sid}.mov',st[sid]))
def ts(x): return f'{int(x//3600)}:{int(x%3600//60):02d}:{x%60:05.2f}'
ass=open(SK+'episodes/heytea_cupnoodle/ass_head.txt').read()
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
            ass+=f'Dialogue: 0,{ts(a)},{ts(max(e,a+0.05))},main,,0,0,0,,{txt}\n'
open('out/subs.ass','w').write(ass)
# audio: base (room sound + his lines) + narration + effects
def peak_db(f): return 20*np.log10(np.abs(pcm(f)).max()+1e-9)
inp=['-i','out/base.mov','-loop','1','-t',str(total),'-i','title.png']; fc=''; mix=['[0:a]']; n=2
for k,s,e in J['vo']:
    ms=int(s*1000); inp+=['-i',f'vo/{k}.wav']
    fc+=f'[{n}:a]aresample=48000,aformat=channel_layouts=stereo,loudnorm=I=-15:TP=-1.5:LRA=11,aresample=48000,adelay={ms}|{ms}[v{n}];'; mix.append(f'[v{n}]'); n+=1
fx=[('whoosh_es',0.31,st[s],0.45) for s in WHOOSH]+[('pop_es',0.0,0.12,0.40)]
for name,po,t,vol in fx:
    f=SK+f'sfx/{name}.wav'; g=10**((-6-peak_db(f))/20)*vol; ms=max(0,int((t-po)*1000)); inp+=['-i',f]
    fc+=f'[{n}:a]aresample=48000,aformat=channel_layouts=stereo,volume={g:.4f},adelay={ms}|{ms}[x{n}];'; mix.append(f'[x{n}]'); n+=1
t0,t1=st[TITLE[0]],st[TITLE[1]]+(st[SEGS[[s[0] for s in SEGS].index(TITLE[1])+1][0]]-st[TITLE[1]])
fc+=(f"[1:v]format=rgba,fade=t=in:st=0:d=0.15:alpha=1,fade=t=out:st={t1-0.2:.2f}:d=0.2:alpha=1[ti];"
     f"[0:v][ti]overlay=enable='between(t,{t0},{t1})'[v1];[v1]subtitles=out/subs.ass:fontsdir={SK}scripts[v];"
     f"{''.join(mix)}amix=inputs={len(mix)}:normalize=0:duration=first,loudnorm=I=-15:TP=-1.5:LRA=11,aresample=48000,alimiter=limit=0.84:level=false[a]")
subprocess.run(['ffmpeg','-loglevel','error','-y']+inp+['-filter_complex',fc,'-map','[v]','-map','[a]','-t',f'{total:.3f}',
  '-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709',
  '-c:a','aac','-b:a','192k','-movflags','+faststart','out/final.mp4'],check=True)
subprocess.run(['ffmpeg','-loglevel','error','-y','-i','out/final.mp4','-vf','scale=540:-2','-c:v','libx264','-crf','24','-preset','medium','-c:a','aac','-b:a','128k','-movflags','+faststart','out/preview540.mp4'],check=True)
print('final',total)
