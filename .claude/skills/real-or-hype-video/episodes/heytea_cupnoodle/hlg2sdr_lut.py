# HLG (BT.2100, BT.2020 primaries) -> SDR BT.709 3D LUT using ITU-R BT.2446-1 Method A tone mapping.
# Input to the LUT: full-range R'G'B' HLG signal (BT.2020).  Output: full-range R'G'B' BT.709 / BT.1886 (gamma 2.4).
# usage: hlg2sdr_lut.py out.cube [N=65] [exposure=1.0]
import sys,numpy as np
out=sys.argv[1]; N=int(sys.argv[2]) if len(sys.argv)>2 else 65; EXP=float(sys.argv[3]) if len(sys.argv)>3 else 1.0
a,b,c=0.17883277,0.28466892,0.55991073
def hlg_inv_oetf(e):
    e=np.clip(e,0,1); return np.where(e<=0.5,e*e/3,(np.exp((e-c)/a)+b)/12)
Lw,gam=1000.0,1.2
g=np.linspace(0,1,N); B,G,R=np.meshgrid(g,g,g,indexing='ij')   # cube order: R fastest
rgb=np.stack([R,G,B],-1).reshape(-1,3)
E=hlg_inv_oetf(rgb)                                   # scene linear
Ys=E@np.array([0.2627,0.6780,0.0593])
disp=(Ys[:,None]**(gam-1))*E*EXP                      # display linear, 1.0 = Lw (1000 nit)
disp=np.clip(disp,0,1)
# --- BT.2446 Method A ---
P=disp**(1/2.4); Yp=P@np.array([0.2627,0.6780,0.0593])
rh=1+32*(Lw/10000)**(1/2.4); Ypp=np.log1p((rh-1)*Yp)/np.log(rh)
Yc=np.where(Ypp<=0.7399,1.0770*Ypp,np.where(Ypp<0.9909,-1.1510*Ypp**2+2.7811*Ypp-0.6302,0.5*Ypp+0.5))
rs=1+32*(100/10000)**(1/2.4); Ysdr=(rs**Yc-1)/(rs-1)
Cb=(P[:,2]-Yp)/1.8814; Cr=(P[:,0]-Yp)/1.4746
f=np.where(Yp>0,Ysdr/(1.1*np.maximum(Yp,1e-6)),1.0)
Cbt,Crt=f*Cb,f*Cr; Yt=Ysdr-np.maximum(0.1*Crt,0)
Rn=Yt+1.4746*Crt; Bn=Yt+1.8814*Cbt; Gn=(Yt-0.2627*Rn-0.0593*Bn)/0.6780
sdr2020=np.clip(np.stack([Rn,Gn,Bn],-1),0,1)**2.4    # linear, BT.2020 primaries
M=np.array([[1.6605,-0.5876,-0.0728],[-0.1246,1.1329,-0.0083],[-0.0182,-0.1006,1.1187]])
lin709=np.clip(sdr2020@M.T,0,1)
o=lin709**(1/2.4)
with open(out,'w') as fh:
    fh.write(f'TITLE "HLG to SDR BT.2446A"\nLUT_3D_SIZE {N}\nDOMAIN_MIN 0 0 0\nDOMAIN_MAX 1 1 1\n')
    np.savetxt(fh,o,fmt='%.6f')
print('lut',out)
