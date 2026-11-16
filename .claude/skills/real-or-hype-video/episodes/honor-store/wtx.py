import sys,subprocess,json,numpy as np,glob,os
from faster_whisper import WhisperModel
m=WhisperModel("medium",compute_type="int8")
out={}
for f in sorted(glob.glob('src/*.mp4')):
    n=os.path.basename(f)[:-4]
    raw=subprocess.run(["ffmpeg","-v","error","-i",f,"-ac","1","-ar","16000","-f","s16le","-"],capture_output=True).stdout
    a=np.frombuffer(raw,np.int16).astype(np.float32)/32768
    segs,_=m.transcribe(a,language="en",vad_filter=True,word_timestamps=True)
    ws=[]
    print("=====",n,flush=True)
    for s in segs:
        print(f"{s.start:6.2f}-{s.end:6.2f} {s.text}",flush=True)
        ws+=[(w.start,w.end,w.word.strip()) for w in s.words]
    out[n]=ws
json.dump(out,open('words.json','w'))
