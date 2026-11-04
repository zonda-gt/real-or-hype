# Hook (5.3 s) + sung sting punch (2.0 s) for episode 2. Usage: ep2_opening.py <workdir>
import subprocess,os,sys
os.chdir(sys.argv[1]); O='ov/'
REACT='drive/reaction.mp4'; HER='ref/viral.mp4'
REACTV='scale=1080:1920,fps=30,setsar=1'; AFMT='aresample=48000,aformat=channel_layouts=stereo'
ENC=['-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-c:a','aac','-b:a','192k','-ar','48000','-ac','2']
def run(cmd):
    r=subprocess.run(cmd,capture_output=True,text=True)
    if r.returncode: print(r.stderr[-1500:]); sys.exit(1)
HOOK_IN,HOOK_D=1.0,5.3          # his deadpan, arms crossed
VIRAL_IN,VIRAL_SP=3.5,1.3       # claim text -> turns with coffee -> walks out -> skyline reveal at ~4.2 s
PUNCH_IN,PUNCH_D=9.8,2.0        # he leans into the camera on "real"
d=HOOK_D
fc=(f'[0:v]{REACTV}[bg];[1:v]setpts=PTS/{VIRAL_SP},scale=594:1056,fps=30,format=rgba[c0];[2:v]format=gray[m];[c0][m]alphamerge[c1];'
    f'[bg][c1]overlay=54:634[v1];[v1][3:v]overlay[v2];[v2][4:v]overlay[v];'
    f'[1:a]{AFMT},atempo={VIRAL_SP},volume=0.22,afade=t=out:st={d-0.5}:d=0.5[m];[5:a]{AFMT},loudnorm=I=-14:TP=-1.5,adelay=200|200,apad[t];[m][t]amix=inputs=2:normalize=0:duration=first[a]')
run(['ffmpeg','-loglevel','error','-y','-ss',str(HOOK_IN),'-t',str(d),'-i',REACT,'-ss',str(VIRAL_IN),'-t',str(d*VIRAL_SP+0.1),'-i',HER,'-i',O+'m_card.png','-i',O+'pill.png','-i',O+'credit.png','-i','vo/hook.wav',
     '-filter_complex',fc,'-map','[v]','-map','[a]','-t',str(d)]+ENC+['seg/H1.mp4'])
# punch: his lean-in + sung sting, captions 2 frames before each sung onset (Is 0.01, real 0.51, or 0.99)
d=PUNCH_D
fc=(f'[0:v]{REACTV}[r];[r][2:v]overlay=enable=\'between(t,0,0.449)\'[a1];[a1][3:v]overlay=enable=\'between(t,0.45,0.929)\'[a2];[a2][4:v]overlay=enable=\'gte(t,0.93)\'[v];'
    f'[1:a]{AFMT},loudnorm=I=-14:TP=-1.5,afade=t=out:st=1.95:d=0.05,apad[a]')
run(['ffmpeg','-loglevel','error','-y','-ss',str(PUNCH_IN),'-t',str(d),'-i',REACT,'-i','gd/sting.mp3','-i',O+'p1.png','-i',O+'p2.png','-i',O+'p3.png',
     '-filter_complex',fc,'-map','[v]','-map','[a]','-t',str(d)]+ENC+['seg/H2.mp4'])
open('seg/open.txt','w').write("file 'H1.mp4'\nfile 'H2.mp4'\n")
run(['ffmpeg','-loglevel','error','-y','-f','concat','-safe','0','-i','seg/open.txt','-c:v','copy','-af','aresample=async=1:first_pts=0,alimiter=limit=0.84:level=false','-c:a','aac','-b:a','192k','-movflags','+faststart','opening.mp4'])
print('ok')
