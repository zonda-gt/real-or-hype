# generate each line with the creator's voice clone, trim, atempo 1.2, Whisper-check (up to 3 takes)
import sys,subprocess,json,re,os,numpy as np
def load(f): return np.frombuffer(subprocess.run(['ffmpeg','-loglevel','error','-i',f,'-ar','16000','-ac','1','-f','f32le','-'],capture_output=True).stdout,dtype=np.float32)
sys.path.insert(0,'.'); from lines import LINES
from faster_whisper import WhisperModel
KEY='/tmp/claude-0/-home-user-real-or-hype/a37d60e4-5484-5fc0-8caf-3caf6ed0466b/scratchpad/el.key'
EL='../../.claude/skills/real-or-hype-video/scripts/eltts_s.py'
VS='{"stability":0.5,"similarity_boost":0.9,"style":0.15,"use_speaker_boost":true}'
m=WhisperModel("small",device="cpu",compute_type="int8")
norm=lambda s: re.sub(r'[^a-z0-9 ]','',s.lower().replace('-',' ')).split()
def num(w): return w
ids=sys.argv[1:] or list(LINES)
res={}
for k in ids:
    txt=LINES[k]; best=None
    for t in range(3):
        raw=f'vo/{k}_raw{t}.mp3'; out=f'vo/{k}.wav'
        subprocess.run(['python3',EL,KEY,'KdPzirZUC0HY6WhfwyeE',txt,raw,VS],check=True)
        af='silenceremove=start_periods=1:start_threshold=-55dB:start_silence=0.03,areverse,silenceremove=start_periods=1:start_threshold=-55dB:start_silence=0.08,areverse,atempo=1.2'
        subprocess.run(['ffmpeg','-y','-loglevel','error','-i',raw,'-af',af,'-ar','44100','-ac','1',f'vo/{k}_t{t}.wav'],check=True)
        segs,_=m.transcribe(load(f'vo/{k}_t{t}.wav'),language='en',beam_size=5)
        heard=' '.join(s.text for s in segs).strip()
        a,b=norm(txt),norm(heard)
        NUM={'a','and','one','two','six','seven','twenty','thirty','forty','hundred','thousand','fourteen','dollars'}
        miss=[w for w in a if w not in b and not (w in NUM and any(c.isdigit() for c in heard))]
        dur=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f'vo/{k}_t{t}.wav'],capture_output=True,text=True).stdout)
        print(k,t,f'{dur:.2f}s','MISS' if miss else 'OK',miss,'|',heard,flush=True)
        if not miss or best is None: best=(t,dur,heard,miss)
        if not miss: break
    os.replace(f'vo/{k}_t{best[0]}.wav',f'vo/{k}.wav')
    res[k]={'dur':best[1],'heard':best[2],'miss':best[3]}
d=json.load(open('vo/vo.json')) if os.path.exists('vo/vo.json') else {}
d.update(res); json.dump(d,open('vo/vo.json','w'),indent=1)
