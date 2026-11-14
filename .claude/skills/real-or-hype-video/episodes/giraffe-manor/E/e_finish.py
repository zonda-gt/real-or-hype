import json,subprocess,re,sys,numpy as np
sys.path.insert(0,'.'); from e_plan import *
tl=json.load(open('timeline.json')); T=tl['T']; st=tl['starts']; words=json.load(open('words.json'))
SK='../../../.claude/skills/real-or-hype-video'
cue_t={i:st[k] for k,(i,_) in enumerate(CUES)}; nxt={i:st[k+1] for k,(i,_) in enumerate(CUES)}
# ---- overlays: (png, start, end)
ovs=[('title',0.0,tl['collage_end']-0.02)]
lab={'Giraffe Manor':'l_manor','capybara':'l_capy','raccoons':'l_racc','red-crowned cranes':'l_crane','6:30 AM':'l_630'}
for txt,i in LABELS: ovs.append((lab[txt],cue_t[i]+0.15,nxt[i]-0.05))
for png,i0,i1 in CARDS: ovs.append((png,cue_t[i0],cue_t[i1]-0.03))
# ---- one-word captions (centred, small caps), skipped under the title and the cards
def ts(x): return f'{int(x//3600)}:{int(x%3600//60):02d}:{x%60:05.2f}'
ass='''[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: w,Poppins SemiBold,54,&H00FFFFFF,&H00FFFFFF,&H60000000,&H70000000,0,0,0,0,100,100,2,0,1,1.6,2.2,5,60,60,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
blocked=[(0,tl['collage_end'])]+[(cue_t[i0],cue_t[i1]) for _,i0,i1 in CARDS]
tok=[w[2] for w in words]
fix={'$1400.':'$1,400','$1400':'$1,400'}
merged=[]
for k,(a,b,w) in enumerate(words):
    if w.startswith('.') and merged: merged[-1]=(merged[-1][0],b,merged[-1][2]+':'+w[1:].rstrip('.')); continue
    merged.append((a,b,fix.get(w,w)))
words=merged; script=[w[2] for w in words]
for k,(a,b,_) in enumerate(words):
    if any(x0-0.01<=a<x1 for x0,x1 in blocked): continue
    e=words[k+1][0] if k+1<len(words) and words[k+1][0]-b<0.35 else b+0.15
    w=re.sub(r'[.,?!]$','',script[k]).upper()
    ass+=f'Dialogue: 0,{ts(a-0.03)},{ts(e-0.03)},w,,0,0,0,,{w}\n'
open('subs.ass','w').write(ass)
inp=['-i','video.mp4']; fc='[0:v]null[v0];'
for k,(png,a,b) in enumerate(ovs):
    inp+=['-loop','1','-t',f'{T:.3f}','-i',f'ov/{png}.png']
    fade='null' if a<0.05 else f'fade=t=in:st={a:.3f}:d=0.15:alpha=1'
    fc+=f"[{k+1}:v]format=rgba,{fade}[o{k}];[v{k}][o{k}]overlay=0:0:enable='between(t,{a:.3f},{b:.3f})'[v{k+1}];"
fc+=f"[v{len(ovs)}]ass=subs.ass:fontsdir=../fonts[vout];"
# ---- audio: VO + warm music bed ducked under it + small sfx
def load(f): return np.frombuffer(subprocess.run(['ffmpeg','-loglevel','error','-i',f,'-ac','1','-f','f32le','-'],capture_output=True).stdout,dtype=np.float32)
def pk(f): return 20*np.log10(np.abs(load(f)).max()+1e-9)
n=len(ovs)+1; ain=['-i','vo.wav','-i','../music/m1.mp3']
fa=f'[{n}:a]aresample=48000,aformat=channel_layouts=stereo,apad=whole_dur={T:.3f}[vo];[vo]asplit=2[vo1][key];'
fa+=f'[{n+1}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{T:.3f},loudnorm=I=-16:TP=-2,volume=-6dB,afade=t=out:st={T-1.2:.2f}:d=1.2[mus];[mus][key]sidechaincompress=threshold=0.03:ratio=6:attack=15:release=300[musd];'
ev=[('whoosh_es',0.31,tl['collage_end'],0.35)]+[('pop_es',0.0,a,0.25) for png,a,b in ovs[1:]]
sl=[]
for j,(nm,po,t,v) in enumerate(ev):
    f=f'{SK}/sfx/{nm}.wav'; ain+=['-i',f]; g=10**((-6-pk(f))/20)*v; ms=max(0,int((t-po)*1000))
    fa+=f'[{n+2+j}:a]aresample=48000,aformat=channel_layouts=stereo,volume={g:.4f},adelay={ms}|{ms}[s{j}];'; sl.append(f'[s{j}]')
fa+='[vo1][musd]'+''.join(sl)+f'amix=inputs={2+len(sl)}:normalize=0:duration=first[mix]'
subprocess.run(['ffmpeg','-y','-loglevel','error']+inp+ain+['-filter_complex',fc+fa,'-map','[vout]','-map','[mix]','-t',f'{T:.3f}','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-c:a','pcm_s16le','premix.mkv'],check=True)
r=subprocess.run(['ffmpeg','-hide_banner','-i','premix.mkv','-vn','-af','ebur128','-f','null','-'],capture_output=True,text=True).stderr
I=float(re.findall(r'I:\s+(-?[\d.]+) LUFS',r)[-1])
subprocess.run(['ffmpeg','-y','-loglevel','error','-i','premix.mkv','-af',f'volume={-15-I:.2f}dB,alimiter=limit=0.84:level=false','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart','giraffe_E_1080.mp4'],check=True)
r=subprocess.run(['ffmpeg','-hide_banner','-i','giraffe_E_1080.mp4','-vn','-af','ebur128=peak=true','-f','null','-'],capture_output=True,text=True).stderr
print('final I',re.findall(r'I:\s+(-?[\d.]+) LUFS',r)[-1],'TP',re.findall(r'Peak:\s+(-?[\d.]+) dBFS',r)[-1],'dur',round(T,2))
subprocess.run(['ffmpeg','-y','-loglevel','error','-i','giraffe_E_1080.mp4','-vf','scale=540:960','-c:v','libx264','-crf','23','-preset','fast','-c:a','aac','-b:a','128k','-movflags','+faststart','giraffe_E_540.mp4'],check=True)
