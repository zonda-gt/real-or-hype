# Word-by-word subtitles (current word yellow). Known script text, timed by Whisper word timestamps on the exact audio used.
import sys,os,ast,subprocess,json,numpy as np
os.chdir(sys.argv[1]); st=ast.literal_eval(open(sys.argv[2]).read()); out=sys.argv[3]
from faster_whisper import WhisperModel
m=WhisperModel("small",device="cpu",compute_type="int8")
def words(f,ss=None,t=None):
    pre=['-ss',str(ss),'-t',str(t)] if ss is not None else []
    a=np.frombuffer(subprocess.run(['ffmpeg','-loglevel','error']+pre+['-i',f,'-ar','16000','-ac','1','-f','f32le','-'],capture_output=True).stdout,dtype=np.float32)
    segs,_=m.transcribe(a,language='en',word_timestamps=True,beam_size=5)
    return [(w.start,w.end) for s in segs for w in s.words]
def align(text,f,offset,ss=None,t=None):
    tw=text.split(); ww=words(f,ss,t)
    if not ww:   # no words recognised: time from the audio's own voiced span
        a=np.frombuffer(subprocess.run(['ffmpeg','-loglevel','error','-i',f,'-ac','1','-ar','16000','-f','f32le','-'],capture_output=True).stdout,dtype=np.float32)
        e=np.array([np.sqrt(np.mean(a[i:i+160]**2)) for i in range(0,len(a)-160,160)]); v=np.where(e>e.max()*0.1)[0]
        ww=[(v[0]*0.01,(v[-1]+1)*0.01)]; print('  fallback timing for',f)
    if len(ww)==len(tw): return [(offset+a,offset+b,w) for (a,b),w in zip(ww,tw)]
    s0,s1=ww[0][0],ww[-1][1]; L=sum(len(w) for w in tw); acc=0; res=[]
    for w in tw:
        a=s0+(s1-s0)*acc/L; acc+=len(w); res.append((offset+a,offset+s0+(s1-s0)*acc/L,w))
    return res
VO=sys.argv[4]; SEGDIR=sys.argv[6]; lines=json.loads(open(sys.argv[5]).read())
allw=[]
for key,sid,text in lines:
    if sid=='SEG':   # his own line: words from the rendered segment file
        allw.append(('main',align(text,f'{SEGDIR}/{key}.mp4',st[key])))
    else:
        off=st[sid]+0.2 if 'hook' in key else st[sid]+(0.25 if key.endswith('verdict') else 0.08)
        allw.append(('hook' if 'hook' in key else 'main',align(text,f'{VO}/{key}.wav',off)))
def ts(x): return f'{int(x//3600)}:{int(x%3600//60):02d}:{x%60:05.2f}'
ass="""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 1

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: main,Montserrat ExtraBold,66,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,6,0,2,90,90,430,1
Style: hook,Montserrat ExtraBold,60,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,6,0,2,60,60,130,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
for style,ws in allw:
    # chunks of up to 3 words, break after punctuation
    chunks=[];cur=[]
    for w in ws:
        cur.append(w)
        if len(cur)==3 or w[2][-1] in '.,?!:': chunks.append(cur);cur=[]
    if cur: chunks.append(cur)
    for ci,ch in enumerate(chunks):
        end_chunk=chunks[ci+1][0][0] if ci+1<len(chunks) else ch[-1][1]+0.25
        for wi,(a,b,w) in enumerate(ch):
            e=ch[wi+1][0] if wi+1<len(ch) else end_chunk
            txt=' '.join(('{\\c&H1AE2FF&}'+x[2]+'{\\c&HFFFFFF&}') if j==wi else x[2] for j,x in enumerate(ch))
            ass+=f'Dialogue: 0,{ts(a)},{ts(max(e,a+0.05))},{style},,0,0,0,,{txt}\n'
open(out,'w').write(ass); print('subs',sum(len(w) for _,w in allw),'words')
