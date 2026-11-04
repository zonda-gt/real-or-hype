import sys,os,glob,subprocess,json
from PIL import Image,ImageDraw,ImageFont
sp=sys.argv[1]; os.chdir(sp)
font=ImageFont.load_default(size=20)
N=6; TW=180
def probe(f):
    r=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','json',f],capture_output=True,text=True)
    return float(json.loads(r.stdout)['format']['duration'])
for f in sorted(glob.glob('prev/*.mp4')):
    name=os.path.basename(f)[:-4]; out=f'strips/{name}.jpg'
    if os.path.exists(out): continue
    try: d=probe(f)
    except: continue
    frames=[]
    for i in range(N):
        t=d*(i+0.5)/N
        r=subprocess.run(['ffmpeg','-loglevel','error','-ss',f'{t:.2f}','-i',f,'-frames:v','1','-vf',f'scale={TW}:-2','-f','image2pipe','-vcodec','png','-'],capture_output=True)
        if r.stdout:
            import io; im=Image.open(io.BytesIO(r.stdout)).convert('RGB'); frames.append((t,im))
    if not frames: continue
    h=max(im.height for _,im in frames)
    row=Image.new('RGB',(TW*N,h+26),'black'); d2=ImageDraw.Draw(row)
    d2.text((4,2),f'{name.replace("VID_20260910_","")}  {d:.0f}s',fill='yellow',font=font)
    for i,(t,im) in enumerate(frames):
        row.paste(im,(i*TW,26)); d2.text((i*TW+4,h+2),f'{t:.0f}s',fill='white',font=font)
    row.save(out,quality=80)
print('STRIPS')
