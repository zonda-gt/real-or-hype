# Doubao Speech TTS (V3 HTTP unidirectional). Key is proxy-injected as X-Api-Key for openspeech.bytedance.com.
# usage: doubao_tts.py <speaker> "<text or @file>" <out.mp3> [--style "用...的语气"] [--rate 20] [--resource seed-icl-2.0]
#   S_ speakers (clones) -> resource seed-icl-2.0 + model_type 4; *_uranus_bigtts / saturn_* -> seed-tts-2.0.
#   --extra '{"use_tag_parser":true}' lets <cot text=开心>...</cot> tags set per-sentence emotion instead of being read aloud.
#   --rate: speech_rate -50..100 (0 = normal; 20 is about 1.2x).  --style: context_texts instruction (expressiveness).
import sys,json,base64,urllib.request,argparse,uuid
ap=argparse.ArgumentParser(); ap.add_argument('speaker'); ap.add_argument('text'); ap.add_argument('out')
ap.add_argument('--style'); ap.add_argument('--rate',type=int,default=0); ap.add_argument('--resource'); ap.add_argument('--loud',type=int,default=0); ap.add_argument('--extra',help='extra JSON merged into additions, e.g. {"use_tag_parser":true}')
a=ap.parse_args()
text=open(a.text[1:]).read().strip() if a.text.startswith('@') else a.text
clone=a.speaker.startswith('S_'); res=a.resource or ('seed-icl-2.0' if clone else 'seed-tts-2.0')
add={}
if clone: add['model_type']=4
if a.style: add['context_texts']=[a.style]
if a.extra: add.update(json.loads(a.extra))
body={"user":{"uid":"spot-video"},"req_params":{"text":text,"speaker":a.speaker,
      "audio_params":{"format":"mp3","sample_rate":24000,"speech_rate":a.rate,"loudness_rate":a.loud},
      "additions":json.dumps(add,ensure_ascii=False)}}
req=urllib.request.Request("https://openspeech.bytedance.com/api/v3/tts/unidirectional",data=json.dumps(body,ensure_ascii=False).encode(),
    headers={"Content-Type":"application/json","X-Api-Key":"proxy-injected","X-Api-Resource-Id":res,"X-Api-Request-Id":str(uuid.uuid4())})
audio=b''; err=None
try:
    with urllib.request.urlopen(req,timeout=180) as r:
        for line in r:
            line=line.strip()
            if not line: continue
            try: j=json.loads(line)
            except: continue
            if j.get('data'): audio+=base64.b64decode(j['data'])
            c=j.get('code',0)
            if c not in (0,20000000): err=j
except urllib.error.HTTPError as e: print('HTTP',e.code,e.read()[:400].decode('utf8','ignore')); sys.exit(1)
if err: print('ERR',json.dumps(err,ensure_ascii=False)[:400])
open(a.out,'wb').write(audio); print('bytes',len(audio),'resource',res)
