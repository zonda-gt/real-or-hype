import sys,json,os,urllib.request
vid,out,model=sys.argv[1],sys.argv[2],sys.argv[3]; text=open('script.txt').read().strip()
vs={"stability":0.3,"similarity_boost":0.75,"style":0.55,"use_speaker_boost":True}
if model=='eleven_v3': vs={"stability":0.5,"similarity_boost":0.75,"style":0.0,"use_speaker_boost":True}
if len(sys.argv)>4: text=text.replace('Huzhou',sys.argv[4])
body=json.dumps({"text":text,"model_id":model,"voice_settings":vs}).encode()
req=urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{vid}?output_format=mp3_44100_128",data=body,headers={"xi-api-key":os.environ['ELEVENLABS_API_KEY'],"Content-Type":"application/json"})
try: open(out,'wb').write(urllib.request.urlopen(req,timeout=180).read()); print('ok',out)
except urllib.error.HTTPError as e: print('ERR',out,e.code,e.read()[:300])
