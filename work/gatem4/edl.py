# Re-timed from ../gatem3 by revoice.py for a new narration.
END = 33.08
EDL = [(0.0, 'A_night', 0.5),
 (2.951, 'B_gatem', 0.0),
 (3.858, 'A_night', 18.5),
 (5.145, 'K_aerial1', 12.0),
 (6.012, 'S_dogs', 15.2),
 (7.146, 'S_dogs', 9.3),
 (9.535, 'I_silos', 7.2),
 (10.724, 'Q_wilddock', 2.37),
 (11.659, 'Q_wilddock', 2.92),
 (13.951, 'Q_wilddock', 5.5),
 (14.816, 'Q_wilddock', 0.4),
 (15.857, 'R_gm', 27.3),
 (18.044, 'R_gm', 12.6),
 (18.894, 'R_gm', 13.65),
 (19.801, 'O_river', 3.24, (1.5, 0.3, 0.5)),
 (21.234, 'O_river', 0.1, (1.5, 0.3, 0.5)),
 (22.499, 'F_blue', 0.12),
 (24.021, 'M_sunset', 2.2, (1.3334, 0.5, 0.5)),
 (25.009, 'S_dogs', 26.45),
 (26.16, 'A_night', 42.0),
 (28.583, 'A_night', 51.5),
 (30.516, 'B_gatem', 38.3)]
TITLE = ('GATE M', 'West Bund Dream Center', 'in  Shanghai', 0.0, 2.934)
LABELS = [(6.012, 7.146, 'dog-friendly', 540, 560, -4),
 (10.724, 11.659, 'Wild Dock', 540, 1150, -4),
 (13.951, 15.857, '¥180 ≈ $25 / person', 540, 560, -3),
 (15.857, 18.044, 'Gentle Monster', 540, 330, -3),
 (19.801, 21.234, '800m riverfront', 520, 640, -3),
 (21.234, 22.499, 'Lupu Bridge', 540, 420, -3),
 (28.583, 30.516, 'walk to Tank Shanghai', 540, 640, -3)]
PILLS = [(26.16, 28.583, ['Metro Line 11', 'Longyao Rd · Exit 4'], 520)]
FOLLOW = (30.516, None)
MUSIC = ('music/m3.mp3', 12.0, -11)
CAPTION_REPLACE = {'龙耀路': 'LONGYAO LU'}

def shots():
    out=[]
    for i,e in enumerate(EDL):
        t0,src,inn=e[:3]
        t1=EDL[i+1][0] if i+1<len(EDL) else END
        z,ay,ax=e[3] if len(e)>3 else (1.0,0.5,0.5)
        out.append(dict(i=i,t0=t0,dur=round(t1-t0,3),src=src,inn=inn,z=z,ay=ay,ax=ax))
    return out
FOLLOW_TEXT = ('COMMENT "WOW"', 'WE PLAN YOUR TRIP')
