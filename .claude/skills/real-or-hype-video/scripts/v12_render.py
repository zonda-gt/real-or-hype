import subprocess,os,sys
os.chdir(sys.argv[1]); V='VID_20260910_'; O='v9/ov/'
def src(n):
    for e in ('.MOV','.mp4'):
        if os.path.exists('orig/'+n+e): return 'orig/'+n+e
    raise SystemExit('missing '+n)
FULL='scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1'
TM='zscale=tin=arib-std-b67:min=bt2020nc:pin=bt2020:t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p,'
_hdr={}
def full(p):
    if p not in _hdr:
        _hdr[p]=subprocess.run(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=color_transfer','-of','csv=p=0',p],capture_output=True,text=True).stdout.strip().startswith('arib-std-b67')
    return (TM if _hdr[p] else '')+FULL
ENC=['-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-c:a','aac','-b:a','192k','-ar','48000','-ac','2']
def run(cmd):
    r=subprocess.run(cmd,capture_output=True,text=True)
    if r.returncode: print(r.stderr[-1500:]); sys.exit(1)
AFMT='aresample=48000,aformat=channel_layouts=stereo'
# (id, kind, args, dur, narr(a,b) or None)
S=[
 ('H1','hook',None,5.3,None),
 ('H2','react',(10.6,),2.0,None),
 ('O1','clip',('IMG_4775',13.0,0.0),2.35,'station'),
 ('O2','clip',(V+'162824_003',0.4,0.15),0.75,'bike'),
 ('O3','clip',(V+'162824_003',4.9,0.15),1.0,None),
 ('O5','panel',(V+'164346_011',0,4.4),2.6,'green'),
 ('O6','clip',(V+'173344_017',15.4,0.15),1.45,'pillar'),
 ('O7','clip',(V+'164338_010',0,0.15),1.45,None),
 ('O8','clip',(V+'173429_020',19,0.15),2.0,'close'),
 ('M1','clip',('IMG_4806',0.4,0.3),1.0,None),
 ('E1','talk',('IMG_4837',1.6,1.0,1.4),2.76,None),
 ('A1','clip',('IMG_4854',5.4,0.15),1.0,'inside'),
 ('A3','talk',('IMG_4855',33.86,1.0,1.4),2.064,None),
 ('I2','clip',(V+'173521_022',15,0.15),1.45,'gorilla2'),
 ('I3','clip',('IMG_4842',35,0.1),0.95,'thisbike'),
 ('I4','price',('IMG_4842',51.4,57.2),1.5,None),
 ('R1','clip',(V+'173552_023',9.5,0.1),2.75,'far'),
 ('R2','clip',(V+'175052_051',2.5,0.1),3.25,'skip'),
 ('V1','clip',('IMG_4793',0,0.15),3.4,'verdict'),
]
REACT='v5/react.mp4'; HER='react/DdMSIVcJBwK.mp4'
REACTV='scale=1080:1920,fps=30,setsar=1'
starts={}; t=0; segs=[]
for sid,kind,args,d,narr in S:
    out=f'v12/seg/{sid}.mp4'; starts[sid]=t
    if kind=='hook':
        fc=(f'[0:v]{REACTV}[bg];[1:v]setpts=PTS/1.3,scale=594:1056,fps=30,format=rgba[c0];[2:v]format=gray[m];[c0][m]alphamerge[c1];'
            f'[bg][c1]overlay=54:634[v1];[v1][3:v]overlay[v2];[v2][4:v]overlay[v];'
            f'[1:a]{AFMT},atempo=1.3,volume=0.22,afade=t=out:st={d-0.5}:d=0.5[m];[5:a]{AFMT},loudnorm=I=-14:TP=-1.5,adelay=200|200,apad[t];[m][t]amix=inputs=2:normalize=0:duration=first[a]')
        cmd=['ffmpeg','-loglevel','error','-y','-ss','0.8','-t',str(d),'-i',REACT,'-ss','0.5','-t',str(d*1.3+0.1),'-i',HER,'-i',O+'m_card.png','-i',O+'pill.png','-i',O+'credit.png','-i','v11/vo/hook.wav',
             '-filter_complex',fc,'-map','[v]','-map','[a]','-t',str(d)]+ENC+[out]
    elif kind=='react':
        fc=f'[0:v]{REACTV}[v];anullsrc=r=48000:cl=stereo[a]'
        cmd=['ffmpeg','-loglevel','error','-y','-ss',str(args[0]),'-t',str(d),'-i',REACT,'-filter_complex',fc,'-map','[v]','-map','[a]','-t',str(d)]+ENC+[out]
    elif kind=='panel':
        n,a,herin=args
        fc=(f'[0:v]{full(src(n))}[bg];[1:v]scale=760:-2,crop=760:700:0:(ih-700)/2,fps=30,format=rgba[p0];[2:v]format=gray[m];[p0][m]alphamerge[p1];'
            f'[bg][p1]overlay=160:1060[v1];[v1][3:v]overlay[v2];[v2][4:v]overlay[v];[0:a]{AFMT},volume=0.15[a]')
        cmd=['ffmpeg','-loglevel','error','-y','-ss',str(a),'-t',str(d),'-i',src(n),'-ss',str(herin),'-t',str(d),'-i',HER,'-i',O+'m_panel.png','-i',O+'l_online.png','-i',O+'l_real.png',
             '-filter_complex',fc,'-map','[v]','-map','[a]','-t',str(d)]+ENC+[out]
    elif kind=='insert':
        n,a,vol,ins=args
        fc=(f'[0:v]{full(src(n))}[bg];[1:v]scale=460:818:force_original_aspect_ratio=increase,crop=460:818,fps=30,format=rgba[p0];[2:v]format=gray[m];[p0][m]alphamerge[p1];'
            f'[bg][p1]overlay=560:960[v];[0:a]{AFMT},volume={vol}[ba];[1:a]{AFMT},volume=1.3,apad[ia];[ba][ia]amix=inputs=2:normalize=0:duration=first[a]')
        cmd=['ffmpeg','-loglevel','error','-y','-ss',str(a),'-t',str(d),'-i',src(n),'-i',ins,'-i',O+'m_ins.png','-filter_complex',fc,'-map','[v]','-map','[a]','-t',str(d)]+ENC+[out]
    elif kind=='price':
        n,a,aa=args
        fc=f'[0:v]{full(src(n))}[v];[1:a]{AFMT},atempo=1.15,highpass=f=80,loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000,adelay=150|150,afade=t=out:st={d-0.06:.3f}:d=0.06,apad[a]'
        cmd=['ffmpeg','-loglevel','error','-y','-ss',str(a),'-t',str(d),'-i',src(n),'-ss',str(aa),'-t','1.6','-i',src(n),'-filter_complex',fc,'-map','[v]','-map','[a]','-t',str(d)]+ENC+[out]
    elif kind=='talk':
        n,a,vol,sp=args
        fc=f'[0:v]setpts=PTS/{sp},{full(src(n))}[v];[0:a]{AFMT},atempo={sp},highpass=f=80,loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000,volume={vol},afade=t=out:st={d-(0.02 if sid=="A3" else 0.05):.3f}:d={0.02 if sid=="A3" else 0.05},apad[a]'
        cmd=['ffmpeg','-loglevel','error','-y','-ss',str(a),'-t',str(d*sp+0.05),'-i',src(n),'-filter_complex',fc,'-map','[v]','-map','[a]','-t',str(d)]+ENC+[out]
    else:
        n,a,vol=args
        fc=f'[0:v]{full(src(n))}[v];[0:a]{AFMT},volume={vol},apad[a]'
        cmd=['ffmpeg','-loglevel','error','-y','-ss',str(a),'-t',str(d),'-i',src(n),'-filter_complex',fc,'-map','[v]','-map','[a]','-t',str(d)]+ENC+[out]
    run(cmd); segs.append(out)
    real=float(subprocess.run(['ffprobe','-v','error','-select_streams','v','-show_entries','stream=duration','-of','csv=p=0',out],capture_output=True,text=True).stdout)
    t+=real
total=t
open('v12/list.txt','w').write(''.join(f"file '{os.path.abspath(p)}'\n" for p in segs))
run(['ffmpeg','-loglevel','error','-y','-f','concat','-safe','0','-i','v12/list.txt','-c:v','copy','-af','aresample=async=1:first_pts=0','-c:a','aac','-b:a','192k','v12/base.mp4'])
# overlays
st=starts
ovs=[('p1.png',st['H2'],st['H2']+0.45),('p2.png',st['H2']+0.45,st['H2']+0.93),('p3.png',st['H2']+0.93,st['O1']),
     ('bar.png',st['O1'],st['V1']),('l_station.png',st['O1'],st['O2']),
     ('p20k.png',st['I4']+0.1,st['R1']),('c_entrance.png',st['E1'],st['A1']),('c_floors.png',st['A3'],st['I2']),
     ('v1.png',st['V1']+1.1,total),('v2.png',st['V1']+2.0,total)]
inputs=['-i','v12/base.mp4']; fc='[0:v]null[v0];'; last='v0'
for i,(png,a,b) in enumerate(ovs):
    inputs+=['-i',O+png]; fc+=f"[{last}][{i+1}:v]overlay=enable='between(t,{a:.3f},{b-0.001:.3f})'[v{i+1}];"; last=f'v{i+1}'
# narration from per-line TTS files + series sting
nar=[(st[sid],key) for sid,kind,args,d,key in S if key]
k=len(ovs)+1
for t0,key in nar: inputs+=['-i',f'v11/vo/{key}.wav']
inputs+=['-i','gd/sting.mp3']
for j,(t0,key) in enumerate(nar):
    ms=int(t0*1000+(250 if key=='verdict' else 80))
    fc+=f'[{k+j}:a]aformat=channel_layouts=stereo,loudnorm=I=-15:TP=-1.5,adelay={ms}|{ms}[d{j}];'
sj=k+len(nar); hs=int(st['H2']*1000)
fc+=f'[{sj}:a]aresample=48000,aformat=channel_layouts=stereo,loudnorm=I=-14:TP=-1.5,afade=t=out:st=1.95:d=0.4,adelay={hs}|{hs}[sting];'
fc+=''.join(f'[d{j}]' for j in range(len(nar)))+f'[sting]amix=inputs={len(nar)+1}:normalize=0[nar];[0:a][nar]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.95[a]'
run(['ffmpeg','-loglevel','error','-y']+inputs+['-filter_complex',fc,'-map',f'[{last}]','-map','[a]','-c:v','libx264','-preset','medium','-crf','19','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart','v12/base_v12.mp4'])
print('TOTAL',round(total,2)); print({k:round(v,2) for k,v in starts.items()})
