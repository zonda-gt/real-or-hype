# Find and download a music track from Instagram's audio library (TikHub) to bake into a reel.
# usage: ig_music.py search <out.json> "<keyword>" ["<keyword>" ...]   lists tracks (index, title, artist, length, highlights)
#        ig_music.py get <out.json> <index> <out.m4a>                  downloads one; prints its highlight starts (s)
# Use a highlight start as MUSIC_IN in plan_A.py so the reel opens on the catchy part.
import sys,os,json,urllib.request,urllib.parse,subprocess
H={'Authorization':'Bearer '+os.environ['TIKHUB_API_KEY'],'User-Agent':'Mozilla/5.0 Chrome/124'}
def walk(o):
    if isinstance(o,dict):
        if 'title' in o and 'display_artist' in o and o.get('progressive_download_url'): yield o
        for v in o.values(): yield from walk(v)
    elif isinstance(o,list):
        for v in o: yield from walk(v)
cmd,out=sys.argv[1],sys.argv[2]
if cmd=='search':
    tracks=[]; seen=set()
    for kw in sys.argv[3:]:
        u='https://api.tikhub.io/api/v1/instagram/v2/search_music?keyword='+urllib.parse.quote(kw)
        d=json.load(urllib.request.urlopen(urllib.request.Request(u,headers=H),timeout=90))
        for m in walk(d.get('data')):
            if m['id'] in seen: continue
            seen.add(m['id']); m['_kw']=kw; tracks.append(m)
    json.dump(tracks,open(out,'w'),ensure_ascii=False)
    for i,m in enumerate(tracks):
        print(f"{i:2d} [{m['_kw'][:14]}] {m['title'][:38]} - {m['display_artist'][:24]} | {m['duration_in_ms']/1000:.0f}s | lyrics {m.get('has_lyrics')} | explicit {m.get('is_explicit')} | hl {[round(x/1000,1) for x in m.get('highlight_start_times_in_ms') or []]}")
elif cmd=='get':
    m=json.load(open(out))[int(sys.argv[3])]; dst=sys.argv[4]
    subprocess.run(['curl','-sSL','-A','Mozilla/5.0','-o',dst+'.mp4',m['progressive_download_url']],check=True)
    subprocess.run(['ffmpeg','-loglevel','error','-y','-i',dst+'.mp4','-vn','-c:a','copy',dst],check=True); os.remove(dst+'.mp4')
    json.dump({k:m.get(k) for k in ['id','title','display_artist','duration_in_ms','highlight_start_times_in_ms','has_lyrics','is_explicit']},open(dst+'.json','w'),ensure_ascii=False)
    print(dst,m['title'],'-',m['display_artist'],'highlights',[round(x/1000,1) for x in m.get('highlight_start_times_in_ms') or []])
