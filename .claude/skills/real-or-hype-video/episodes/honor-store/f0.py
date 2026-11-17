import parselmouth,numpy as np,sys
def stats(f):
    s=parselmouth.Sound(f); p=s.to_pitch(time_step=0.01,pitch_floor=70,pitch_ceiling=400)
    f0=p.selected_array['frequency']; f0=f0[f0>0]
    st=12*np.log2(f0/np.median(f0))
    return np.std(st), np.percentile(st,95)-np.percentile(st,5)
if __name__=='__main__':
    for f in sys.argv[1:]:
        sd,rg=stats(f); print(f'{f:40s} pitch sd {sd:4.2f} st, range {rg:4.1f} st')
