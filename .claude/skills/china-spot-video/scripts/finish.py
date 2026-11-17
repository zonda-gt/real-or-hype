# Graphics + one-word captions + VO + ducked music + sfx, mastered to -15 LUFS / TP <= -1. usage: finish.py <workdir> <name>
# Writes <name>_1080.mp4 and <name>_540.mp4 in <workdir>. Run graphics.py and render_cut.py first.
import json,subprocess,re,sys,os,numpy as np
W,NAME=sys.argv[1],sys.argv[2]; sys.path.insert(0,W); import plan as P; os.chdir(W)
SK=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
tl=json.load(open('timeline.json')); T=tl['T']; words=json.load(open('words.json')); LEAD=getattr(P,'LEAD',0.10)
cue_starts=dict(zip(tl['cue_words'],tl['starts'])); allst=sorted(tl['starts'])
def wt(i): return cue_starts.get(i,words[i][0]-LEAD)
def until_next_cut(t): return next((s for s in allst if s>t+0.05),T)
ovs=[('title',0.0,tl['collage_end']-0.02)]
for k,(_,i) in enumerate(getattr(P,'LABELS',[])): a=wt(i)+0.15; ovs.append((f'label{k}',a,until_next_cut(a)-0.05))
for k,(_,_,_,i0,i1) in enumerate(getattr(P,'CARDS',[])): ovs.append((f'card{k}',wt(i0),wt(i1)-0.03))
if getattr(P,'CTA',None): ovs.append(('cta',wt(P.CTA[1]),T))
# captions: one word at a time, small caps, centred; hidden under title/cards/CTA
def ts(x): return f'{int(x//3600)}:{int(x%3600//60):02d}:{x%60:05.2f}'
ass=('[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\n\n[V4+ Styles]\n'
 'Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n'
 'Style: w,Poppins SemiBold,54,&H00FFFFFF,&H00FFFFFF,&H60000000,&H70000000,0,0,0,0,100,100,2,0,1,1.6,2.2,5,60,60,0,1\n\n[Events]\n'
 'Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n')
blocked=[(0,tl['collage_end'])]+[(wt(c[3]),wt(c[4])) for c in getattr(P,'CARDS',[])]+([(wt(P.CTA[1]),T)] if getattr(P,'CTA',None) else [])
FIX=getattr(P,'CAPTION_FIX',{})
toks=[]
for a,b,w in words:   # Whisper splits "6:30" as "6" ".30" and "wake-up" as "wake" "-up": merge; CAPTION_FIX maps misheard tokens ('' = drop)
    if w.startswith('.') and toks: toks[-1]=(toks[-1][0],b,toks[-1][2]+':'+w[1:].rstrip('.')); continue
    if w.startswith('-') and toks: toks[-1]=(toks[-1][0],b,toks[-1][2]+w); continue
    w=FIX.get(w,w)
    if w=='' and toks: toks[-1]=(toks[-1][0],b,toks[-1][2]); continue
    toks.append((a,b,w))
for k,(a,b,w) in enumerate(toks):
    if any(x0-0.01<=a<x1 for x0,x1 in blocked): continue
    e=toks[k+1][0] if k+1<len(toks) and toks[k+1][0]-b<0.35 else b+0.15
    ass+=f'Dialogue: 0,{ts(a-0.03)},{ts(e-0.03)},w,,0,0,0,,{re.sub(r"[.,?!]$","",w).upper()}\n'
open('subs.ass','w').write(ass)
inp=['-i','video.mp4']; fc='[0:v]null[v0];'
for k,(png,a,b) in enumerate(ovs):
    inp+=['-loop','1','-t',f'{T:.3f}','-i',f'ov/{png}.png']; fade='null' if a<0.05 else f'fade=t=in:st={a:.3f}:d=0.15:alpha=1'
    fc+=f"[{k+1}:v]format=rgba,{fade}[o{k}];[v{k}][o{k}]overlay=0:0:enable='between(t,{a:.3f},{b:.3f})'[v{k+1}];"
fc+=f"[v{len(ovs)}]ass=subs.ass:fontsdir={SK}/fonts[vout];"
def pk(f): return 20*np.log10(np.abs(np.frombuffer(subprocess.run(['ffmpeg','-loglevel','error','-i',f,'-ac','1','-f','f32le','-'],capture_output=True).stdout,dtype=np.float32)).max()+1e-9)
music=getattr(P,'MUSIC',f'{SK}/sfx/music_marimba_el.mp3'); n=len(ovs)+1; ain=['-i','vo.wav','-i',music]
fa=f'[{n}:a]aresample=48000,aformat=channel_layouts=stereo,apad=whole_dur={T:.3f}[vo];[vo]asplit=2[vo1][key];'
fa+=f'[{n+1}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{T:.3f},loudnorm=I=-16:TP=-2,volume={getattr(P,"MUSIC_DB",-8)}dB,afade=t=out:st={T-1.2:.2f}:d=1.2[mus];[mus][key]sidechaincompress=threshold=0.03:ratio=6:attack=15:release=300[musd];'
# pops land 0.15 s BEFORE the word that triggers the graphic, never on it (a pop on the word masked "capybaras" and "giraffe")
trig=[wt(i) for _,i in getattr(P,'LABELS',[])]+[wt(c[3]) for c in getattr(P,'CARDS',[])]+([wt(P.CTA[1])] if getattr(P,'CTA',None) else [])
ev=[('whoosh_es',0.31,tl['collage_end'],0.30)]+[('pop_es',0.0,t-0.05,0.18) for t in trig]
sl=[]
for j,(nm,po,t,v) in enumerate(ev):
    f=f'{SK}/sfx/{nm}.wav'; ain+=['-i',f]; g=10**((-6-pk(f))/20)*v; ms=max(0,int((t-po)*1000))
    fa+=f'[{n+2+j}:a]aresample=48000,aformat=channel_layouts=stereo,volume={g:.4f},adelay={ms}|{ms}[s{j}];'; sl.append(f'[s{j}]')
fa+='[vo1][musd]'+''.join(sl)+f'amix=inputs={2+len(sl)}:normalize=0:duration=first[mix]'
subprocess.run(['ffmpeg','-y','-loglevel','error']+inp+ain+['-filter_complex',fc+fa,'-map','[vout]','-map','[mix]','-t',f'{T:.3f}','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-c:a','pcm_s16le','premix.mkv'],check=True)
r=subprocess.run(['ffmpeg','-hide_banner','-i','premix.mkv','-vn','-af','ebur128','-f','null','-'],capture_output=True,text=True).stderr
I=float(re.findall(r'I:\s+(-?[\d.]+) LUFS',r)[-1])
subprocess.run(['ffmpeg','-y','-loglevel','error','-i','premix.mkv','-af',f'volume={-15-I:.2f}dB,alimiter=limit=0.84:level=false','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart',f'{NAME}_1080.mp4'],check=True)
r=subprocess.run(['ffmpeg','-hide_banner','-i',f'{NAME}_1080.mp4','-vn','-af','ebur128=peak=true','-f','null','-'],capture_output=True,text=True).stderr
print(f'{NAME}_1080.mp4  I',re.findall(r'I:\s+(-?[\d.]+) LUFS',r)[-1],'LUFS  TP',re.findall(r'Peak:\s+(-?[\d.]+) dBFS',r)[-1],'dBTP  dur',round(T,2))
subprocess.run(['ffmpeg','-y','-loglevel','error','-i',f'{NAME}_1080.mp4','-vf','scale=540:960','-c:v','libx264','-crf','23','-preset','fast','-c:a','aac','-b:a','128k','-movflags','+faststart',f'{NAME}_540.mp4'],check=True)
