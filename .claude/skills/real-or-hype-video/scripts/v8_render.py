import subprocess,os,sys
os.chdir(sys.argv[1]); V='VID_20260910_'; O='v8/ov/'
def src(n):
    for e in ('.MOV','.mp4'):
        if os.path.exists('orig/'+n+e): return 'orig/'+n+e
    raise SystemExit('missing '+n)
FULL='scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1,eq=saturation=1.08'
ENC=['-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-c:a','aac','-b:a','192k','-ar','48000','-ac','2']
def run(cmd):
    r=subprocess.run(cmd,capture_output=True,text=True)
    if r.returncode: print(r.stderr[-1500:]); sys.exit(1)
AFMT='aresample=48000,aformat=channel_layouts=stereo'
# (id, kind, args, dur, narr(a,b) or None)
S=[
 ('H1','hook',None,4.6,None),
 ('H2','react',(10.6,),1.6,None),
 ('O1','clip',('IMG_4775',8.8,0.0),2.80,'station'),
 ('O2','clip',(V+'162824_003',0.4,0.15),0.85,'bike'),
 ('O3','clip',(V+'162824_003',4.9,0.15),1.05,None),
 ('O5','panel',(V+'164346_011',0,4.4),2.55,'green'),
 ('O6','clip',(V+'173344_017',15.4,0.15),1.55,'pillar'),
 ('O7','clip',(V+'164338_010',0,0.15),1.50,None),
 ('O8','clip',(V+'173429_020',19,0.15),1.85,'close'),
 ('M1','clip',('IMG_4806',0.4,0.3),1.10,None),
 ('E1','talk',('IMG_4837',1.6,1.0,1.3),2.88,None),
 ('A1','clip',('IMG_4854',5.4,0.15),1.25,'inside'),
 ('A2','clip',(V+'173934_028',13.5,0.15),1.0,None),
 ('A3','talk',('IMG_4855',33.86,1.0,1.3),2.27,None),
 ('I2','clip',(V+'173521_022',15,0.15),2.50,'gorilla'),
 ('I3','clip',('IMG_4842',35,0.1),0.95,'thisbike'),
 ('I4','clip',('IMG_4842',51.4,0.1),1.0,None),
 ('I5','talk',('IMG_4842',57.2,1.0,1.15),1.04,None),
 ('I6','clip',(V+'173621_024',23.5,0.15),1.20,None),
 ('I11','talk',('IMG_4861',28.0,1.0,1.3),3.0,None),
 ('V1','clip',('IMG_4793',0,0.15),2.75,'verdict'),
]
REACT='v5/react.mp4'; HER='react/DdMSIVcJBwK.mp4'
REACTV='scale=1080:1920,fps=30,setsar=1'
starts={}; t=0; segs=[]
for sid,kind,args,d,narr in S:
    out=f'v8/seg/{sid}.mp4'; starts[sid]=t
    if kind=='hook':
        fc=(f'[0:v]{REACTV}[bg];[1:v]scale=594:1056,fps=30,format=rgba[c0];[2:v]format=gray[m];[c0][m]alphamerge[c1];'
            f'[bg][c1]overlay=54:634[v1];[v1][3:v]overlay[v2];[v2][4:v]overlay[v];'
            f'[1:a]{AFMT},volume=0.22,afade=t=out:st={d-0.5}:d=0.5[m];[5:a]{AFMT},loudnorm=I=-14:TP=-1.5,adelay=200|200,apad[t];[m][t]amix=inputs=2:normalize=0:duration=first[a]')
        cmd=['ffmpeg','-loglevel','error','-y','-ss','0.8','-t',str(d),'-i',REACT,'-ss','0','-t',str(d),'-i',HER,'-i',O+'m_card.png','-i',O+'pill.png','-i',O+'credit.png','-i','v8/vo/hook.wav',
             '-filter_complex',fc,'-map','[v]','-map','[a]','-t',str(d)]+ENC+[out]
    elif kind=='react':
        fc=f'[0:v]{REACTV}[v];anullsrc=r=48000:cl=stereo[a]'
        cmd=['ffmpeg','-loglevel','error','-y','-ss',str(args[0]),'-t',str(d),'-i',REACT,'-filter_complex',fc,'-map','[v]','-map','[a]','-t',str(d)]+ENC+[out]
    elif kind=='panel':
        n,a,herin=args
        fc=(f'[0:v]{FULL}[bg];[1:v]scale=760:-2,crop=760:700:0:(ih-700)/2,fps=30,format=rgba[p0];[2:v]format=gray[m];[p0][m]alphamerge[p1];'
            f'[bg][p1]overlay=160:1060[v1];[v1][3:v]overlay[v2];[v2][4:v]overlay[v];[0:a]{AFMT},volume=0.15[a]')
        cmd=['ffmpeg','-loglevel','error','-y','-ss',str(a),'-t',str(d),'-i',src(n),'-ss',str(herin),'-t',str(d),'-i',HER,'-i',O+'m_panel.png','-i',O+'l_online.png','-i',O+'l_real.png',
             '-filter_complex',fc,'-map','[v]','-map','[a]','-t',str(d)]+ENC+[out]
    elif kind=='talk':
        n,a,vol,sp=args
        fc=f'[0:v]setpts=PTS/{sp},{FULL}[v];[0:a]{AFMT},atempo={sp},volume={vol},apad[a]'
        cmd=['ffmpeg','-loglevel','error','-y','-ss',str(a),'-t',str(d*sp+0.05),'-i',src(n),'-filter_complex',fc,'-map','[v]','-map','[a]','-t',str(d)]+ENC+[out]
    else:
        n,a,vol=args
        fc=f'[0:v]{FULL}[v];[0:a]{AFMT},volume={vol},apad[a]'
        cmd=['ffmpeg','-loglevel','error','-y','-ss',str(a),'-t',str(d),'-i',src(n),'-filter_complex',fc,'-map','[v]','-map','[a]','-t',str(d)]+ENC+[out]
    run(cmd); segs.append(out)
    real=float(subprocess.run(['ffprobe','-v','error','-select_streams','v','-show_entries','stream=duration','-of','csv=p=0',out],capture_output=True,text=True).stdout)
    t+=real
total=t
open('v8/list.txt','w').write(''.join(f"file '{os.path.abspath(p)}'\n" for p in segs))
run(['ffmpeg','-loglevel','error','-y','-f','concat','-safe','0','-i','v8/list.txt','-c:v','copy','-af','aresample=async=1:first_pts=0','-c:a','aac','-b:a','192k','v8/base.mp4'])
# overlays
st=starts
ovs=[('isit.png',st['H2'],st['H2']+1.0),('isitfact.png',st['H2']+1.0,st['O1']),
     ('bar.png',st['O1'],st['V1']),('l_station.png',st['O1'],st['O2']),('l_price.png',st['I4'],st['I5']),
     ('p20k.png',st['I5'],st['I6']),('c_entrance.png',st['E1'],st['A1']),('c_floors.png',st['A3'],st['I2']),
     ('c_verdict.png',st['I11'],st['V1']),
     ('v1.png',st['V1']+1.0,total),('v2.png',st['V1']+1.9,total)]
inputs=['-i','v8/base.mp4']; fc='[0:v]null[v0];'; last='v0'
for i,(png,a,b) in enumerate(ovs):
    inputs+=['-i',O+png]; fc+=f"[{last}][{i+1}:v]overlay=enable='between(t,{a:.3f},{b-0.001:.3f})'[v{i+1}];"; last=f'v{i+1}'
# narration from per-line TTS files + series sting
nar=[(st[sid],key) for sid,kind,args,d,key in S if key]
k=len(ovs)+1
for t0,key in nar: inputs+=['-i',f'v8/vo/{key}.wav']
inputs+=['-i','v5/sting.wav']
for j,(t0,key) in enumerate(nar):
    ms=int(t0*1000+(330 if key=='verdict' else 80))
    fc+=f'[{k+j}:a]aformat=channel_layouts=stereo,loudnorm=I=-15:TP=-1.5,adelay={ms}|{ms}[d{j}];'
sj=k+len(nar); hs=int(st['H2']*1000)
fc+=f'[{sj}:a]loudnorm=I=-16:TP=-2,adelay={hs}|{hs}[sting];'
fc+=''.join(f'[d{j}]' for j in range(len(nar)))+f'[sting]amix=inputs={len(nar)+1}:normalize=0[nar];[0:a][nar]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.95[a]'
run(['ffmpeg','-loglevel','error','-y']+inputs+['-filter_complex',fc,'-map',f'[{last}]','-map','[a]','-c:v','libx264','-preset','medium','-crf','19','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart','v8/1000trees_v8.mp4'])
print('TOTAL',round(total,2)); print({k:round(v,2) for k,v in starts.items()})
