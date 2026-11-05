# Hook auditions: viral clip with its own sound up for the first 1.5 s, then the VO line (clip ducked), then the sting.
# Usage: ep2_hook_audition.py <workdir> <vo.wav> <out.mp4>
import subprocess,os,sys
os.chdir(sys.argv[1]); vo,out=sys.argv[2],sys.argv[3]; O='ov/'
REACTV='scale=1080:1920,fps=30,setsar=1'; AFMT='aresample=48000,aformat=channel_layouts=stereo'
ENC=['-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar','48000','-ac','2']
d=5.3; UP=1.5
fc=(f'[0:v]{REACTV}[bg];[1:v]setpts=PTS/1.3,scale=594:1056,fps=30,format=rgba[c0];[2:v]format=gray[m];[c0][m]alphamerge[c1];'
    f'[bg][c1]overlay=54:634[v1];[v1][3:v]overlay[v2];[v2][4:v]overlay[hv];'
    f"[1:a]{AFMT},atempo=1.3,volume='if(lt(t,{UP-0.2}),0.75,if(lt(t,{UP}),0.75-(t-{UP-0.2})/0.2*0.53,0.22))':eval=frame,afade=t=out:st={d-0.5}:d=0.5[m];"
    f'[5:a]{AFMT},loudnorm=I=-14:TP=-1.5,adelay={int(UP*1000)}|{int(UP*1000)},apad[t];[m][t]amix=inputs=2:normalize=0:duration=first,atrim=0:{d}[ha];'
    f"[6:v]{REACTV},trim=duration=2,setpts=PTS-STARTPTS[r];[r][7:v]overlay=enable='between(t,0,0.449)'[a1];[a1][8:v]overlay=enable='between(t,0.45,0.929)'[a2];[a2][9:v]overlay=enable='gte(t,0.93)'[pv];"
    f'[10:a]{AFMT},loudnorm=I=-14:TP=-1.5,afade=t=out:st=1.95:d=0.05,atrim=0:2[pa];'
    f'[hv][ha][pv][pa]concat=n=2:v=1:a=1[v][a0];[a0]alimiter=limit=0.84:level=false[a]')
cmd=['ffmpeg','-loglevel','error','-y','-ss','1.0','-t',str(d),'-i','drive/reaction.mp4','-ss','3.5','-t',str(d*1.3+0.1),'-i','ref/viral.mp4','-i',O+'m_card.png','-i',O+'pill.png','-i',O+'credit.png','-i',vo,
     '-ss','9.8','-t','2','-i','drive/reaction.mp4','-i',O+'p1.png','-i',O+'p2.png','-i',O+'p3.png','-i','gd/sting.mp3',
     '-filter_complex',fc,'-map','[v]','-map','[a]','-vf' if False else '-map_metadata','-1']+ENC+['-s','540x960',out]
r=subprocess.run(cmd,capture_output=True,text=True)
if r.returncode: print(r.stderr[-1500:]); sys.exit(1)
print('ok',out)
