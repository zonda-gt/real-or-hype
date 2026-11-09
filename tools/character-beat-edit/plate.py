import numpy as np, cv2
fr = np.load("reel_frames.npy")[:, 40:600, 0:440]          # same crop as frames/
n,h,w,_ = fr.shape
q = (fr >> 4).astype(np.int32)
code = (q[...,0] << 8) | (q[...,1] << 4) | q[...,2]          # (n,h,w)
plate = np.zeros((h,w,3), np.float32); support = np.zeros((h,w), np.float32)
for y in range(h):
    c = code[:, y, :]                                        # (n,w)
    for x in range(w):
        vals, cnt = np.unique(c[:, x], return_counts=True)
        m = vals[cnt.argmax()]
        sel = c[:, x] == m
        plate[y, x] = np.median(fr[sel, y, x], axis=0)
        support[y, x] = sel.mean()
np.save("plate.npy", plate); np.save("support.npy", support)
cv2.imwrite("chk/plate.png", plate.astype(np.uint8))
cv2.imwrite("chk/support.png", (support*255).astype(np.uint8))
print("support pct<0.1:", (support<0.1).mean(), "<0.2:", (support<0.2).mean())
