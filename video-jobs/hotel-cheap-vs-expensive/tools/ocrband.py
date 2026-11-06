import sys,os,subprocess,glob,pytesseract,collections
from PIL import Image
aid=sys.argv[1]; fps=sys.argv[2] if len(sys.argv)>2 else "2"
d=f"work/frames/{aid}"; os.makedirs(d,exist_ok=True)
if not glob.glob(d+"/*.png"):
    subprocess.run(["ffmpeg","-v","error","-i",f"raw/best/{aid}.mp4","-vf",f"fps={fps}",d+"/f%04d.png"],check=True)
rows=collections.Counter()
for f in sorted(glob.glob(d+"/*.png")):
    im=Image.open(f); W,H=im.size
    data=pytesseract.image_to_data(im,lang="chi_sim+eng",output_type=pytesseract.Output.DICT,config="--psm 11")
    t=(int(f[-8:-4])-1)/float(fps)
    words=[(data["text"][i],data["top"][i],data["height"][i],data["left"][i],data["width"][i]) for i in range(len(data["text"])) if data["text"][i].strip() and float(data["conf"][i])>55 and len(data["text"][i].strip())>=1]
    cj=[w for w in words if any('一'<=c<='鿿' for c in w[0])]
    for w in cj: rows[(w[1]//40)*40]+=1
    if cj: print(f"{t:5.1f}s", " | ".join(f"{w[0]}@y{w[1]}-{w[1]+w[2]} x{w[3]}" for w in cj[:6]))
print("Y-band histogram (CJK words, 40px bins, H=%d):"%H, sorted(rows.items()))
