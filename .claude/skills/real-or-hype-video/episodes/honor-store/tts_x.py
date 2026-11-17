# Old clone (v2 voice) on eleven_v3 with emotion tags: 3 takes/line, keep the most expressive take that passes Whisper.
import json,subprocess,os,sys,re,time,urllib.request,difflib,numpy as np
from faster_whisper import WhisperModel
from f0 import stats
KEY=os.environ['ELEVENLABS_API_KEY']; VID='KdPzirZUC0HY6WhfwyeE'; OD='vox'; os.makedirs(OD,exist_ok=True)
VS={"stability":0.5,"similarity_boost":0.85}
TAG={
 'a1':"[excited] Honor made a phone with a robot camera, and of course I had to try it!",
 'a2':"If you don't know Honor, it's one of China's biggest phone brands.",
 'a3':"[amazed] The camera pops out on a tiny robot arm, and it moves on its own!",
 'a4':"[impressed] It's about fourteen hundred dollars.",
 'a5':"[excited] And let me tell you right now, that's not even the craziest thing in here!",
 'a6':"They have a telescope lens for your phone! You can zoom across the whole building.",
 'a7':"And this is a cat massage gun. [laughs] It literally punches you in the face!",
 'a8':"[amused] Honestly? It felt kind of nice.",
 'a9':"[excited] Hit that follow button for more cool stuff in China!",
 'b1':"[excited] These are the three craziest things I found in a phone store in China!",
 'b2':"Number three: a cat massage gun.",
 'b3':"[laughs] It punches you in the face with its little paws, and I don't hate it!",
 'b4':"Number two: a telescope lens for your phone.",
 'b5':"Clip it on, and you can zoom across the whole building!",
 'b6':"[excited] And number one: the Honor Robot Phone!",
 'b8':"It's about fourteen hundred dollars. [amused] Honestly? I'd get one.",
 'b9':"[excited] Hit that follow button, because I'm showing you more things to do in China!",
}
L=json.load(open('lines.json'))
if os.path.exists('tags_c.json'): TAG.update(json.load(open('tags_c.json')))
NUM={'1400':'fourteen hundred','1,400':'fourteen hundred','3':'three','2':'two','1':'one'}
def norm(s):
    s=s.lower().replace('$','').replace('-',' ')
    for k,v in NUM.items(): s=re.sub(rf'\b{re.escape(k)}\b',v,s)
    return re.sub(r"[^a-z' ]",' ',s).split()
m=WhisperModel("small",compute_type="int8")
def tts(text,out):
    body=json.dumps({"text":text,"model_id":"eleven_v3","voice_settings":VS}).encode()
    for i in range(4):
        try:
            r=urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{VID}?output_format=mp3_44100_128",data=body,headers={"xi-api-key":KEY,"Content-Type":"application/json"})
            open(out,'wb').write(urllib.request.urlopen(r,timeout=180).read()); return
        except Exception as e: print('retry',e); time.sleep(4)
    raise SystemExit('tts failed')
for k in (sys.argv[1:] or list(TAG)):
    cands=[]
    for take in range(3):
        raw=f'{OD}/{k}_raw{take}.mp3'; out=f'{OD}/{k}_t{take}.wav'; tts(TAG[k],raw)
        subprocess.run(['ffmpeg','-v','error','-y','-i',raw,'-af',
            'silenceremove=start_periods=1:start_threshold=-55dB:start_silence=0.03,'
            'silenceremove=stop_periods=-1:stop_duration=0.14:stop_threshold=-45dB:stop_silence=0.12,'
            'areverse,silenceremove=start_periods=1:start_threshold=-55dB:start_silence=0.08,areverse,atempo=1.12,aresample=48000',
            '-ac','1',out],check=True)
        a=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',out,'-ac','1','-ar','16000','-f','f32le','-'],capture_output=True).stdout,np.float32)
        hyp=' '.join(s.text for s in m.transcribe(a,language='en')[0])
        r=difflib.SequenceMatcher(None,norm(hyp),norm(L[k])).ratio(); sd,rg=stats(out); d=len(a)/16000
        print(f'{k} t{take} {d:5.2f}s range {rg:4.1f} match {r:.2f} | {hyp.strip()}',flush=True)
        cands.append((r>=0.93,rg,-d,out))
    ok=[c for c in cands if c[0]] or sorted(cands,key=lambda c:-c[1])[:1]
    best=min(ok,key=lambda c:abs(c[1]-15)+(10 if c[1]>20 else 0)); os.replace(best[3],f'{OD}/{k}.wav'); print(' ->',k,'keeps',best[3],'OK' if best[0] else 'NO PASSING TAKE',flush=True)
