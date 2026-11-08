"""ElevenLabs TTS with timestamps. usage: el.py <voice_id> "<text>" out.mp3 [stability] [style]
writes out.mp3 and out.json (character alignment). Key from env only."""
import os,sys,json,base64,time,requests
vid,text,out=sys.argv[1],sys.argv[2],sys.argv[3]
stab=float(sys.argv[4]) if len(sys.argv)>4 else 0.45; style=float(sys.argv[5]) if len(sys.argv)>5 else 0.3
body={"text":text,"model_id":"eleven_multilingual_v2","voice_settings":{"stability":stab,"similarity_boost":0.75,"style":style,"use_speaker_boost":True}}
for i in range(4):
    r=requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{vid}/with-timestamps?output_format=mp3_44100_128",json=body,headers={"xi-api-key":os.environ['ELEVENLABS_API_KEY']},timeout=180)
    if r.status_code==200: break
    print('ERR',r.status_code,r.text[:200]); time.sleep(3*(i+1))
r.raise_for_status(); j=r.json()
open(out,'wb').write(base64.b64decode(j['audio_base64']))
json.dump({'text':text,'alignment':j.get('alignment'),'normalized':j.get('normalized_alignment')},open(out[:-4]+'.json','w'))
print('ok',out)
