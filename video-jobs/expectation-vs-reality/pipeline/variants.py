# Segment lists. Each seg: clip id, in point, min dur, tag (kind, label, sub), vo key (or None), sfx list
# kinds: online (yellow), real (red), fix (green), none
BUND_DREAM='7639581892485180059'; BUND_GW='7691696825632647355'; BUND_SUMMER='7663904546812425423'; BUND_5AM='7657542861315213541'
WK_UP='7684819445881937024'; WK_CROWD='7673651777053333113'; WK_EMPTY='7664352836336464613'
HYD_DREAM='7672366988765931195'; HYD_CROWD='7676478856703111562'; HYD_RIVER='7684303159230392179'; HYD_GROUND='7697608326519121225'
GW_CLOUD='7668986182978084965'; GW_BDL='7656712949243781859'; GW_SUN='7672603817116028214'; GW_BDL2='7671173444927695862'; BUND_HIGH='7666811861115543985'

def S(clip,t,dur=0,tag=None,vo=None,sfx=(),big=None,pad=0.22,z=1.0,ax=0.5,ay=0.5,band=False):
    return dict(clip=clip,t=t,dur=dur,tag=tag,vo=vo,sfx=list(sfx),big=big,pad=pad,z=z,ax=ax,ay=ay,band=band)

V={}
V['A']=[
 S(BUND_DREAM,3.0,tag=('online','ONLINE','The Bund, Shanghai'),vo='A_hook1'),
 S(BUND_GW,9.4,dur=1.15,tag=('real','REAL LIFE','The Bund, Golden Week'),vo='A_hook2',sfx=['buzz']),
 S(GW_BDL2,0.0,dur=0.1,tag=('real','REAL LIFE','Great Wall, summer'),vo=None,pad=0),
 S(BUND_HIGH,6.9,band=True,tag=('real','REAL LIFE','The Bund, summer holidays'),vo='A_bund1'),
 S(BUND_5AM,2.0,dur=1.7,tag=('fix','DO THIS','Early morning, weekday'),vo='A_bund2',sfx=['ding']),
 S(BUND_5AM,6.0,dur=0.1,tag=('fix','DO THIS','Early morning, weekday'),vo=None,pad=0),
 S(WK_UP,26.6,tag=('online','ONLINE','Wukang Mansion, Shanghai'),vo='A_wk1',sfx=['whoosh']),
 S(WK_CROWD,14.6,z=1.25,ax=0.6,ay=0.0,tag=('real','REAL LIFE','Wukang Mansion'),vo='A_wk2',sfx=['buzz']),
 S(WK_EMPTY,6.0,tag=('fix','DO THIS','Before 8 a.m.'),vo='A_wk3',sfx=['ding']),
 S(HYD_DREAM,11.4,tag=('online','ONLINE','Hongyadong, Chongqing'),vo='A_hyd1',sfx=['whoosh']),
 S(HYD_CROWD,0.5,tag=('real','REAL LIFE','Hongyadong, August'),vo='A_hyd2',sfx=['buzz']),
 S(HYD_RIVER,0.3,tag=('fix','DO THIS','From the river'),vo='A_hyd3',sfx=['ding']),
 S(GW_CLOUD,0.3,tag=('online','ONLINE','The Great Wall'),vo='A_gw1',sfx=['whoosh']),
 S(GW_BDL,0.1,tag=('real','REAL LIFE','Badaling'),vo='A_gw2',sfx=['buzz']),
 S(GW_SUN,3.6,tag=('fix','DO THIS','Jinshanling'),vo='A_gw3',sfx=['ding']),
 S(BUND_5AM,16.9,dur=1.5,tag=None,vo='A_end',big='SPOTS',pad=0.7),
 S(GW_SUN,14.0,dur=0.1,tag=None,vo=None,big='SPOTS',pad=0),
]
V['B']=[
 S(GW_CLOUD,0.3,tag=('online','ONLINE','The Great Wall'),vo='B_hook1',big='SCAM'),
 S(GW_BDL,0.2,tag=('real','REAL LIFE','Badaling'),vo='B_hook2',sfx=['buzz']),
 S(GW_SUN,0.0,tag=('online','ONLINE','The Great Wall'),vo='B_gw1',sfx=['whoosh']),
 S(GW_BDL2,2.6,tag=('real','REAL LIFE','Badaling'),vo='B_gw2',sfx=['buzz']),
 S(GW_SUN,3.6,tag=('fix','TRICK 1','Go to Jinshanling'),vo='B_gw3',sfx=['ding']),
 S(BUND_DREAM,3.0,tag=('online','ONLINE','The Bund, Shanghai'),vo='B_bund1',sfx=['whoosh']),
 S(BUND_HIGH,6.9,band=True,tag=('real','REAL LIFE','The Bund, summer'),vo='B_bund2',sfx=['buzz']),
 S(BUND_5AM,2.0,dur=1.7,tag=('fix','TRICK 2','Sunrise'),vo='B_bund3',sfx=['ding']),
 S(BUND_5AM,6.0,dur=0.1,tag=('fix','TRICK 2','Sunrise'),vo=None,pad=0),
 S(WK_EMPTY,5.0,tag=('online','ONLINE','Wukang Mansion, Shanghai'),vo='B_wk1',sfx=['whoosh']),
 S(WK_CROWD,14.6,z=1.25,ax=0.6,ay=0.0,tag=('real','REAL LIFE','Wukang Mansion'),vo='B_wk2',sfx=['buzz']),
 S(WK_UP,26.6,tag=('fix','TRICK 3','Before 8 a.m.'),vo='B_wk3',sfx=['ding']),
 S(HYD_DREAM,11.4,tag=('online','ONLINE','Hongyadong, Chongqing'),vo='B_hyd1',sfx=['whoosh']),
 S(HYD_GROUND,3.7,tag=('real','REAL LIFE','Hongyadong'),vo='B_hyd2',sfx=['buzz']),
 S(HYD_RIVER,0.3,tag=('fix','TRICK 4','From the river'),vo='B_hyd3',sfx=['ding']),
 S(BUND_5AM,16.9,dur=1.5,tag=None,vo='B_end',big='SPOTS',pad=0.7),
 S(GW_SUN,14.0,dur=0.1,tag=None,vo=None,big='SPOTS',pad=0),
]
V['C']=[
 S(BUND_DREAM,3.0,dur=1.4,tag=('online','ONLINE','The Bund'),vo='C_hook1'),
 S(GW_CLOUD,0.3,dur=0.1,tag=('online','ONLINE','The Great Wall'),vo=None,pad=0),
 S(BUND_GW,9.4,dur=1.0,tag=('real','REAL LIFE','The Bund'),vo='C_hook2',sfx=['buzz']),
 S(WK_CROWD,14.6,z=1.25,ax=0.6,ay=0.0,dur=0.9,tag=('real','REAL LIFE','Wukang Mansion'),vo=None,pad=0),
 S(HYD_CROWD,1.0,dur=0.9,tag=('real','REAL LIFE','Hongyadong'),vo=None,pad=0),
 S(GW_BDL,0.4,dur=1.0,tag=('real','REAL LIFE','Great Wall, Badaling'),vo=None,pad=0),
 S(GW_BDL,1.4,dur=1.3,tag=None,vo='C_real',big='REAL',sfx=['whoosh'],pad=0.3),
 S(BUND_5AM,2.0,dur=1.7,tag=('fix','RIGHT TIME','The Bund, sunrise'),vo='C_bund',sfx=['ding']),
 S(BUND_5AM,6.0,dur=0.7,tag=('fix','RIGHT TIME','The Bund, sunrise'),vo=None,pad=0),
 S(WK_EMPTY,5.0,dur=2.6,tag=('fix','RIGHT TIME','Wukang, before 8 a.m.'),vo='C_wk',sfx=['ding']),
 S(HYD_RIVER,0.3,dur=2.6,tag=('fix','RIGHT SPOT','Hongyadong, from the river'),vo='C_hyd',sfx=['ding']),
 S(GW_CLOUD,0.8,dur=2.6,tag=('fix','RIGHT SPOT','Great Wall, Jinshanling'),vo='C_gw',sfx=['ding']),
 S(GW_SUN,14.0,dur=2.3,tag=None,vo='C_end',big='SPOTS',pad=0.7),
 S(HYD_DREAM,11.4,dur=0.1,tag=None,vo=None,big='SPOTS',pad=0),
]
