# ElevenLabs TTS (voice Liam). Usage: eltts.py <keyfile> <text> <out.mp3> [speed]
import sys,json,urllib.request
key=open(sys.argv[1]).read().strip(); text,out=sys.argv[2],sys.argv[3]; speed=float(sys.argv[4]) if len(sys.argv)>4 else 1.0
VOICE='TX3LPaxmHKxFdv7VOQHJ'   # Liam (premade)
body=json.dumps({"text":text,"model_id":"eleven_multilingual_v2",
  "voice_settings":{"stability":0.45,"similarity_boost":0.8,"style":0.25,"use_speaker_boost":True,"speed":speed}}).encode()
req=urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}?output_format=mp3_44100_128",data=body,
  headers={"xi-api-key":key,"Content-Type":"application/json","Accept":"audio/mpeg"})
try: open(out,'wb').write(urllib.request.urlopen(req,timeout=120).read())
except urllib.error.HTTPError as e: print(e.code,e.read()[:300]); sys.exit(1)
