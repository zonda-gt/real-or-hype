# build_draft.py <jianying|capcut> <media_dir> <manifest.json> <out_drafts_dir> <draft_name>
import sys,os,json
lib,M,manf,OUT,NAME=sys.argv[1:6]
man=json.load(open(manf)); us=lambda s:int(round(s*1_000_000))
if lib=='jianying':
    import pyJianYingDraft as d
    from pyJianYingDraft import TrackSpec
else:
    import pycapcut as d
os.makedirs(OUT,exist_ok=True)
folder=d.DraftFolder(OUT); script=folder.create_draft(NAME,1080,1920,30,allow_replace=True)
def track(kind,name):
    tt={'video':d.TrackType.video,'audio':d.TrackType.audio}[kind]
    if lib=='jianying': return script.append_track(TrackSpec(tt,name))
    script.add_track(tt,name, relative_index=track.idx.setdefault(kind,0)); track.idx[kind]+=1; return name
track.idx={}
# main video: shots back to back from 0 (lengths taken from the next shot's start, so there are no gaps)
main=track('video','main')
V=man['video']
for i,v in enumerate(V):
    end=V[i+1]['start'] if i+1<len(V) else man['total']
    a,b=us(v['start']),us(end)
    mat=d.VideoMaterial(os.path.join(M,v['file'])); L=b-a
    if mat.duration>=L: seg=d.VideoSegment(mat,d.trange(a,L),source_timerange=d.trange(0,L))
    else: seg=d.VideoSegment(mat,d.trange(a,L),speed=mat.duration/L)   # a few ms short: stretch imperceptibly to fill the slot
    script.add_segment(seg,main)
# graphics: put each PNG on the first graphics track where it doesn't overlap
lanes=[]
for o in sorted(man['overlays'],key=lambda o:o['start']):
    for ln in lanes:
        if ln['end']<=o['start']+1e-6: break
    else:
        ln={'end':0,'ref':track('video',f'graphics{len(lanes)+1}')}; lanes.append(ln)
    a,b=us(o['start']),us(o['end'])
    script.add_segment(d.VideoSegment(os.path.join(M,o['file']),d.trange(a,b-a)),ln['ref']); ln['end']=o['end']
# subtitles as native, editable text
ref=d.TextSegment('Subtitle',d.trange(0,1_000_000),style=d.TextStyle(size=9,bold=True,color=(1.0,1.0,1.0),align=1,auto_wrapping=True),
                  border=d.TextBorder(color=(0.0,0.0,0.0),width=50.0))
script.import_srt(os.path.join(M,man['subtitles']),'subtitles',style_reference=ref,clip_settings=d.ClipSettings(transform_y=-0.52))
# audio tracks
for key,name in [('narration','narration'),('sfx','sound effects')]:
    t=track('audio',name)
    items=sorted(man[key],key=lambda x:x['start'])
    for i,x in enumerate(items):
        mat=d.AudioMaterial(os.path.join(M,x['file'])); a=us(x['start']); n=mat.duration
        if i+1<len(items): n=min(n,us(items[i+1]['start'])-a-1)   # encoder padding must not touch the next clip
        script.add_segment(d.AudioSegment(mat,d.trange(a,n),source_timerange=d.trange(0,n)),t)
t=track('audio','sting'); x=man['sting']; mat=d.AudioMaterial(os.path.join(M,x['file'])); n=mat.duration
script.add_segment(d.AudioSegment(mat,d.trange(us(x['start']),n),source_timerange=d.trange(0,n)),t)
script.save(); print(lib,'draft saved:',os.path.join(OUT,NAME),'| graphics tracks',len(lanes))
