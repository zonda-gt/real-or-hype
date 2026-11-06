import json,subprocess,sys
name=sys.argv[1]; MAXGAP=float(sys.argv[2]) if len(sys.argv)>2 else 0.30; TEMPO=1.12
d=json.load(open(f"work/vo/{name}.json")); W=d["words"]
dur=float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f"work/vo/{name}.mp3"],capture_output=True,text=True).stdout)
# chunks: keep audio, but shrink gaps > MAXGAP
cuts=[]; pad=0.06
keep=[]; start=0.0
for a,b in zip(W,W[1:]):
    gap=b["s"]-a["e"]
    if gap>MAXGAP:
        keep.append((start,a["e"]+pad)); start=b["s"]-(MAXGAP-pad)
keep.append((start,min(dur,W[-1]["e"]+0.25)))
# map times
def mp(t):
    acc=0
    for s,e in keep:
        if t<=e: return acc+max(0,t-s)
        acc+=e-s
    return acc
for w in W: w["s"]=round(mp(w["s"])/TEMPO,3); w["e"]=round(mp(w["e"])/TEMPO,3)
filt="".join(f"[0:a]atrim={s:.3f}:{e:.3f},asetpts=PTS-STARTPTS[a{i}];" for i,(s,e) in enumerate(keep))
filt+="".join(f"[a{i}]" for i in range(len(keep)))+f"concat=n={len(keep)}:v=0:a=1,atempo={TEMPO},aresample=48000[o]"
subprocess.run(["ffmpeg","-v","error","-y","-i",f"work/vo/{name}.mp3","-filter_complex",filt,"-map","[o]","-c:a","pcm_s16le",f"work/vo/{name}_t.wav"],check=True)
nd=float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f"work/vo/{name}_t.wav"],capture_output=True,text=True).stdout)
json.dump({"text":d["text"],"words":W,"duration":nd,"tempo":TEMPO,"maxgap":MAXGAP},open(f"work/vo/{name}_t.json","w"),indent=1)
print(name,f"{dur:.2f}->{nd:.2f}s"," ".join(f"{w['w']}@{w['s']:.2f}" for w in W))
