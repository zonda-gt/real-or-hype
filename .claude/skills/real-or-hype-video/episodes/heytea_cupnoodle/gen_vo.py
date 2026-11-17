# Generate narration lines with ElevenLabs, Whisper-check each take, keep the SHORTEST take that passes.
# usage: gen_vo.py <keyfile> <voice_id> <model> '<settings json>' <lines.json> <outdir> [takes=3] [atempo=1.0]
# Audio tags like [excited] are stripped for the check. Writes <outdir>/<key>.wav (trimmed, inner pauses squeezed).
import sys,os,json,re,subprocess,difflib
key,vid,model,vs,lf,od=sys.argv[1:7]; N=int(sys.argv[7]) if len(sys.argv)>7 else 3; AT=float(sys.argv[8]) if len(sys.argv)>8 else 1.0
os.makedirs(od,exist_ok=True); lines=json.load(open(lf)); json.dump(lines,open(od+'/lines.json','w'),indent=1,ensure_ascii=False)
T=os.path.join(os.path.dirname(os.path.abspath(__file__)),'../../scripts/eltts_m.py')
from faster_whisper import WhisperModel
import numpy as np
m=WhisperModel('medium.en',device='cpu',compute_type='int8')
def norm(s):
    s=re.sub(r'\[[^\]]*\]','',s).lower().replace('hey tea','heytea').replace('twenty-two','22')
    return re.sub(r'[^a-z0-9 ]',' ',s).split()
def hear(f):
    a=np.frombuffer(subprocess.run(['ffmpeg','-loglevel','error','-i',f,'-ar','16000','-ac','1','-f','f32le','-'],capture_output=True).stdout,dtype=np.float32)
    segs,_=m.transcribe(a,language='en',beam_size=5); return ' '.join(s.text for s in segs)
def dur(f): return float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f],capture_output=True,text=True).stdout)
SQ=(f'silenceremove=start_periods=1:start_threshold=-55dB:start_silence=0.03,areverse,silenceremove=start_periods=1:start_threshold=-55dB:start_silence=0.08,areverse,'
    f'silenceremove=stop_periods=-1:stop_duration=0.2:stop_threshold=-45dB:stop_silence=0.16'+(f',atempo={AT}' if AT!=1 else '')+',aresample=48000')
for k,txt in lines.items():
    ok=[]
    for i in range(1,N+1):
        f=f'{od}/{k}_t{i}.mp3'
        if not os.path.exists(f):
            r=subprocess.run(['python3','-I',T,key,vid,txt,f,vs,model],capture_output=True,text=True)
            if r.returncode or not os.path.exists(f): print(k,i,'TTS fail',r.stdout[-200:]); continue
        w=subprocess.run(['ffmpeg','-loglevel','error','-y','-i',f,'-af',SQ,'-ac','2',f[:-4]+'.wav']); d=dur(f[:-4]+'.wav')
        h=hear(f); a=norm(txt); b=norm(h.replace('Hey, tea','heytea').replace('Haiti','heytea').replace('Hay tea','heytea').replace('Hey T','heytea'))
        sc=difflib.SequenceMatcher(None,a,b).ratio()
        print(f'{k} t{i} {d:4.2f}s match {sc:.2f} | {h.strip()}')
        if sc>=0.85: ok.append((d,f[:-4]+'.wav'))
    if ok:
        d,best=min(ok); subprocess.run(['cp',best,f'{od}/{k}.wav']); print(f'  -> {k}: {os.path.basename(best)} {d:.2f}s')
    else: print(f'  -> {k}: NO TAKE PASSED')
