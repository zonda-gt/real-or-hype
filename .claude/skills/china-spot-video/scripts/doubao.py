# Doubao (Volcano Engine) TTS with a cloned voice (声音复刻 2.0), HTTP v3 streaming endpoint.
# Key: env DOUBAO_TTS_KEY (an API key from the Volcano speech console; never commit it).
# Voice: the clone's speaker ID, e.g. S_hgDXnnfk2. speech_rate: -50..100 (0 = normal).
import base64,json,os,time,urllib.request
URL="https://openspeech.bytedance.com/api/v3/tts/unidirectional"
def tts(speaker,text,out,speech_rate=0,resource="seed-icl-2.0"):
    body=json.dumps({"user":{"uid":"chinapal"},"req_params":{"text":text,"speaker":speaker,
        "audio_params":{"format":"mp3","sample_rate":24000,"speech_rate":speech_rate}}}).encode()
    for t in range(3):   # one request at a time
        try:
            req=urllib.request.Request(URL,data=body,headers={"X-Api-Key":os.environ["DOUBAO_TTS_KEY"],"X-Api-Resource-Id":resource,"Content-Type":"application/json"})
            audio=b"";last=None
            for line in urllib.request.urlopen(req,timeout=180).read().decode().splitlines():
                if not line.strip(): continue
                j=json.loads(line); last=j
                if j.get("data"): audio+=base64.b64decode(j["data"])
                if j.get("code") not in (0,20000000,None): raise RuntimeError(j)
            if not audio: raise RuntimeError(last)
            open(out,"wb").write(audio); return True
        except Exception as e: print("ERR",str(e)[:200]); time.sleep(2)
    return False
