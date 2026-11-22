# Render the China version: original sink opener (0-4.2 s) + 19 montage shots on the original reel's cut times.
import subprocess, sys, os
W=sys.argv[1]; os.chdir(W); os.makedirs('seg',exist_ok=True)
B=[4.2,4.6,5.0667,5.5667,5.8667,6.2,6.4667,6.9,7.4667,7.7333,8.1,8.4,8.8333,9.3,9.6667,10.0333,10.2667,10.7333,11.2333,11.9]
ID={1:'7214379965003959584',2:'7448413329086811446',3:'7507589178009095478',4:'7544633059090402570',5:'7582457236531907897',
6:'7598481496160946597',7:'7613419947418487163',8:'7623264801070450938',10:'7639307580749851513',11:'7651933270904877563',
12:'7656406813604445691',13:'7657737264316175973',14:'7667122568068296421',15:'7693041483927135305',16:'7703271594554247334',
17:'7706182348165685455',18:'7708715520551636328'}
HLG={3,17}
# (clip, start s, crop fraction (x,y,w,h) before cover-scale, x-bias for wide sources 0..1)
SH=[(12,12.0,None,.5),(11,2.1,None,.5),(1,7.0,(.05,.21,.9,.74),.5),(6,12.5,None,.5),(10,14.9,None,.5),(7,8.0,None,.5),
(15,4.6,None,.5),(5,10.5,None,.5),(13,1.4,(0,0,1,.88),.5),(18,4.5,(0,0,1,.79),.5),(14,16.5,None,.5),(17,4.5,None,.5),
(3,25.3,None,.5),(8,4.4,None,.5),(4,5.0,None,.5),(16,3.4,None,.5),(13,7.1,None,.5),(10,6.8,None,.5),(2,6.9,None,.45)]
assert len(SH)==len(B)-1
TM="zscale=tin=arib-std-b67:min=bt2020nc:pin=bt2020:t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p,"
def run(a): subprocess.run(a,check=True)
fr=lambda t: round(t*30)
lst=[]
# opener: the original reel's first 4.2 s (sink.src.mp4), its caption blurred out and replaced (cap2.png/mask2.png from caption2.py)
n0=fr(B[0])
run(['ffmpeg','-v','error','-y','-i','sink.src.mp4','-i','mask2.png','-i','cap2.png','-filter_complex',
 f'[0:v]fps=30,scale=1080:1920:flags=lanczos,setsar=1,split[a][b];[b]gblur=sigma=28[bl];[bl][1:v]alphamerge[blm];[a][blm]overlay[c];[c][2:v]overlay,format=yuv420p,trim=end_frame={n0}',
 '-an','-c:v','libx264','-crf','16','-preset','medium','seg/00.mp4'])
lst.append('seg/00.mp4')
for i,(c,ss,cr,xb) in enumerate(SH,1):
    nf=fr(B[i])-fr(B[i-1]); f=f'broll/{ID[c]}.mp4'
    vf=TM if c in HLG else ''
    if cr: vf+=f'crop=iw*{cr[2]}:ih*{cr[3]}:iw*{cr[0]}:ih*{cr[1]},'
    EX={10:'delogo=x=328:y=1604:w=108:h=108,'}.get(i,'')
    vf+=f'scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920:(iw-1080)*{xb}:(ih-1920)/2,setsar=1,{EX}fps=30,format=yuv420p,trim=end_frame={nf}'
    o=f'seg/{i:02d}.mp4'
    run(['ffmpeg','-v','error','-y','-ss',str(ss),'-i',f,'-vf',vf,'-an','-c:v','libx264','-crf','16','-preset','medium',o]); lst.append(o)
open('concat.txt','w').write(''.join(f"file '{x}'\n" for x in lst))
run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i','concat.txt','-c','copy','china_silent_1080.mp4'])
