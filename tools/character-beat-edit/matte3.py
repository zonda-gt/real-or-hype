import numpy as np, cv2, os
from scipy import ndimage
fr = np.load("reel_frames.npy")[:, 40:600, 0:440]
n, h, w, _ = fr.shape
plate_mode = np.load("plate.npy"); core = np.load("core.npy")
A = np.stack([cv2.imread(f"alpha1/{i+1:04d}.png", 0) for i in range(n)]) > 10
A = np.stack([ndimage.binary_dilation(a, iterations=14) for a in A])          # very conservative
vis = ~A
cnt = vis.sum(0)
plate = plate_mode.astype(np.float32).copy()
ok = core & (cnt >= 25)
std_ok = np.zeros_like(ok)
for c in range(3):
    v = np.where(vis, fr[..., c].astype(np.float32), np.nan)
    med = np.nanmedian(v[:, ok], axis=0); sd = np.nanstd(v[:, ok], axis=0)
    plate[..., c][ok] = med
    std_ok_c = np.zeros_like(ok); std_ok_c[ok] = sd < 18
    std_ok = std_ok_c if c == 0 else (std_ok & std_ok_c)
known = (~core) | (ok & std_ok)
hole = ~known
pl = cv2.inpaint(plate.astype(np.uint8), hole.astype(np.uint8) * 255, 7, cv2.INPAINT_TELEA)
cv2.imwrite("chk/plate3.png", pl)
print("core px", core.sum(), "recovered", (core & known).sum(), "still unknown", hole.sum())
plab = cv2.cvtColor(pl, cv2.COLOR_BGR2LAB).astype(np.float32); pf = pl.astype(np.float32) + 1
# watermark: static text in the plate area at bottom-left -> never foreground
wm = np.zeros((h, w), bool); wm[425:455, 0:75] = True
for i, f in enumerate(fr):
    fb = cv2.GaussianBlur(f, (3, 3), 0)
    flab = cv2.cvtColor(fb, cv2.COLOR_BGR2LAB).astype(np.float32)
    d = np.sqrt(((flab - plab) ** 2).sum(-1))
    thr = np.where(known, 26, 22)
    fg = d > thr
    r = (fb.astype(np.float32) + 1) / pf
    shadow = known & (r.std(-1) < 0.07) & (r.mean(-1) > 0.35) & (r.mean(-1) < 0.97)
    fg &= ~shadow
    fg &= ~(wm & (d < 70))
    fg = ndimage.binary_opening(fg, iterations=1)
    lab, k = ndimage.label(fg)
    if k:
        sz = ndimage.sum(fg, lab, range(1, k + 1))
        fg = np.isin(lab, 1 + np.where(sz >= 0.05 * sz.max())[0])
    fg = ndimage.binary_closing(fg, iterations=2)
    fg = ndimage.binary_fill_holes(fg)
    fg = ndimage.binary_opening(fg, iterations=2)          # drop thin slivers
    band = ndimage.binary_dilation(fg, iterations=2) & ~ndimage.binary_erosion(fg, iterations=1)
    soft = np.clip((d - 10) / (thr - 10 + 12), 0, 1) * ~shadow
    a = np.where(band, soft * ndimage.binary_dilation(fg, iterations=2), fg.astype(np.float32))
    a = cv2.GaussianBlur(a.astype(np.float32), (3, 3), 0.6)
    cv2.imwrite(f"alpha/{i+1:04d}.png", (a * 255).astype(np.uint8))
print("done")
