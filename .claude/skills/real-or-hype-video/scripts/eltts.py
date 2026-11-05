import os,sys,json,urllib.request
key=os.environ['ELEVENLABS_API_KEY'] if sys.argv[1]=='-' else open(sys.argv[1]).read().strip(); vid,text,out=sys.argv[2],sys.argv[3],sys.argv[4]; model=sys.argv[5] if len(sys.argv)>5 else 'eleven_multilingual_v2'
body=json.dumps({"text":text,"model_id":model,"voice_settings":{"stability":0.4,"similarity_boost":0.75,"style":0.35,"use_speaker_boost":True}}).encode()
req=urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{vid}?output_format=mp3_44100_128",data=body,headers={"xi-api-key":key,"Content-Type":"application/json"})
try: open(out,'wb').write(urllib.request.urlopen(req,timeout=120).read())
except urllib.error.HTTPError as e: print('ERR',e.code,e.read()[:200]); sys.exit(1)
