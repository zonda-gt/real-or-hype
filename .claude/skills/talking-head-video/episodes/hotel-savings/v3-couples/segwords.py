# words.json by transcribing each timeline segment of voice.wav on its own (full-track Whisper skipped a whole stretch)
import sys,json,subprocess,numpy as np
from faster_whisper import WhisperModel
E=sys.argv[1]; m=WhisperModel("medium",device="cpu",compute_type="int8")
a=np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",f"{E}/voice.wav","-f","f32le","-ac","1","-ar","16000","-"],capture_output=True).stdout,np.float32)
out=[]
for s in json.load(open(f"{E}/timeline.json")):
    x=a[int(s['start']*16000):int((s['start']+s['dur'])*16000)]
    ws=[(round(s['start']+w.start,3),round(s['start']+w.end,3),w.word.strip()) for g in m.transcribe(x,language='en',beam_size=5,word_timestamps=True,initial_prompt=s['text'],condition_on_previous_text=False)[0] for w in g.words]
    print(s['k'],' '.join(w for _,_,w in ws)); out+=ws
json.dump(out,open(f"{E}/words.json","w"))
print(len(out),'words'); print(' '.join(f'{i}:{w[2]}@{w[0]:.2f}' for i,w in enumerate(out)))
