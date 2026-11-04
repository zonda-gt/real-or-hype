# Episode 2 (North Bund vs the Bund) full render. Usage: ep2_render.py <workdir>
# Structure built from the footage: hook -> sting -> "Don't go to the Bund" (night crowd cutaway) -> "come to the North Bund"
# -> skyline + "zero people" -> ONLINE/REAL LIFE panel -> bars & restaurants -> mirror-egg park -> "absolute gem" -> verdict.
import subprocess,os,sys,json
os.chdir(sys.argv[1]); O='ov/'; V='VID_20260916_'
def src(n):
    for p in ('orig/'+n+'.MOV','orig/'+n+'.mp4','photos/jpg/'+n+'.jpg'):
        if os.path.exists(p): return p
    raise SystemExit('missing '+n)
FULL='scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1'
TM='zscale=tin=arib-std-b67:min=bt2020nc:pin=bt2020:t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p,'
_hdr={}
def full(p):
    if p not in _hdr:
        _hdr[p]=subprocess.run(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=color_transfer','-of','csv=p=0',p],capture_output=True,text=True).stdout.strip().startswith('arib-std-b67')
    return (TM if _hdr[p] else '')+FULL
ENC=['-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-c:a','aac','-b:a','192k','-ar','48000','-ac','2']
AFMT='aresample=48000,aformat=channel_layouts=stereo'
def run(cmd):
    r=subprocess.run(cmd,capture_output=True,text=True)
    if r.returncode: print(' '.join(cmd)[:600]); print(r.stderr[-1500:]); sys.exit(1)
def dur(p,stream='v'):
    return float(subprocess.run(['ffprobe','-v','error','-select_streams',stream,'-show_entries','stream=duration','-of','csv=p=0',p],capture_output=True,text=True).stdout)
SP=1.4
# talk: (src, a, b, speed, [(t_out, src, ss)] cutaways at 1x from t_out to the next piece / end)
# clip: (src, ss, ambient vol)   panel: (bg src, bg ss, viral ss)   photo: (name,)
S=[
 ('H1','hook',None,5.3,None),
 ('H2','react',(9.8,),2.0,None),
 ('T1','talk',('IMG_5095',6.70,10.60,SP,[(1.75,'IMG_5113',1.4)]),None,None),        # Don't go to the Bund... (X arms) -> night crowd at the 外滩 sign
 ('T2','talk',('IMG_5096',1.45,6.92,SP,[]),None,None),                                # Instead, come to this place, the North Bund...
 ('T3','talk',('IMG_5103',4.05,6.80,SP,[]),None,None),                                # look at this beautiful skyline (selfie)
 ('T4','talk',('IMG_5103',10.92,14.17,SP,[(0.0,'IMG_5098',9.6)]),None,None),         # zero people -> empty promenade
 ('P1','panel',(V+'171459_005',0.2,9.3),2.4,'same'),
 ('T5','talk',(V+'171108_002',55.00,59.65,SP,[(1.6,V+'173805_023',2.4)]),None,None), # restaurants and bars -> terrace
 ('T6','talk',(V+'171108_002',68.20,70.75,SP,[]),None,None),                          # which the real Bund doesn't have
 ('E1','clip',(V+'174403_031',0.0,0.0),1.35,'egg'),
 ('E2','clip',(V+'173900_025',3.3,0.0),1.30,None),
 ('E3','photo',('IMG_2155',V+'174323_030',2.0,0.7),1.0,None),
 ('T7','talk',(V+'172120_010',28.95,33.00,SP,[(1.3,V+'172451_013',8.6)],4.0),None,None), # absolute gem compared to the real Bund
 ('R1','clip',(V+'172008_009',44.0,0.0),2.19,'verdict'),
 ('R2','clip',('IMG_5112',1.4,0.35),2.25,None),
]
REACT='drive/reaction.mp4'; HER='ref/viral.mp4'; REACTV='scale=1080:1920,fps=30,setsar=1'
os.makedirs('seg',exist_ok=True)
starts={}; t=0; segs=[]
for sid,kind,args,d,narr in S:
    out=f'seg/{sid}.mp4'; starts[sid]=t
    if kind=='hook':
        fc=(f'[0:v]{REACTV}[bg];[1:v]setpts=PTS/1.3,scale=594:1056,fps=30,format=rgba[c0];[2:v]format=gray[m];[c0][m]alphamerge[c1];'
            f'[bg][c1]overlay=54:634[v1];[v1][3:v]overlay[v2];[v2][4:v]overlay[v];'
            f'[1:a]{AFMT},atempo=1.3,volume=0.22,afade=t=out:st={d-0.5}:d=0.5[m];[5:a]{AFMT},loudnorm=I=-14:TP=-1.5,adelay=200|200,apad[t];[m][t]amix=inputs=2:normalize=0:duration=first[a]')
        cmd=['ffmpeg','-loglevel','error','-y','-ss','1.0','-t',str(d),'-i',REACT,'-ss','3.5','-t',str(d*1.3+0.1),'-i',HER,'-i',O+'m_card.png','-i',O+'pill.png','-i',O+'credit.png','-i','vo/hook.wav',
             '-filter_complex',fc,'-map','[v]','-map','[a]','-t',str(d)]+ENC+[out]
    elif kind=='react':
        fc=f'[0:v]{REACTV}[v];anullsrc=r=48000:cl=stereo[a]'
        cmd=['ffmpeg','-loglevel','error','-y','-ss',str(args[0]),'-t',str(d),'-i',REACT,'-filter_complex',fc,'-map','[v]','-map','[a]','-t',str(d)]+ENC+[out]
    elif kind=='talk':
        n,a,b,sp,cuts=args[:5]; gain=args[5] if len(args)>5 else 0; d=round((b-a)/sp,3); f=src(n)
        pieces=[(0.0,n,a,sp)]+[(to,cn,ss,1.0) for to,cn,ss in cuts]
        if cuts and cuts[0][0]==0.0: pieces=pieces[1:]
        inputs=['-ss',str(a),'-t',str(b-a+0.1),'-i',f]; fc=''; labels=[]
        for i,(to,pn,ss,psp) in enumerate(pieces):
            end=pieces[i+1][0] if i+1<len(pieces) else d; pd=end-to
            if pn==n and psp==sp:
                vin=0; fc+=f'[0:v]trim=start={to*sp:.3f}:duration={pd*sp:.3f},setpts=(PTS-STARTPTS)/{sp},{full(f)},trim=duration={pd:.3f}[p{i}];'
            else:
                inputs+=['-ss',str(ss),'-t',str(pd+0.2),'-i',src(pn)]; k=inputs.count('-i')-1
                fc+=f'[{k}:v]{full(src(pn))},trim=duration={pd:.3f},setpts=PTS-STARTPTS[p{i}];'
            labels.append(f'[p{i}]')
        fc+=''.join(labels)+f'concat=n={len(labels)}:v=1:a=0[v];'
        fc+=f'[0:a]{AFMT},atempo={sp},highpass=f=80,loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000,volume={gain}dB,afade=t=in:d=0.03,afade=t=out:st={d-0.05:.3f}:d=0.05,apad[a]'
        cmd=['ffmpeg','-loglevel','error','-y']+inputs+['-filter_complex',fc,'-map','[v]','-map','[a]','-t',str(d)]+ENC+[out]
    elif kind=='panel':
        n,a,herin=args
        fc=(f'[0:v]{full(src(n))}[bg];[1:v]scale=760:-2,crop=760:700:0:ih*0.14,fps=30,format=rgba[p0];[2:v]format=gray[m];[p0][m]alphamerge[p1];'
            f'[bg][p1]overlay=160:1060[v1];[v1][3:v]overlay[v2];[v2][4:v]overlay[v];[0:a]{AFMT},volume=0.15[a]')
        cmd=['ffmpeg','-loglevel','error','-y','-ss',str(a),'-t',str(d),'-i',src(n),'-ss',str(herin),'-t',str(d),'-i',HER,'-i',O+'m_panel.png','-i',O+'l_online.png','-i',O+'l_real.png',
             '-filter_complex',fc,'-map','[v]','-map','[a]','-t',str(d)]+ENC+[out]
    elif kind=='photo':
        n,an,ass,avol=args; fr=int(d*30)
        fc=(f"[0:v]scale=1188:2112:force_original_aspect_ratio=increase,crop=1188:2112,setsar=1,"
            f"zoompan=z='1+0.06*on/{fr}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={fr}:s=1080x1920:fps=30,format=yuv420p[v];[1:a]{AFMT},volume={avol},apad[a]")
        cmd=['ffmpeg','-loglevel','error','-y','-i',src(n),'-ss',str(ass),'-t',str(d),'-i',src(an),'-filter_complex',fc,'-map','[v]','-map','[a]','-t',str(d)]+ENC+[out]
    else:
        n,a,vol=args
        fc=f'[0:v]{full(src(n))}[v];[0:a]{AFMT},volume={vol},apad[a]'
        cmd=['ffmpeg','-loglevel','error','-y','-ss',str(a),'-t',str(d),'-i',src(n),'-filter_complex',fc,'-map','[v]','-map','[a]','-t',str(d)]+ENC+[out]
    run(cmd); segs.append(out); t+=dur(out)
total=t
open('seg/list.txt','w').write(''.join(f"file '{os.path.abspath(p)}'\n" for p in segs))
run(['ffmpeg','-loglevel','error','-y','-f','concat','-safe','0','-i','seg/list.txt','-c:v','copy','-af','aresample=async=1:first_pts=0','-c:a','aac','-b:a','192k','seg/base.mp4'])
st=starts
# verdict word onsets in vo/verdict.wav (envelope): "The Bund" 1.99, "real" 1.30, "hype" 2.65; narration placed at R1+0.25; graphics 2 frames early
VOFF=0.25; REAL_T=st['R1']+VOFF+1.30-0.067; HYPE_T=st['R1']+VOFF+2.65-0.067
ovs=[('p1.png',st['H2'],st['H2']+0.45),('p2.png',st['H2']+0.45,st['H2']+0.93),('p3.png',st['H2']+0.93,st['T1']),
     ('bar.png',st['T1'],REAL_T),('l_bund.png',st['T1']+1.75,st['T2']),('l_north.png',st['T2']+(3.62-1.45)/SP-0.067,st['T3']),
     ('v1.png',REAL_T,total),('v2.png',HYPE_T,total)]
inputs=['-i','seg/base.mp4']; fc='[0:v]null[v0];'; last='v0'
for i,(png,a,b) in enumerate(ovs):
    inputs+=['-i',O+png]; fc+=f"[{last}][{i+1}:v]overlay=enable='between(t,{a:.3f},{b-0.001:.3f})'[v{i+1}];"; last=f'v{i+1}'
nar=[(st[sid],key) for sid,kind,args,d,key in S if key]
k=len(ovs)+1
for t0,key in nar: inputs+=['-i',f'vo/{key}.wav']
inputs+=['-i','gd/sting.mp3']
for j,(t0,key) in enumerate(nar):
    ms=int(t0*1000+(VOFF*1000 if key=='verdict' else 80))
    fc+=f'[{k+j}:a]aformat=channel_layouts=stereo,loudnorm=I=-15:TP=-1.5,aresample=48000,adelay={ms}|{ms}[d{j}];'
sj=k+len(nar); hs=int(st['H2']*1000)
fc+=f'[{sj}:a]aresample=48000,aformat=channel_layouts=stereo,loudnorm=I=-14:TP=-1.5,afade=t=out:st=1.95:d=0.4,adelay={hs}|{hs}[sting];'
fc+=''.join(f'[d{j}]' for j in range(len(nar)))+f'[sting]amix=inputs={len(nar)+1}:normalize=0[nar];[0:a][nar]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.95[a]'
run(['ffmpeg','-loglevel','error','-y']+inputs+['-filter_complex',fc,'-map',f'[{last}]','-map','[a]','-c:v','libx264','-preset','medium','-crf','19','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart','base_ep2.mp4'])
json.dump({'starts':starts,'total':total,'REAL_T':REAL_T,'HYPE_T':HYPE_T},open('seg/starts.json','w'),indent=1)
open('seg/starts.txt','w').write(repr({k:round(v,3) for k,v in starts.items()}))
print('TOTAL',round(total,2)); print({k:round(v,2) for k,v in starts.items()})
# narration overlap check (checklist #4)
for j,(t0,key) in enumerate(nar):
    a=t0+(VOFF if key=='verdict' else 0.08); e=a+dur(f'vo/{key}.wav','a')
    nxt=[s for s in starts.values() if s>t0]
    print(f'  narr {key}: {a:.2f}-{e:.2f}')
