import numpy as np, cv2, json, librosa
fr = np.load("reel_frames.npy")[:, 40:600, 0:440].astype(np.float32)
al = np.stack([cv2.imread(f"alpha/{i+1:04d}.png",0) for i in range(len(fr))]).astype(np.float32)/255
# motion energy of the character: frame difference inside the (dilated) character area
mot = np.array([0]+[ (np.abs(fr[i]-fr[i-1]).mean(-1)*np.maximum(al[i],al[i-1])).sum()/1e4 for i in range(1,len(fr))])
cy = np.array([ (al[i]*np.arange(560)[:,None]).sum()/al[i].sum() for i in range(len(fr))])   # body height (bounce)
t = np.arange(len(fr))/30
np.save("dance_mot.npy", mot); np.save("dance_cy.npy", cy)
for name, sig in [("motion", mot), ("vertical bounce", cy - cv2.GaussianBlur(cy.reshape(-1,1),(1,31),0).ravel())]:
    s = sig - sig.mean(); ac = np.correlate(s, s, "full")[len(s)-1:]; ac/=ac[0]
    lags = np.arange(len(ac))/30
    m=(lags>0.25)&(lags<3)
    pk=[i for i in np.where(m)[0] if ac[i]>ac[i-1] and ac[i]>=ac[i+1] and ac[i]>0.1]
    print(name, "autocorr peaks (s, r):", [(round(lags[i],3), round(ac[i],2)) for i in pk][:8])
# motion peaks = dance hits
pk = [i for i in range(2,len(mot)-2) if mot[i]==mot[i-2:i+3].max() and mot[i]>np.percentile(mot,70)]
print("dance hit times:", np.round(t[pk],2).tolist())
json.dump(t[pk].tolist(), open("dance_hits.json","w"))
