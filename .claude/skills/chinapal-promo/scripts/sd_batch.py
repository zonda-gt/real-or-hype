import json,requests,time,os,sys
H={'Authorization':'Bearer proxy-injected'}; URL='https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks'
WHO=('A friendly East Asian man in his twenties with shoulder-length lilac-purple and blonde hair, wearing a black zip-up jacket over a black-and-white striped sweater')
ROOM=('Vertical 9:16 Instagram Reel, shot on an iPhone on a locked-off tripod; the camera does not move at all. '+WHO+
' sits on a stool in a bright minimal apartment, framed from the waist up and centred, with space above his head. Behind him, about 1.5 metres away, a plain warm off-white wall, '
'a window with soft daylight on the left and a small plant. ')
END=' Natural light, realistic, no text, no music.'
S=[("02_orbit",5,ROOM+'The wall behind him is completely bare, nothing on it and nothing floating in the air. He glances left and right with curiosity, then looks back at the camera and says in English: "Rooftop bars, dumpling spots, that cafe..."'),
("03_vertigo",4,ROOM+'He stays completely still, deadpan, looking straight into the camera, and says slowly in English: "And you have been to none of them."'),
("04_uiworld",4,ROOM+'He glances up toward his left shoulder, then back at the camera, makes a small tossing gesture with one hand and says in English: "So just send them all to us."'),
("05_checklist",5,ROOM+'He counts on his fingers, one, two, three, and says in English: "Save the reel. Send it to us. That is it."'),
("06_pullback",5,ROOM+'He talks to the camera calmly, hands relaxed, and says in English: "We turn them into a day-by-day plan, built around your reels."'),
("07_route",5,ROOM+'He turns half toward the wall behind him and points to three spots on it from left to right, then says in English: "Day one: this cafe, then the garden, then dinner here."'),
("08_cafe",4,'Vertical 9:16 Instagram Reel shot on an iPhone. '+WHO+' sits at a wooden table in a cosy cat cafe in the former French Concession of Shanghai, a fluffy ginger cat next to his latte, he smiles and strokes the cat, soft window light, handheld but steady. No dialogue.'),
("09_cover",4,ROOM+'He lifts his chin slightly, looks straight into the camera with a confident small smile and says in English: "Your trip."'),
("10_framebreak",6,ROOM+'He leans forward toward the camera and reaches both open hands toward the lens, energetic, and says in English: "Send us your saved reels. Comment TRIP and I will send you the link.")')]
os.makedirs('sd/shots',exist_ok=True); tasks={}
if os.path.exists('sd/shots/tasks.json'): tasks=json.load(open('sd/shots/tasks.json'))
for n,d,t in S:
    if n in tasks or (n!='02_orbit' and len(sys.argv)>1): continue
    body={"model":"doubao-seedance-2-0-mini-260615","content":[{"type":"text","text":t+END}],"ratio":"9:16","resolution":"480p","duration":d,"generate_audio":True,"watermark":False,"seed":77911}
    for a in range(4):
        r=requests.post(URL,headers=H,json=body,timeout=60)
        if r.status_code==200: tasks[n]=r.json()['id']; break
        print(n,r.status_code,r.text[:200]); time.sleep(5*(a+1))
    json.dump(tasks,open('sd/shots/tasks.json','w')); time.sleep(1)
print('submitted',len(tasks))
pending=dict(tasks); tok=0
while pending:
    time.sleep(15)
    for n,i in list(pending.items()):
        d=requests.get(f'{URL}/{i}',headers=H,timeout=60).json(); s=d.get('status')
        if s=='succeeded':
            v=requests.get(d['content']['video_url'],timeout=120).content; open(f'sd/shots/{n}.mp4','wb').write(v)
            tok+=d['usage']['total_tokens']; print(n,'ok',d['usage']['total_tokens'],flush=True); del pending[n]
        elif s in('failed','expired','cancelled'): print(n,s,json.dumps(d.get('error'))[:200],flush=True); del pending[n]
print('total tokens',tok,'~yuan',round(tok*0.023/1000,2))
