import os,sys,json,base64,time,requests
from concurrent.futures import ThreadPoolExecutor
K=os.environ['OPENAI_API_KEY']; OUT=sys.argv[1]; REF=sys.argv[2]; J=json.load(open(sys.argv[3]))
BASE=("Use the person in the reference photo: keep his exact face, purple-and-blonde hair, black zip jacket with white PRINCE lettering "
"and black-and-white striped sweater. New photo, vertical 9:16, shot on an iPhone on a tripod for an Instagram Reel: he sits on a stool in a bright, "
"minimal apartment, framed from the waist up, centred, with clear space above his head. Behind him, about 1.5 metres away, a plain warm off-white wall "
"with lots of empty space, a window with soft daylight on the left and a small plant. Soft natural light on his face, realistic, no text. ")
def go(it):
    p=f"{OUT}/{it['name']}.png"
    if os.path.exists(p): return it['name'],'cached'
    for a in range(4):
        try:
            r=requests.post('https://api.openai.com/v1/images/edits',headers={'Authorization':f'Bearer {K}'},
              files={'image[]':open(REF,'rb')},data={'model':'gpt-image-2','prompt':BASE+it['pose'],'size':'1024x1536','quality':'high','n':'1'},timeout=400)
            d=r.json()
            if 'data' in d: open(p,'wb').write(base64.b64decode(d['data'][0]['b64_json'])); return it['name'],'ok'
            err=d
        except Exception as e: err=str(e)
        time.sleep(5*(a+1))
    return it['name'],f'FAIL {err}'
with ThreadPoolExecutor(3) as ex:
    for r in ex.map(go,J): print(*r,flush=True)
