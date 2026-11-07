# usage: sd_batch2.py shots.json outdir   (shots: [{name,dur,action,line|null,room:true|false,scene?}])
import json,requests,time,os,sys
H={'Authorization':'Bearer proxy-injected'}; URL='https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks'
WHO='A friendly East Asian man in his twenties with shoulder-length lilac-purple and blonde hair, wearing a black zip-up jacket over a black-and-white striped sweater'
ROOM=('Vertical 9:16 Instagram Reel, shot on an iPhone on a locked-off tripod; the camera does not move at all. '+WHO+
' sits on a stool in a bright minimal apartment, framed from the waist up and centred, with space above his head. Behind him, about 1.5 metres away, a plain warm off-white wall that is completely bare, '
'a window with soft daylight on the left and a small plant. ')
END=' Natural light, realistic, no text on screen, no music.'
S=json.load(open(sys.argv[1])); OUT=sys.argv[2]; os.makedirs(OUT,exist_ok=True)
TF=f'{OUT}/tasks.json'; tasks=json.load(open(TF)) if os.path.exists(TF) else {}
for s in S:
    if s['name'] in tasks or os.path.exists(f"{OUT}/{s['name']}.mp4"): continue
    txt=(ROOM if s.get('room',True) else s['scene'].replace('WHO',WHO)+' ')+s['action']
    if s.get('line'): txt+=f' He says in English, upbeat and quick, like a confident creator: "{s["line"]}"'
    body={"model":"doubao-seedance-2-0-mini-260615","content":[{"type":"text","text":txt+END}],"ratio":"9:16","resolution":"480p","duration":s['dur'],"generate_audio":True,"watermark":False,"seed":77911}
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
        d=requests.get(f'{URL}/{i}',headers=H,timeout=60).json(); st=d.get('status')
        if st=='succeeded':
            open(f'{OUT}/{n}.mp4','wb').write(requests.get(d['content']['video_url'],timeout=120).content); tok+=d['usage']['total_tokens']; print(n,'ok',flush=True); del pending[n]
        elif st in('failed','expired','cancelled'): print(n,st,json.dumps(d.get('error'))[:200],flush=True); del pending[n]
print('tokens',tok,'~yuan',round(tok*0.023/1000,2))
