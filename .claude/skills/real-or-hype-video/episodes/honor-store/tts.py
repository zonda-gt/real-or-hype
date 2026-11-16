# generate each line with the creator's clone, trim, atempo, whisper-check; up to 3 takes
import json,subprocess,os,sys,re,time,urllib.request,numpy as np
from faster_whisper import WhisperModel
KEY=os.environ['ELEVENLABS_API_KEY']; VID='KdPzirZUC0HY6WhfwyeE'
VS={"stability":0.45,"similarity_boost":0.9,"style":0.3,"use_speaker_boost":True}
L=json.load(open('lines.json')); only=sys.argv[1:] or list(L)
m=WhisperModel("small",compute_type="int8")
norm=lambda s:re.sub(r'[^a-z0-9 ]','',s.lower().replace('-',' ')).split()
def tts(text,out):
    body=json.dumps({"text":text,"model_id":"eleven_multilingual_v2","voice_settings":VS}).encode()
    for i in range(4):
        try:
            r=urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{VID}?output_format=mp3_44100_128",data=body,headers={"xi-api-key":KEY,"Content-Type":"application/json"})
            open(out,'wb').write(urllib.request.urlopen(r,timeout=120).read()); return
        except Exception as e: print('retry',e); time.sleep(3)
    raise SystemExit('tts failed')
for k in only:
    text=L[k]; best=None
    for take in range(3):
        raw=f'vo/{k}_raw{take}.mp3'; tts(text,raw)
        out=f'vo/{k}_t{take}.wav'
        subprocess.run(['ffmpeg','-v','error','-y','-i',raw,'-af','silenceremove=start_periods=1:start_threshold=-55dB:start_silence=0.03,areverse,silenceremove=start_periods=1:start_threshold=-55dB:start_silence=0.08,areverse,atempo=1.2,aresample=48000','-ac','1',out],check=True)
        a=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',out,'-ac','1','-ar','16000','-f','f32le','-'],capture_output=True).stdout,np.float32)
        hyp=' '.join(s.text for s in m.transcribe(a,language='en')[0])
        h,t=norm(hyp),norm(text); ok=h==t
        d=len(a)/16000; print(k,take,f'{d:.2f}s','OK' if ok else 'MISMATCH',hyp,flush=True)
        if ok: best=out; break
        if best is None: best=out
    os.replace(best,f'vo/{k}.wav')
