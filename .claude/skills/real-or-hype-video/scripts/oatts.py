import os,sys,json,urllib.request
voice,text,out=sys.argv[1],sys.argv[2],sys.argv[3]
instr=sys.argv[4] if len(sys.argv)>4 else ''
body=json.dumps({"model":"gpt-4o-mini-tts","voice":voice,"input":text,"instructions":instr,"response_format":"wav"}).encode()
req=urllib.request.Request("https://api.openai.com/v1/audio/speech",data=body,headers={"Authorization":"Bearer "+os.environ["OPENAI_API_KEY"],"Content-Type":"application/json"})
open(out,'wb').write(urllib.request.urlopen(req,timeout=120).read())
