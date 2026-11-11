# usage: mix.py <video_in(no audio needed)> <audio_src> <out.mp4>
import sys,subprocess
vin,asrc,out=sys.argv[1:4]
SFX='/home/user/real-or-hype/.claude/skills/real-or-hype-video/sfx/'
# (file, peak offset s, peak dBFS, role gain dB)
K={'whoosh':('whoosh_es.wav',0.454,0.0,-13),'pop':('pop_es.wav',0.005,-0.2,-11),'ding':('ding.wav',0.009,0.0,-12)}
EV=[('whoosh',t) for t in (7.10,11.00,15.20,16.95,27.85,29.30,31.20)] + \
   [('pop',t) for t in (8.32,12.18,16.26,25.04,37.30,43.38)] + [('ding',35.26)]
cmd=['ffmpeg','-nostdin','-loglevel','error','-y','-i',vin,'-i',asrc]
fl=[]; labels=[]
for i,(k,t) in enumerate(EV):
    f,pk,db,g=K[k]; cmd+=['-i',SFX+f]
    start=max(0,t-pk); gain=g-db
    fl.append(f'[{i+2}:a]aformat=sample_rates=48000:channel_layouts=stereo,volume={gain}dB,adelay={int(start*1000)}|{int(start*1000)}[s{i}]'); labels.append(f'[s{i}]')
fl.append('[1:a]aformat=sample_rates=48000:channel_layouts=stereo[v]')
fl.append('[v]'+''.join(labels)+f'amix=inputs={len(labels)+1}:normalize=0:duration=first[m]')
fl.append('[m]loudnorm=I=-15:TP=-2:LRA=11,alimiter=limit=0.79:level=false,aresample=48000[ao]')
cmd+=['-filter_complex',';'.join(fl),'-map','0:v:0','-map','[ao]','-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart','-shortest',out]
subprocess.run(cmd,check=True); print('mixed',out)
