# "Version A" renderer: a no-narration reel in the style of @nicole.inchina (long POV takes, one small
# meme-style text line, music only). usage: nicole_style.py <workdir> <name>   (reads <workdir>/plan_A.py)
# plan_A.py:
#   SRC={id:{'cut':0.14,'top':0.0,'pre':'delogo=x=..'}}  # optional bottom/top crop; 'pre' = filter before the crop (e.g. delogo a text band)
#   SHOTS=[(src,t_in,secs,x_centre[,speed])]  # hard cuts, in order; speed<1 slows (default 1)
#   TEXTS=[("line one\nline two",t0,t1[,y[,'box']])]  # small centred text (white, soft shadow); y = centre 0-1; 'box' = white label box (LABEL_SIZE, LABEL_MIN_W/H)
#   TEXT_Y=0.40; TEXT_SIZE=50                  # optional
#   MUSIC='path.mp3'; MUSIC_IN=0.0             # music bed and start offset
#   AMBIENT=[(shot_index,db)]                  # optional: keep a shot's own sound under the music
# Writes <name>_1080.mp4 and <name>_540.mp4, mastered to -15 LUFS, TP <= -1.
import sys,os,subprocess,json
from PIL import Image,ImageDraw,ImageFont,ImageFilter
W,NAME=sys.argv[1],sys.argv[2]; SK=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,W); import plan_A as P; os.chdir(W); os.makedirs('segA',exist_ok=True)
FPS=30; run=lambda c: subprocess.run(c,check=True)
def probe(src):
    s=json.loads(subprocess.run(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height,color_transfer:stream_side_data=rotation:stream_tags=rotate','-of','json',f'broll/{src}.mp4'],capture_output=True,text=True).stdout)['streams'][0]
    rot=int(float(next((d.get('rotation',0) for d in s.get('side_data_list',[]) if 'rotation' in d),s.get('tags',{}).get('rotate',0))))
    w,h=(s['height'],s['width']) if abs(rot)%180==90 else (s['width'],s['height'])   # ffmpeg autorotates, so crop in display orientation
    return w,h,s.get('color_transfer','')
def vf(src,x):
    w,h,tr=probe(src); o=getattr(P,'SRC',{}).get(src,{}); c=o.get('cut',0.0); top=o.get('top',0.0); ch=h*(1-c-top); cw=ch*1080/1920
    if cw>w: cw=w; ch=cw*1920/1080
    X=min(max(x*w-cw/2,0),w-cw); Y=int(h*top)//2*2
    tm='zscale=tin=arib-std-b67:min=bt2020nc:pin=bt2020:t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p,' if tr=='arib-std-b67' else ''
    pre=o.get('pre',''); pre=pre+',' if pre else ''
    return f"{tm}{pre}crop={int(cw)//2*2}:{int(ch)//2*2}:{int(X)}:{Y},scale=1080:1920:flags=lanczos,setsar=1"
segs=[]; t=0.0
for k,s in enumerate(P.SHOTS):
    src,tin,d,x=s[:4]; sp=s[4] if len(s)>4 else 1.0; nf=int(round((t+d)*FPS))-int(round(t*FPS)); o=f'segA/{k:03d}.mp4'
    run(['ffmpeg','-y','-loglevel','error','-ss',f'{tin:.3f}','-t',f'{nf/FPS*sp+0.3:.3f}','-i',f'broll/{src}.mp4','-vf',vf(src,x)+f',setpts=(PTS-STARTPTS)/{sp:.4f},fps={FPS}',
         '-frames:v',str(nf),'-an','-c:v','libx264','-preset','fast','-crf','16','-pix_fmt','yuv420p',o]); segs.append((o,t,d,src,tin,sp)); t+=d
T=t; open('concatA.txt','w').write(''.join(f"file '{os.path.abspath(o)}'\n" for o,*_ in segs))
run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i','concatA.txt','-c','copy','videoA.mp4'])
# text overlays (PNG, full frame)
font=ImageFont.truetype(f'{SK}/fonts/poppins-latin-600-normal.ttf',getattr(P,'TEXT_SIZE',50)); ov=[]
for k,tx in enumerate(P.TEXTS):
    txt,t0,t1=tx[:3]; ty=tx[3] if len(tx)>3 else getattr(P,'TEXT_Y',0.40)
    im=Image.new('RGBA',(1080,1920),(0,0,0,0)); d=ImageDraw.Draw(im); lines=txt.split('\n'); lh=int(font.size*1.25)
    y0=int(1920*ty)-lh*len(lines)//2
    sh=Image.new('RGBA',(1080,1920),(0,0,0,0)); sd=ImageDraw.Draw(sh)
    if len(tx)>4 and tx[4]=='box':   # Nicole-style label: black text on a white rounded box (also hides a burned-in subtitle band)
        lf=ImageFont.truetype(f'{SK}/fonts/poppins-latin-600-normal.ttf',getattr(P,'LABEL_SIZE',56)); lh2=int(lf.size*1.3)
        bw=max(tx[5] if len(tx)>5 else getattr(P,'LABEL_MIN_W',0),max(d.textlength(l,font=lf) for l in lines)+80); bh=max(getattr(P,'LABEL_MIN_H',0),lh2*len(lines)+44)
        cy=int(1920*ty); x0=(1080-bw)/2; y1=cy-bh/2
        d.rounded_rectangle([x0,y1,x0+bw,y1+bh],radius=26,fill=(255,255,255,245))
        for j,l in enumerate(lines):
            w=d.textlength(l,font=lf); d.text(((1080-w)/2,y1+(bh-lh2*len(lines))/2+j*lh2+4),l,font=lf,fill=(20,20,20))
        im.save(f'segA/text{k}.png'); ov.append((f'segA/text{k}.png',t0,min(t1,T))); continue
    for j,l in enumerate(lines):
        w=d.textlength(l,font=font); xx=(1080-w)/2; yy=y0+j*lh
        sd.text((xx+2,yy+3),l,font=font,fill=(0,0,0,200)); d.text((xx,yy),l,font=font,fill='white',stroke_width=2,stroke_fill=(0,0,0,110))
    sh=sh.filter(ImageFilter.GaussianBlur(4)); sh.alpha_composite(im); p=f'segA/text{k}.png'; sh.save(p); ov.append((p,t0,min(t1,T)))
ins=['-i','videoA.mp4']+sum([['-i',p] for p,*_ in ov],[]); fc=''; last='[0:v]'
for k,(p,t0,t1) in enumerate(ov):
    fc+=f"{last}[{k+1}:v]overlay=0:0:enable='between(t,{t0:.2f},{t1:.2f})'[v{k}];"; last=f'[v{k}]'
# audio: music (+ optional ambient from shots)
mi=len(ov)+1; ins+=['-ss',f'{getattr(P,"MUSIC_IN",0.0):.2f}','-i',P.MUSIC]
fc+=f"[{mi}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{T:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.3,afade=t=out:st={T-1.5:.2f}:d=1.5[mus];"
amb=getattr(P,'AMBIENT',[]); mix='[mus]'
for j,(si,db) in enumerate(amb):
    o,t0,d,src,tin,sp=segs[si]; ins+=['-ss',f'{tin:.3f}','-t',f'{d*sp:.3f}','-i',f'broll/{src}.mp4']
    fc+=f"[{mi+1+j}:a]aresample=48000,aformat=channel_layouts=stereo,atempo={max(sp,0.5):.3f},volume={db}dB,adelay={int(t0*1000)}|{int(t0*1000)},apad[amb{j}];"; mix+=f'[amb{j}]'
fc+=f"{mix}amix=inputs={1+len(amb)}:normalize=0:duration=first,atrim=0:{T:.3f}[a]"
run(['ffmpeg','-y','-loglevel','error']+ins+['-filter_complex',fc,'-map',last,'-map','[a]','-c:v','libx264','-preset','medium','-crf','18','-maxrate','22M','-bufsize','44M','-pix_fmt','yuv420p','-r',str(FPS),
     '-c:a','pcm_s16le','-t',f'{T:.3f}','premixA.mov'])
# two-pass loudnorm to -15 LUFS, TP -1.5 (AAC adds a little), so the master lands at TP <= -1
m=subprocess.run(['ffmpeg','-hide_banner','-i','premixA.mov','-af','loudnorm=I=-15:TP=-2:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True).stderr
m=json.loads(m[m.rindex('{'):m.rindex('}')+1])
ln=f"loudnorm=I=-15:TP=-2:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true,alimiter=limit=0.84:level=false"
run(['ffmpeg','-y','-loglevel','error','-i','premixA.mov','-af',ln,'-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart',f'{NAME}_1080.mp4'])
run(['ffmpeg','-y','-loglevel','error','-i',f'{NAME}_1080.mp4','-vf','scale=540:960','-c:v','libx264','-crf','23','-c:a','copy','-movflags','+faststart',f'{NAME}_540.mp4'])
r=subprocess.run(['ffmpeg','-hide_banner','-i',f'{NAME}_1080.mp4','-af','ebur128=peak=true','-f','null','-'],capture_output=True,text=True).stderr
print(f'{NAME}_1080.mp4',round(T,2),'s |',' '.join(l.strip() for l in r.splitlines()[-12:] if l.strip().startswith(('I:','Peak:'))))
