# cut_aroll.py <src.mp4> <cuts.json> <outdir>: per-segment accurate cuts (30 fps, light grade, 12 ms audio fades),
# audio padded/trimmed to each segment's video length, joined + processed voice.wav, timeline.json with exact starts.
import sys,json,subprocess,os
src,cf,E=sys.argv[1:4]; os.makedirs(E+'/seg',exist_ok=True)
def dur(f,s): return float(subprocess.run(['ffprobe','-v','error','-select_streams',s,'-show_entries','stream=duration','-of','csv=p=0',f],capture_output=True,text=True).stdout)
t=0;tl=[];al=[]
for k,s,e,txt in json.load(open(cf)):
    d=round(e-s,3); mov=f'{E}/seg/{k}.mov'
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(s),'-i',src,'-t',str(d),'-vf','fps=30,scale=1080:1920,eq=contrast=1.06:saturation=1.04:gamma=0.98,colorbalance=rm=0.02:bm=-0.02',
      '-af',f'afade=t=in:d=0.012,afade=t=out:st={d-0.012:.3f}:d=0.012','-ar','48000','-ac','1','-c:v','libx264','-crf','15','-preset','fast','-pix_fmt','yuv420p','-c:a','pcm_s16le',mov],check=True)
    vd=dur(mov,'v'); subprocess.run(['ffmpeg','-v','error','-y','-i',mov,'-map','0:a','-af',f'apad,atrim=end={vd}',f'{E}/seg/{k}.wav'],check=True)
    subprocess.run(['ffmpeg','-v','error','-y','-i',mov,'-an','-c','copy',f'{E}/seg/{k}.mp4'],check=True)
    tl.append({"k":k,"src_in":s,"src_out":e,"start":round(t,4),"dur":round(vd,4),"text":txt}); t+=vd; al.append(f"file '{E}/seg/{k}.wav'")
open(f'{E}/seg/alist.txt','w').write('\n'.join(al))
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',f'{E}/seg/alist.txt','-c','copy',f'{E}/voice_raw.wav'],check=True)
subprocess.run(['ffmpeg','-v','error','-y','-i',f'{E}/voice_raw.wav','-af',f'highpass=f=80,afftdn=nf=-40,atrim=start=0.025,asetpts=PTS-STARTPTS,apad,atrim=end={t},acompressor=threshold=-22dB:ratio=3:attack=5:release=120,loudnorm=I=-15:TP=-1.5:LRA=7','-ar','48000',f'{E}/voice.wav'],check=True)
json.dump(tl,open(f'{E}/timeline.json','w'),indent=1); print('total',round(t,3),'voice',dur(f'{E}/voice.wav','a'))
