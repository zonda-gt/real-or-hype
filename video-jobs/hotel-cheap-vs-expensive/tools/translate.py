import json,os,sys,urllib.request
for aid in sys.argv[1:]:
    d=json.load(open(f"work/tx/{aid}.json"))
    src="\n".join(f"[{s['start']:.1f}-{s['end']:.1f}] {s['text']}" for s in d["segments"])
    body={"model":"gpt-4.1-mini","messages":[{"role":"system","content":"Translate each line of this Chinese Douyin transcript into natural English. Keep the [start-end] timestamps. Whisper may mis-hear hotel names; keep the Chinese name in brackets after your English guess. Output only the lines."},{"role":"user","content":src}],"temperature":0}
    req=urllib.request.Request("https://api.openai.com/v1/chat/completions",data=json.dumps(body).encode(),headers={"Authorization":"Bearer "+os.environ["OPENAI_API_KEY"],"Content-Type":"application/json"})
    out=json.load(urllib.request.urlopen(req,timeout=120))["choices"][0]["message"]["content"]
    open(f"work/tx/{aid}.en.txt","w").write(out); print("==",aid); print(out)
