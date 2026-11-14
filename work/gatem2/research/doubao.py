# usage: doubao.py out.json "question" [model]
import sys,os,json,urllib.request,time
out,q=sys.argv[1],sys.argv[2]; model=sys.argv[3] if len(sys.argv)>3 else 'doubao-seed-2-1-lite-260915'
body={"model":model,"input":q,"tools":[{"type":"web_search","max_keyword":3}],"thinking":{"type":"disabled"},"max_output_tokens":1200}
req=urllib.request.Request('https://ark.cn-beijing.volces.com/api/v3/responses',data=json.dumps(body).encode(),
    headers={'Authorization':'Bearer '+os.environ['ARK_API_KEY'],'Content-Type':'application/json','User-Agent':'curl/8.5.0'})
for k in range(3):
    try: d=json.load(urllib.request.urlopen(req,timeout=280)); break
    except Exception as e: print('retry',e); time.sleep(4)
else: sys.exit(1)
txt='';cites=[]
for o in d.get('output',[]):
    if o.get('type')=='message':
        for c in o['content']:
            if c.get('type')=='output_text':
                txt+=c['text']; cites+=[a.get('url') for a in c.get('annotations',[]) if a.get('url')]
json.dump({'q':q,'answer':txt,'sources':sorted(set(cites))},open(out,'w'),ensure_ascii=False,indent=1)
print(txt); print('SOURCES:',sorted(set(cites))[:5])
