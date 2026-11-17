# Download an Instagram reel (e.g. a reference creator) via TikHub. usage: ig_fetch.py <reel_url> <outdir>
# Writes <shortcode>.mp4 and <shortcode>_meta.json (caption, views, duration).
import sys,json,os,re,subprocess,urllib.request,urllib.parse
url,out=sys.argv[1],sys.argv[2]; os.makedirs(out,exist_ok=True)
code=re.search(r'/(?:reel|p)/([^/?]+)',url).group(1)
q=urllib.parse.quote(f'https://www.instagram.com/reel/{code}/',safe='')
req=urllib.request.Request(f'https://api.tikhub.io/api/v1/instagram/v1/fetch_post_by_url?post_url={q}',headers={'Authorization':'Bearer '+os.environ['TIKHUB_API_KEY'],'User-Agent':'Mozilla/5.0 Chrome/124'})
d=json.load(urllib.request.urlopen(req,timeout=90))['data']
def find(o,key):
    if isinstance(o,dict):
        for k,v in o.items():
            if k==key: yield v
            yield from find(v,key)
    elif isinstance(o,list):
        for v in o: yield from find(v,key)
vv=next(find(d,'video_versions')); best=max(vv,key=lambda x:(x.get('height',0),x.get('bandwidth',0)))
subprocess.run(['curl','-sSL','-A','Mozilla/5.0','-o',f'{out}/{code}.mp4',best['url']],check=True)
meta={'caption':next(find(d,'text'),''),'username':next(find(d,'username'),''),'views':next(find(d,'video_view_count'),None),'duration':next(find(d,'video_duration'),None)}
json.dump(meta,open(f'{out}/{code}_meta.json','w'),ensure_ascii=False,indent=1); print(code,meta['username'],meta['views'],meta['duration'])
