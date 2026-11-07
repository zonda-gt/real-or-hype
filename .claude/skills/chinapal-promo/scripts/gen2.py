import os,sys,json,base64,time,requests
from concurrent.futures import ThreadPoolExecutor
K=os.environ['OPENAI_API_KEY']; OUT=sys.argv[1]; J=json.load(open(sys.argv[2]))
def go(it):
    p=f"{OUT}/{it['name']}.png"
    if os.path.exists(p): return it['name'],'cached'
    for a in range(3):
        try:
            d=requests.post('https://api.openai.com/v1/images/generations',headers={'Authorization':f'Bearer {K}'},json={'model':it['model'],'prompt':it['prompt'],'size':it.get('size','1152x2496'),'quality':'high','n':1},timeout=600).json()
            if 'data' in d: open(p,'wb').write(base64.b64decode(d['data'][0]['b64_json'])); return it['name'],'ok'
            err=d
        except Exception as e: err=str(e)
        time.sleep(5)
    return it['name'],f'FAIL {err}'
with ThreadPoolExecutor(4) as ex:
    for r in ex.map(go,J): print(*r,flush=True)
