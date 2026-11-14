# overlays + word subtitles + narration + ducked music + SFX, then loudness to -15 LUFS / TP <= -1
import sys,os,json,subprocess,re,numpy as np
sys.path.insert(0,'.'); from lines import LINES
V=sys.argv[1]; D=f'out/{V}'; tl=json.load(open(f'{D}/timeline.json')); T=tl['total']
st={k:s for k,s in tl['vo']}
keys=[k for k,_ in tl['vo']]
slot={}   # slot start/end per line
for i,k in enumerate(keys):
    # slot starts = placement - lead; ends at next slot start
    pass
SK='../../.claude/skills/real-or-hype-video'
def dur(f): return float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f],capture_output=True,text=True).stdout)
lead={'A1':0.05,'C1':0.05}
s0={k:st[k]-lead.get(k,0.12) for k in keys}
s1={k:(s0[keys[i+1]] if i+1<len(keys) else T) for i,k in enumerate(keys)}
CARDS={'A':[('titleA','A1'),('price','A7')],
       'B':[('kenya','B1'),('china','B2'),('price_b','B6'),('tenx','B7')],
       'C':[('titleC','C1'),('name','C2'),('price','C4'),('time','C6')]}[V]
NOSUB={'A7','B1','B2','B6','B7','C2','C4','C6'}
# ---- subtitles (Whisper word stamps on the exact wav)
from faster_whisper import WhisperModel
m=WhisperModel("small",device="cpu",compute_type="int8")
def load(f): return np.frombuffer(subprocess.run(['ffmpeg','-loglevel','error','-i',f,'-ar','16000','-ac','1','-f','f32le','-'],capture_output=True).stdout,dtype=np.float32)
def ts(x): return f'{int(x//3600)}:{int(x%3600//60):02d}:{x%60:05.2f}'
ass=open(f'{SK}/scripts/subs.py').read().split('ass="""')[1].split('"""')[0]
for k in keys:
    if k in NOSUB: continue
    tw=LINES[k].split(); segs,_=m.transcribe(load(f'vo/{k}.wav'),language='en',word_timestamps=True,beam_size=5)
    ww=[(w.start,w.end) for s in segs for w in s.words]
    if len(ww)==len(tw): ws=[(st[k]+a,st[k]+b,w) for (a,b),w in zip(ww,tw)]
    else:   # spread script words over the voiced span by character length
        a0,a1=ww[0][0],ww[-1][1]; L=sum(len(w) for w in tw); acc=0; ws=[]
        for w in tw: a=a0+(a1-a0)*acc/L; acc+=len(w); ws.append((st[k]+a,st[k]+a0+(a1-a0)*acc/L,w))
        print('  proportional timing for',k,len(ww),len(tw))
    chunks=[];cur=[]
    for w in ws:
        cur.append(w)
        if len(cur)==3 or w[2][-1] in '.,?!:': chunks.append(cur);cur=[]
    if cur: chunks.append(cur)
    for ci,ch in enumerate(chunks):
        endc=chunks[ci+1][0][0] if ci+1<len(chunks) else min(ch[-1][1]+0.25,s1[k])
        for wi,(a,b,w) in enumerate(ch):
            e=ch[wi+1][0] if wi+1<len(ch) else endc
            txt=' '.join(('{\\c&H1AE2FF&}'+x[2]+'{\\c&HFFFFFF&}') if j==wi else x[2] for j,x in enumerate(ch))
            ass+=f'Dialogue: 0,{ts(a)},{ts(max(e,a+0.05))},main,,0,0,0,,{txt}\n'
open(f'{D}/subs.ass','w').write(ass)
# ---- video: overlays (2 frames before slot start... cards appear on the cut) + subs
inp=['-i',f'{D}/video.mp4']; fc='[0:v]null[v0];'; n=0
for i,(png,k) in enumerate(CARDS):
    inp+=['-loop','1','-t',str(T),'-i',f'ov/{png}.png']
    a,b=s0[k],s1[k]
    fc+=f"[{i+1}:v]format=rgba,{'fade=t=in:st=%.3f:d=0.12:alpha=1'%a if a>0.1 else 'null'}[o{i}];[v{i}][o{i}]overlay=0:0:enable='between(t,{a:.3f},{b-0.02:.3f})'[v{i+1}];"
    n=i+1
fc+=f"[v{n}]ass={D}/subs.ass:fontsdir={SK}/scripts[vout];"
# ---- audio
ai=len(CARDS)+1; ains=[]
for k in keys: ains+=['-i',f'vo/{k}.wav']
fca=''
for j,k in enumerate(keys):
    ms=int(st[k]*1000); fca+=f'[{ai+j}:a]aresample=48000,aformat=channel_layouts=stereo,adelay={ms}|{ms}[a{j}];'
fca+=''.join(f'[a{j}]' for j in range(len(keys)))+f'amix=inputs={len(keys)}:normalize=0,apad=whole_dur={T}[vo];[vo]asplit=2[vo1][key];'
mi=ai+len(keys); ains+=['-i','music/m1.mp3']
fca+=f'[{mi}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{T},loudnorm=I=-16:TP=-2:LRA=11,volume=-4dB,afade=t=in:d=0.3,afade=t=out:st={T-1.2:.2f}:d=1.2[mus];'
fca+='[mus][key]sidechaincompress=threshold=0.03:ratio=6:attack=15:release=350:makeup=1[musd];'
# sfx: whoosh into the cut after the hook, pop on each mid-screen card
def peak_db(f):
    a=load(f); return 20*np.log10(np.abs(a).max()+1e-9)
ev=[('whoosh_es',0.31,s0[keys[1]],0.40)]+[('pop_es',0.0,s0[k]+0.02,0.35) for png,k in CARDS if s0[k]>0.5]
si=mi+1; sl=[]
for j,(nm,po,t,v) in enumerate(ev):
    f=f'{SK}/sfx/{nm}.wav'; ains+=['-i',f]; g=10**((-6-peak_db(f))/20)*v; ms=max(0,int((t-po)*1000))
    fca+=f'[{si+j}:a]aresample=48000,aformat=channel_layouts=stereo,volume={g:.4f},adelay={ms}|{ms}[s{j}];'; sl.append(f'[s{j}]')
fca+='[vo1][musd]'+''.join(sl)+f'amix=inputs={2+len(sl)}:normalize=0:duration=first[mix]'
tmp=f'{D}/premix.mp4'
subprocess.run(['ffmpeg','-y','-loglevel','error']+inp+ains+['-filter_complex',fc+fca,'-map','[vout]','-map','[mix]','-t',str(T),
    '-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-c:a','pcm_s16le',f'{D}/premix.mkv'],check=True)
# loudness: measure, gain to -15 LUFS, limiter
r=subprocess.run(['ffmpeg','-hide_banner','-i',f'{D}/premix.mkv','-vn','-af','ebur128','-f','null','-'],capture_output=True,text=True).stderr
I=float(re.findall(r'I:\s+(-?[\d.]+) LUFS',r)[-1]); g=-15-I
subprocess.run(['ffmpeg','-y','-loglevel','error','-i',f'{D}/premix.mkv','-af',f'volume={g:.2f}dB,alimiter=limit=0.84:level=false','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart',f'{D}/giraffe_{V}_1080.mp4'],check=True)
r=subprocess.run(['ffmpeg','-hide_banner','-i',f'{D}/giraffe_{V}_1080.mp4','-vn','-af','ebur128=peak=true','-f','null','-'],capture_output=True,text=True).stderr
print(V,'premix',I,'final I',re.findall(r'I:\s+(-?[\d.]+) LUFS',r)[-1],'TP',re.findall(r'Peak:\s+(-?[\d.]+) dBFS',r)[-1],'dur',round(T,2))
subprocess.run(['ffmpeg','-y','-loglevel','error','-i',f'{D}/giraffe_{V}_1080.mp4','-vf','scale=540:960','-c:v','libx264','-crf','24','-preset','fast','-c:a','aac','-b:a','128k','-movflags','+faststart',f'{D}/giraffe_{V}_540.mp4'],check=True)
