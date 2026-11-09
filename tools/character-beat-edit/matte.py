import numpy as np, cv2, os
from scipy import ndimage
plate = np.load("plate.npy"); sup = np.load("support.npy")
fr = np.load("reel_frames.npy")[:, 40:600, 0:440]
s = cv2.GaussianBlur(sup, (0,0), 6)
core = s < 0.5
lab, n = ndimage.label(core); sizes = ndimage.sum(core, lab, range(1, n+1))
core = lab == (1 + sizes.argmax())
core = ndimage.binary_fill_holes(ndimage.binary_dilation(core, iterations=10))
pl = cv2.inpaint(plate.astype(np.uint8), core.astype(np.uint8)*255, 9, cv2.INPAINT_TELEA)
cv2.imwrite("chk/plate_inpaint.png", pl)
np.save("core.npy", core)
plab = cv2.cvtColor(pl, cv2.COLOR_BGR2LAB).astype(np.float32)
os.makedirs("alpha", exist_ok=True)
for i, f in enumerate(fr):
    fb = cv2.GaussianBlur(f, (3,3), 0)
    flab = cv2.cvtColor(fb, cv2.COLOR_BGR2LAB).astype(np.float32)
    d = np.sqrt(((flab - plab) ** 2).sum(-1))
    thr = np.where(core, 22, 26)
    fg = d > thr
    fg = ndimage.binary_opening(fg, iterations=1)
    lab, n = ndimage.label(fg)
    if n:
        sz = ndimage.sum(fg, lab, range(1, n+1))
        fg = np.isin(lab, 1 + np.where(sz >= 0.05 * sz.max())[0])
    fg = ndimage.binary_closing(fg, iterations=2)
    fg = ndimage.binary_fill_holes(fg)
    # soft edge: ramp of the colour distance in a 2px band around the hard matte
    band = ndimage.binary_dilation(fg, iterations=2) & ~ndimage.binary_erosion(fg, iterations=1)
    soft = np.clip((d - 10) / (thr - 10 + 12), 0, 1)
    a = np.where(band, soft, fg.astype(np.float32))
    a = cv2.GaussianBlur(a.astype(np.float32), (3,3), 0.6)
    cv2.imwrite(f"alpha/{i+1:04d}.png", (a*255).astype(np.uint8))
print("done", len(fr))
