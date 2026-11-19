# Cinematic "teal & orange" travel grade (modelled on DJI's Osmo Action 5 Pro colour-grade short), applied on top of an
# existing HLG->SDR cube so one LUT does both. usage: grade_lut.py in.cube out.cube [strength=1.0]
# Steps on display-referred R'G'B' (0..1): black point + S-curve with darker mids, hue-preserving luma remap,
# split toning (teal-blue shadows, golden highlights, a little orange in the mids), saturation boost with a soft clip.
import sys,numpy as np
src,dst=sys.argv[1],sys.argv[2]; K=float(sys.argv[3]) if len(sys.argv)>3 else 1.0
hdr=[];vals=[]
for line in open(src):
    t=line.split()
    if len(t)==3 and all(c.replace('.','',1).replace('-','',1).replace('e','',1).isdigit() for c in t): vals.append([float(x) for x in t])
    else: hdr.append(line)
rgb=np.array(vals)
W=np.array([0.2126,0.7152,0.0722])
Y=rgb@W
# tone curve on luma
y1=np.clip((Y-0.035*K)/(1-0.035*K),0,1)                 # deeper black point
y2=y1**(1+0.22*K)                                       # darker midtones
c=1+1.3*K; y3=0.5+0.5*np.tanh(c*(y2-0.5))/np.tanh(c*0.5) # S-curve contrast
y3=0.92*y3+0.08*y2*(y3>0.9)+0.0                         # gentle shoulder
r=np.where(Y>1e-4,y3/np.maximum(Y,1e-4),0)[:,None]
out=rgb*r
# keep highlights from blowing out channel-wise: soft clip toward luma
mx=out.max(1,keepdims=True); over=np.clip(mx-1,0,None); Yo=out@W
out=np.where(mx>1,Yo[:,None]+(out-Yo[:,None])/(1+over*2),out)
Yo=np.clip(out@W,0,1)
ws=(1-Yo)**2.2; wh=Yo**2.0; wm=4*Yo*(1-Yo)
out=out+K*(ws[:,None]*np.array([-0.030,0.004,0.038])+wh[:,None]*np.array([0.030,0.010,-0.032])+wm[:,None]*np.array([0.012,0.002,-0.012]))
# saturation
Yo=out@W; out=Yo[:,None]+(out-Yo[:,None])*(1+0.28*K)
out=np.clip(out,0,1)
with open(dst,'w') as f:
    f.write(''.join(hdr).replace('HLG to SDR BT.2446A','HLG to SDR BT.2446A + cinematic teal-orange grade'))
    np.savetxt(f,out,fmt='%.6f')
print('graded lut',dst,'strength',K)
