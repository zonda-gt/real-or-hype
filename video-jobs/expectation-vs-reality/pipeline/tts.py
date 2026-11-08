#!/usr/bin/env python3
# tts.py lines.json outdir : ElevenLabs Liam with-timestamps; one request at a time; writes <key>.wav (trimmed, atempo 1.12) and <key>.json word times (post-tempo)
import os,sys,json,base64,urllib.request,subprocess,time
V='TX3LPaxmHKxFdv7VOQHJ'; TEMPO=float(os.environ.get('TEMPO','1.12'))
lines=json.load(open(sys.argv[1])); out=sys.argv[2]; os.makedirs(out,exist_ok=True)
for key,text in lines.items():
    wav=f'{out}/{key}.wav'
    if os.path.exists(wav) and json.load(open(f'{out}/{key}.json')).get('text')==text: continue
    body=json.dumps({"text":text,"model_id":"eleven_multilingual_v2","voice_settings":{"stability":0.4,"similarity_boost":0.75,"style":0.35,"use_speaker_boost":True}}).encode()
    for k in range(4):
        try:
            req=urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{V}/with-timestamps?output_format=mp3_44100_128",data=body,headers={"xi-api-key":os.environ['ELEVENLABS_API_KEY'],"Content-Type":"application/json"})
            d=json.load(urllib.request.urlopen(req,timeout=120)); break
        except urllib.error.HTTPError as e: print('ERR',e.code,e.read()[:200]); time.sleep(3)
    open(f'{out}/{key}.raw.mp3','wb').write(base64.b64decode(d['audio_base64']))
    al=d['alignment']; ch=al['characters']; st=al['character_start_times_seconds']; en=al['character_end_times_seconds']
    # words
    words=[];cur='';ws=None
    for c,a,b in zip(ch,st,en):
        if c.isspace():
            if cur: words.append((cur,ws,pe)); cur=''
        else:
            if not cur: ws=a
            cur+=c; pe=b
    if cur: words.append((cur,ws,pe))
    # trim front: first char start; keep 0.03 lead
    t0=max(0,words[0][1]-0.03); t1=words[-1][2]+0.08
    subprocess.run(['ffmpeg','-v','error','-y','-ss',f'{t0:.3f}','-to',f'{t1:.3f}','-i',f'{out}/{key}.raw.mp3','-af',f'atempo={TEMPO},aresample=48000','-ac','1',wav],check=True)
    W=[{'w':w,'s':(a-t0)/TEMPO,'e':(b-t0)/TEMPO} for w,a,b in words]
    dur=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',wav],capture_output=True,text=True).stdout)
    json.dump({'text':text,'words':W,'dur':dur},open(f'{out}/{key}.json','w'),indent=0)
    print(key,f'{dur:.2f}s',text)
