# Soft dark shade behind the CTA block (no blur version): elliptical, feathered, ~50% at the centre.
import os, sys, numpy as np
from PIL import Image
here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, here)
from cta_v import CENTER_Y
W, H = 1080, 1920
y, x = np.mgrid[0:H, 0:W].astype(np.float32)
d = np.sqrt(((x - W / 2) / 660) ** 2 + ((y - CENTER_Y) / 360) ** 2)
alpha = np.clip(1 - d, 0, 1) ** 1.5 * 0.7
img = np.zeros((H, W, 4), np.uint8); img[..., 3] = (alpha * 255).astype(np.uint8)
Image.fromarray(img, 'RGBA').save(f"{here}/{os.environ.get('LABELDIR', 'labels_v')}/scrim.png"); print('max alpha', alpha.max())
