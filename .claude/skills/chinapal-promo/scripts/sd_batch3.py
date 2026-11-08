# usage: sd_batch3.py shots.json outdir asset_id   (presenter from a verified Ark portrait asset)
import json,requests,time,os,sys
H={'Authorization':'Bearer proxy-injected'}; URL='https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks'
S=json.load(open(sys.argv[1])); OUT=sys.argv[2]; ASSET=sys.argv[3]; os.makedirs(OUT,exist_ok=True)
WHO='The man in image 1 (same face, lilac-blonde hair, black zip-up jacket with white lettering over a black-and-white striped sweater)'
ROOM=('Vertical 9:16 Instagram Reel, shot on an iPhone on a locked-off tripod; the camera does not move at all. '+WHO+
' sits on a stool in a bright minimal apartment, framed from the waist up and centred, with space above his head. Behind him, about 1.5 metres away, a plain warm off-white wall that is completely bare, a window with soft daylight on the left and a small plant. ')
END=' Natural light, realistic, no text on screen, no music.'
TF=f'{OUT}/tasks.json'; tasks=json.load(open(TF)) if os.path.exists(TF) else {}
for s in S:
    if s['name'] in tasks or os.path.exists(f"{OUT}/{s['name']}.mp4"): continue
    txt=(ROOM if s.get('room',True) else s['scene'].replace('WHO',WHO)+' ')+s['action']
    if s.get('line'): txt+=f' He starts speaking at the very first frame and says only this exact line in English, upbeat and quick, nothing before or after it: "{s["line"]}"'
    body={"model":"doubao-seedance-2-0-mini-260615","content":[{"type":"text","text":txt+END},{"type":"image_url","image_url":{"url":f"asset://{ASSET}"},"role":"reference_image"}],
          "ratio":"9:16","resolution":"480p","duration":s['dur'],"generate_audio":True,"watermark":False,"seed":s.get("seed",77911)}
    for a in range(4):
        r=requests.post(URL,headers=H,json=body,timeout=60)
        if r.status_code==200: tasks[s['name']]=r.json()['id']; break
        print(s['name'],r.status_code,r.text[:200],flush=True); time.sleep(5*(a+1))
    json.dump(tasks,open(TF,'w')); time.sleep(1)
print('submitted',len(tasks),flush=True)
pending={k:v for k,v in tasks.items() if not os.path.exists(f'{OUT}/{k}.mp4')}; tok=0
while pending:
    time.sleep(15)
    for n,i in list(pending.items()):
        try: d=requests.get(f'{URL}/{i}',headers=H,timeout=60).json()
        except Exception: continue
        st=d.get('status')
        if st=='succeeded':
            open(f'{OUT}/{n}.mp4','wb').write(requests.get(d['content']['video_url'],timeout=120).content); tok+=d['usage']['total_tokens']; print(n,'ok',flush=True); del pending[n]
        elif st in('failed','expired','cancelled'): print(n,st,json.dumps(d.get('error'))[:200],flush=True); del pending[n]
print('tokens',tok,'~yuan',round(tok*0.023/1000,2),flush=True)
