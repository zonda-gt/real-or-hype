#!/usr/bin/env python3
# render.py VAR outdir  -> base.mp4 (footage only), final.mp4 (+overlays, subs, VO, sfx), timeline.json
import sys,os,json,subprocess
sys.path.insert(0,os.path.dirname(__file__))
from variants import V
import overlays
S=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
var=sys.argv[1]; out=sys.argv[2]; os.makedirs(out+'/seg',exist_ok=True); os.makedirs(out+'/ov',exist_ok=True)
segs=V[var]; FPS=30
SFX={'buzz':('/home/user/real-or-hype/.claude/skills/real-or-hype-video/sfx/buzz_el.wav',0.0,-12),
     'ding':('/home/user/real-or-hype/.claude/skills/real-or-hype-video/sfx/ding.wav',0.0,-14),
     'whoosh':('/home/user/real-or-hype/.claude/skills/real-or-hype-video/sfx/whoosh.wav',-0.30,-16)}
vo=lambda k: json.load(open(f'{S}/vo/{k}.json'))
disp=json.load(open(f'{S}/vo/lines_display.json'))
def r(x): return round(x*FPS)/FPS
# group durations
groups=[];cur=None
for i,s in enumerate(segs):
    if s['vo'] or cur is None: cur={'segs':[i],'vo':s['vo']}; groups.append(cur)
    else: cur['segs'].append(i)
for g in groups:
    mins=[max(segs[i]['dur'],0.1) for i in g['segs']]
    first=segs[g['segs'][0]]; lead=0.3 if 'buzz' in first['sfx'] else 0.12
    if g is groups[0]: lead=0.05
    need=(lead+vo(g['vo'])['dur']+first['pad']) if g['vo'] else 0
    if len(g['segs'])==1: mins[0]=max(mins[0],need)
    else: mins[-1]=max(mins[-1],need-sum(mins[:-1]))
    for i,m in zip(g['segs'],mins): segs[i]['D']=r(m)
    g['lead']=lead
t=0; tl=[]
for i,s in enumerate(segs):
    s['start']=t; t=r(t+s['D'])
total=t
# render segments
for i,s in enumerate(segs):
    f=f'{out}/seg/{i:02d}.mp4'
    if s['band']:
        vf=(f"split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,gblur=sigma=40,eq=brightness=-0.08[bg];"
            f"[b]scale=1080:-2:flags=lanczos[fg];[bg][fg]overlay=0:(H-h)/2,fps={FPS},setsar=1,format=yuv420p")
    else:
        Z=s['z']; W,H=int(1080*Z),int(1920*Z)
        vf=f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920:(iw-1080)*{s['ax']}:(ih-1920)*{s['ay']},fps={FPS},setsar=1,format=yuv420p"
    subprocess.run(['ffmpeg','-v','error','-y','-ss',f"{s['t']:.3f}",'-i',f"{S}/media/dy/{s['clip']}.mp4",'-t',f"{s['D']:.4f}",'-filter_complex' if s['band'] else '-vf',vf,'-an','-c:v','libx264','-preset','medium','-crf','15','-r',str(FPS),f],check=True)
    n=int(subprocess.run(['ffprobe','-v','error','-count_frames','-select_streams','v:0','-show_entries','stream=nb_read_frames','-of','csv=p=0',f],capture_output=True,text=True).stdout)
    if n!=round(s['D']*FPS): print('frame mismatch',i,n,round(s['D']*FPS))
open(f'{out}/seg/list.txt','w').write(''.join(f"file '{i:02d}.mp4'\n" for i in range(len(segs))))
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',f'{out}/seg/list.txt','-c','copy',f'{out}/base.mp4'],check=True)
# overlays
ovs=[]
for i,s in enumerate(segs):
    if s['tag']:
        p=f"{out}/ov/tag{i:02d}.png"; overlays.tag(*s['tag'],p); ovs.append((p,s['start'],s['start']+s['D']))
    if s['big']:
        p=f"{out}/ov/big{i:02d}.png"; overlays.big(s['big'],p)
        a=s['start']; 
        if s['big']=='SPOTS':  # show from the word "Comment"
            g=[g for g in groups if i in g['segs']][0]
            if g['vo']:
                w=[x for x in vo(g['vo'])['words'] if x['w'].lower().startswith('comment')][0]; a=segs[g['segs'][0]]['start']+g['lead']+w['s']-2/FPS
            else: continue
            ovs.append((p,a,total))
        elif s['big']=='REAL': ovs.append((p,s['start'],s['start']+s['D']))
        else: ovs.append((p,s['start'],s['start']+1.6))
# VO placement + subtitles
vos=[];words=[]
for g in groups:
    if not g['vo']: continue
    st=segs[g['segs'][0]]['start']+g['lead']; v=vo(g['vo'])
    vos.append((f"{S}/vo/{g['vo']}.wav",st))
    dw=disp[g['vo']].split()
    assert len(dw)==len(v['words']),(g['vo'],dw,[x['w'] for x in v['words']])
    words.append([(st+x['s'],st+x['e'],d) for x,d in zip(v['words'],dw)])
    # check no overlap with next group
skip_sub=set()
def ts(x): return f'{int(x//3600)}:{int(x%3600//60):02d}:{x%60:05.2f}'
ass="""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 1

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: main,Montserrat ExtraBold,66,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,6,0,2,90,90,430,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
for ws in words:
    chunks=[];c=[]
    for w in ws:
        c.append(w)
        if len(c)==3 or w[2][-1] in '.,?!:': chunks.append(c);c=[]
    if c: chunks.append(c)
    for ci,ch in enumerate(chunks):
        endc=chunks[ci+1][0][0] if ci+1<len(chunks) else ch[-1][1]+0.25
        for wi,(a,b,w) in enumerate(ch):
            e=ch[wi+1][0] if wi+1<len(ch) else endc
            txt=' '.join(('{\\c&H00D4FF&}'+x[2]+'{\\c&HFFFFFF&}') if j==wi else x[2] for j,x in enumerate(ch))
            ass+=f'Dialogue: 0,{ts(a-0.05)},{ts(max(e-0.05,a))},main,,0,0,0,,{txt}\n'
open(f'{out}/subs.ass','w').write(ass)
# check VO overlap
vv=sorted([(st,st+vo(k)['dur'],k) for (p,st) in vos for k in [os.path.basename(p)[:-4]]])
for a,b in zip(vv,vv[1:]):
    if a[1]+0.05>b[0]: print('VO OVERLAP',a,b)
if vv[-1][1]>total-0.1: print('VO runs past end',vv[-1],total)
# video: overlays + subs
inp=['-i',f'{out}/base.mp4']; fc='[0:v]'; last='0:v'; k=0
chain=[]
for j,(p,a,b) in enumerate(ovs):
    inp+=['-i',p]; chain.append(f"[{last}][{j+1}:v]overlay=0:0:enable='between(t,{a:.3f},{b-0.001:.3f})'[o{j}]"); last=f'o{j}'
SKD='/home/user/real-or-hype/.claude/skills/real-or-hype-video/scripts'
chain.append(f"[{last}]subtitles={out}/subs.ass:fontsdir={SKD}[vout]")
# audio
ai=len(ovs)+1; aud=[]; ac=[]
for n,(p,st) in enumerate(vos):
    inp+=['-i',p]; ac.append(f"[{ai}:a]aresample=48000,aformat=channel_layouts=stereo,adelay={int(st*1000)}|{int(st*1000)}[a{n}]"); aud.append(f'a{n}'); ai+=1
for i,s in enumerate(segs):
    for e in s['sfx']:
        p,off,db=SFX[e]; st=max(0,s['start']+off)
        inp+=['-i',p]; ac.append(f"[{ai}:a]aresample=48000,aformat=channel_layouts=stereo,volume={db}dB,adelay={int(st*1000)}|{int(st*1000)}[a{len(aud)}]"); aud.append(f'a{len(aud)}'); ai+=1
ac.append(''.join(f'[{x}]' for x in aud)+f"amix=inputs={len(aud)}:normalize=0:duration=longest,apad,atrim=0:{total:.3f}[aout]")
fc=';'.join(chain+ac)
subprocess.run(['ffmpeg','-v','error','-y']+inp+['-filter_complex',fc,'-map','[vout]','-map','[aout]','-c:v','libx264','-preset','slow','-crf','17','-pix_fmt','yuv420p','-r',str(FPS),'-c:a','pcm_s24le','-t',f'{total:.3f}',f'{out}/premix.mov'],check=True)
import re
m=subprocess.run(['ffmpeg','-nostats','-i',f'{out}/premix.mov','-map','0:a','-af','ebur128=framelog=quiet','-f','null','-'],capture_output=True,text=True).stderr
I=float(re.findall(r'I:\s+(-?[\d.]+) LUFS',m)[-1]); g=-15.0-I
subprocess.run(['ffmpeg','-v','error','-y','-i',f'{out}/premix.mov','-map','0:v','-map','0:a','-c:v','copy','-af',f'volume={g:.2f}dB,alimiter=limit=0.75:level=false:attack=1:release=50,aresample=48000','-c:a','aac','-b:a','192k','-movflags','+faststart',f'{out}/final.mp4'],check=True)
os.remove(f'{out}/premix.mov')
json.dump({'total':total,'segs':[{k:s[k] for k in ('clip','t','D','start','tag','vo','big')} for s in segs],'vo':[(os.path.basename(p),st) for p,st in vos]},open(f'{out}/timeline.json','w'),indent=1,ensure_ascii=False)
print(var,'total',round(total,2),'s', len(segs),'segs')
