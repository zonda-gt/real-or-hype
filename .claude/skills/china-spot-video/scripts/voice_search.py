# Search the ElevenLabs shared voice library. usage:
#   voice_search.py --gender male --search "chinese accent" [--accent british] [--use_case social_media] [--descriptive upbeat] [--age young] [-n 30]
import argparse,json,os,urllib.request,urllib.parse
ap=argparse.ArgumentParser(); ap.add_argument('--gender'); ap.add_argument('--search'); ap.add_argument('--accent'); ap.add_argument('--use_case')
ap.add_argument('--descriptive'); ap.add_argument('--age'); ap.add_argument('--language',default='en'); ap.add_argument('-n',type=int,default=30); a=ap.parse_args()
q={'page_size':a.n,'sort':'usage_character_count_1y','language':a.language}
for k,v in [('gender',a.gender),('search',a.search),('accent',a.accent),('use_cases',a.use_case),('descriptives',a.descriptive),('age',a.age)]:
    if v: q[k]=v
req=urllib.request.Request('https://api.elevenlabs.io/v1/shared-voices?'+urllib.parse.urlencode(q),headers={'xi-api-key':os.environ['ELEVENLABS_API_KEY']})
for v in json.load(urllib.request.urlopen(req,timeout=60)).get('voices',[]):
    print(v['voice_id'],'|',v['name'][:46],'|',v.get('accent'),'|',v.get('age'),'|',v.get('descriptive'),'|',v.get('usage_character_count_1y'),'|',(v.get('description') or '').replace('\n',' ')[:90])
