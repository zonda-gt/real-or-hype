import os,sys,json,subprocess
from concurrent.futures import ThreadPoolExecutor
def one(aid):
    out=f"work/tx/{aid}.json"
    if os.path.exists(out): return aid,"exists"
    mp3=f"work/audio/{aid}.mp3"
    subprocess.run(["ffmpeg","-v","error","-y","-i",f"raw/{aid}.mp4","-vn","-ac","1","-ar","16000","-b:a","64k",mp3],check=True)
    p=subprocess.run(["curl","-sS","-m","180","https://api.openai.com/v1/audio/transcriptions","-H","Authorization: Bearer "+os.environ["OPENAI_API_KEY"],
      "-F",f"file=@{mp3}","-F","model=whisper-1","-F","response_format=verbose_json","-F","language=zh"],capture_output=True,text=True)
    d=json.loads(p.stdout)
    if "error" in d: return aid,"ERR "+str(d["error"].get("message"))[:100]
    json.dump(d,open(out,"w"),ensure_ascii=False,indent=1)
    return aid,f'{d.get("duration")}s '+d.get("text","")[:80]
ids=[f[:-4] for f in sorted(os.listdir("raw")) if f.endswith(".mp4")]
with ThreadPoolExecutor(6) as ex:
    for r in ex.map(one,ids): print(*r)
