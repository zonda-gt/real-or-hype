# Shared ElevenLabs TTS helper. Lively preset = stability 0.3, similarity 0.75, style 0.55, speaker boost, multilingual v2.
# Output format must be mp3_44100_128 (192 needs a higher tier). Library voices work by id without adding them to the account.
import json,os,urllib.request,time
LIVELY={"stability":0.3,"similarity_boost":0.75,"style":0.55,"use_speaker_boost":True}
def tts(voice_id,text,out,settings=LIVELY,model="eleven_multilingual_v2"):
    body=json.dumps({"text":text,"model_id":model,"voice_settings":settings}).encode()
    for t in range(3):   # one request at a time; parallel requests fail
        try:
            req=urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}?output_format=mp3_44100_128",data=body,headers={"xi-api-key":os.environ['ELEVENLABS_API_KEY'],"Content-Type":"application/json"})
            open(out,'wb').write(urllib.request.urlopen(req,timeout=180).read()); return True
        except urllib.error.HTTPError as e: print('ERR',e.code,e.read()[:200]); time.sleep(2)
    return False
