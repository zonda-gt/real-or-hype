# usage: skymask.py model.onnx in.jpg out_mask.png  -> white = sky
import sys, numpy as np, onnxruntime as ort
from PIL import Image
_s = None
def sky_prob(img, model, size=640):
    global _s
    if _s is None:
        _s = ort.InferenceSession(model, providers=['CPUExecutionProvider'])
    W, H = img.size
    sw = size; sh = int(round(size * H / W / 32) * 32)
    x = np.asarray(img.convert('RGB').resize((sw, sh), Image.BICUBIC), np.float32) / 255.
    x = (x - [0.485, 0.456, 0.406]) / [0.229, 0.224, 0.225]
    x = x.transpose(2, 0, 1)[None].astype(np.float32)
    lg = _s.run(None, {'pixel_values': x})[0][0]
    e = np.exp(lg - lg.max(0)); p = e / e.sum(0)
    sky = p[2]  # ADE20K: 2 = sky
    return Image.fromarray((sky * 255).astype(np.uint8)).resize((W, H), Image.BILINEAR)
if __name__ == '__main__':
    m = sky_prob(Image.open(sys.argv[2]), sys.argv[1])
    m.save(sys.argv[3])
