import sys,json,urllib.request
key=open(sys.argv[1]).read().strip(); vid,text,out=sys.argv[2],sys.argv[3],sys.argv[4]; vs=json.loads(sys.argv[5])
body=json.dumps({"text":text,"model_id":(sys.argv[6] if len(sys.argv)>6 else "eleven_multilingual_v2"),"voice_settings":vs}).encode()
req=urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{vid}?output_format=mp3_44100_128",data=body,headers={"xi-api-key":key,"Content-Type":"application/json"})
try: open(out,'wb').write(urllib.request.urlopen(req,timeout=120).read())
except urllib.error.HTTPError as e: print('ERR',e.code,e.read()[:300]); sys.exit(1)
