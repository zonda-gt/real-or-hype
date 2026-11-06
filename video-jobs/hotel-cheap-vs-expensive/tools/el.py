import json,os,sys,base64,urllib.request
vid="TX3LPaxmHKxFdv7VOQHJ"
name,text=sys.argv[1],sys.argv[2]
body={"text":text,"model_id":"eleven_multilingual_v2","voice_settings":{"stability":0.45,"similarity_boost":0.8,"style":0.3,"use_speaker_boost":True}}
req=urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{vid}/with-timestamps",data=json.dumps(body).encode(),headers={"xi-api-key":os.environ["ELEVENLABS_API_KEY"],"Content-Type":"application/json"})
d=json.load(urllib.request.urlopen(req,timeout=180))
open(f"work/vo/{name}.mp3","wb").write(base64.b64decode(d["audio_base64"]))
al=d.get("alignment") or d.get("normalized_alignment")
ch,st,en=al["characters"],al["character_start_times_seconds"],al["character_end_times_seconds"]
words=[];cur="";s=None
for c,a,b in zip(ch,st,en):
    if c.isspace():
        if cur: words.append({"w":cur,"s":s,"e":pe}); cur=""
        continue
    if not cur: s=a
    cur+=c; pe=b
if cur: words.append({"w":cur,"s":s,"e":pe})
json.dump({"text":text,"chars":len(text),"words":words},open(f"work/vo/{name}.json","w"),indent=1)
print(name,len(text),"chars", f"{words[-1]['e']:.2f}s", " ".join(f"{w['w']}@{w['s']:.2f}" for w in words))
