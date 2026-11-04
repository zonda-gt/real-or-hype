import sys,os,subprocess,numpy as np,json
from faster_whisper import WhisperModel
os.chdir(sys.argv[1]); m=WhisperModel("small",device="cpu",compute_type="int8")
out={}
for spec in sys.argv[2:]:
    n,lang=spec.split(':')
    f='prev/'+n+'.mp4'
    a=np.frombuffer(subprocess.run(['ffmpeg','-loglevel','error','-i',f,'-ar','16000','-ac','1','-f','f32le','-'],capture_output=True).stdout,dtype=np.float32)
    segs,_=m.transcribe(a,language=lang,word_timestamps=True,beam_size=3)
    ws=[(round(w.start,2),round(w.end,2),w.word) for s in segs for w in s.words]
    out[n]=ws
    print('##',n); print(' '.join(f'{w[2].strip()}@{w[0]}' for w in ws),flush=True)
json.dump(out,open('words.json','w'),ensure_ascii=False)
