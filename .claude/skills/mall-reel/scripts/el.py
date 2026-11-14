# usage: el.py voice_id model out_prefix 'settings_json' "text" [prev_text] [next_text]
import sys,os,json,base64,urllib.request,time
vid,model,out,vs,text=sys.argv[1:6]
body={"text":text,"model_id":model,"voice_settings":json.loads(vs)}
if len(sys.argv)>6 and sys.argv[6]: body["previous_text"]=sys.argv[6]
if len(sys.argv)>7 and sys.argv[7]: body["next_text"]=sys.argv[7]
if model=='eleven_v3': body.pop("previous_text",None); body.pop("next_text",None)
req=urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{vid}/with-timestamps?output_format=mp3_44100_128",data=json.dumps(body).encode(),headers={"xi-api-key":os.environ['ELEVENLABS_API_KEY'],"Content-Type":"application/json"})
for k in range(3):
    try:
        d=json.load(urllib.request.urlopen(req,timeout=180)); break
    except urllib.error.HTTPError as e:
        msg=e.read()[:300]; print('ERR',e.code,msg)
        if e.code in (400,401,403,404,422): sys.exit(1)
        time.sleep(5)
else: sys.exit(1)
open(out+'.mp3','wb').write(base64.b64decode(d['audio_base64']))
json.dump(d.get('alignment') or d.get('normalized_alignment'),open(out+'.align.json','w'))
print('ok',out)
