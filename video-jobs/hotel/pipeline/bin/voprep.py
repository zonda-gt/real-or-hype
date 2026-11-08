"""Trim + speed narration, derive word timings from ElevenLabs char alignment. usage: voprep.py TEMPO key..."""
import sys,json,subprocess,re
tempo=float(sys.argv[1])
for k in sys.argv[2:]:
    j=json.load(open(f'vo/m/{k}.json')); al=j['alignment']
    ch,st,en=al['characters'],al['character_start_times_seconds'],al['character_end_times_seconds']
    idx=[i for i,c in enumerate(ch) if c.strip()]
    t0=max(0,st[idx[0]]-0.03); t1=en[idx[-1]]+0.10
    # words
    words=[];cur='';ws=None;we=None
    for c,s,e in zip(ch,st,en):
        if c.isspace():
            if cur: words.append([cur,ws,we]); cur=''
            continue
        if not cur: ws=s
        cur+=c; we=e
    if cur: words.append([cur,ws,we])
    words=[[w,round((s-t0)/tempo,3),round((e-t0)/tempo,3)] for w,s,e in words]
    subprocess.run(['ffmpeg','-v','error','-y','-i',f'vo/m/{k}.mp3','-af',f'atrim={t0}:{t1},asetpts=N/SR/TB,atempo={tempo},afade=t=out:st={(t1-t0)/tempo-0.04}:d=0.04','-ar','48000','-ac','1',f'vo/p/{k}.wav'],check=True)
    d=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f'vo/p/{k}.wav'],capture_output=True,text=True).stdout)
    json.dump({'dur':d,'words':words,'text':j['text']},open(f'vo/p/{k}.json','w'))
    print(k,round(d,2),' '.join(f"{w}@{s}" for w,s,e in words[:6]))
