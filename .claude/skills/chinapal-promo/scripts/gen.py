import os,sys,json,base64,time,requests
from concurrent.futures import ThreadPoolExecutor
K=os.environ['OPENAI_API_KEY']; OUT=sys.argv[1]
J=json.load(open(sys.argv[2]))
def go(item):
    name,prompt,size,q=item['name'],item['prompt'],item.get('size','1024x1536'),item.get('quality','medium')
    p=f'{OUT}/{name}.png'
    if os.path.exists(p): return name,'cached'
    for a in range(4):
        try:
            r=requests.post('https://api.openai.com/v1/images/generations',headers={'Authorization':f'Bearer {K}'},json={'model':'gpt-image-2','prompt':prompt,'size':size,'quality':q,'n':1},timeout=300)
            d=r.json()
            if 'data' in d:
                open(p,'wb').write(base64.b64decode(d['data'][0]['b64_json'])); return name,'ok'
            err=d
        except Exception as e: err=str(e)
        time.sleep(5*(a+1))
    return name,f'FAIL {err}'
with ThreadPoolExecutor(4) as ex:
    for r in ex.map(go,J): print(*r,flush=True)
