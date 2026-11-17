import sys,subprocess,numpy as np,json
from faster_whisper import WhisperModel
m=WhisperModel("small",device="cpu",compute_type="int8")
for f in sys.argv[1:]:
    a=np.frombuffer(subprocess.run(['ffmpeg','-loglevel','error','-i',f,'-ar','16000','-ac','1','-f','f32le','-'],capture_output=True).stdout,dtype=np.float32)
    segs,_=m.transcribe(a,language='en',word_timestamps=True,beam_size=5,vad_filter=False)
    out=[]
    print('##',f)
    for s in segs:
        print(f'[{s.start:6.2f}-{s.end:6.2f}] {s.text.strip()}')
        out.append({'s':s.start,'e':s.end,'t':s.text,'w':[(w.start,w.end,w.word) for w in s.words]})
    json.dump(out,open(f+'.json','w'))
