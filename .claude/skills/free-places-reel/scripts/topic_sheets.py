"""Stack the per-clip 1 fps sheets of each topic into one tall image: topic_sheets.py SHEETDIR OUTDIR"""
import sys, os, glob, collections
from PIL import Image
sd, od = sys.argv[1], sys.argv[2]; os.makedirs(od, exist_ok=True)
g = collections.defaultdict(list)
for f in sorted(glob.glob(f'{sd}/*.jpg')): g[os.path.basename(f).split('_')[0]].append(f)
for k, fs in g.items():
    ims = [Image.open(f) for f in fs]; Wd = max(i.width for i in ims); Hd = sum(i.height for i in ims)
    s = Image.new('RGB', (Wd, Hd)); y = 0
    for i in ims: s.paste(i, (0, y)); y += i.height
    s.thumbnail((1920, 4400)); s.save(f'{od}/{k}.jpg', quality=80); print(k, len(fs))
