# Re-timed from ../gatem4 by revoice.py for a new narration.
END = 32.08
EDL = [(0.0, 'A_night', 0.5),        # Shanghai turned Asia's biggest cement factory   (headline on screen)
 (2.34, 'B_gatem', 34.6),             # into this.   (reveal: the lit silos)
 (3.08, 'B_gatem', 0.0),              # It's called Gate M,
 (4.09, 'A_night', 18.5),             # the West Bund Dream Center,
 (5.51, 'K_aerial1', 12.0),
 (6.439, 'S_dogs', 15.2),
 (7.787, 'S_dogs', 9.3),
 (10.013, 'I_silos', 7.2),
 (10.936, 'Q_wilddock', 2.37),
 (12.074, 'Q_wilddock', 2.92),
 (14.431, 'Q_wilddock', 5.5),
 (15.091, 'Q_wilddock', 0.4),
 (15.947, 'R_gm', 27.3),
 (18.071, 'R_gm', 12.6),
 (18.892, 'R_gm', 13.65),
 (19.871, 'O_river', 3.24, (1.5, 0.3, 0.5)),
 (21.018, 'O_river', 0.1, (1.5, 0.3, 0.5)),
 (22.283, 'F_blue', 0.12),
 (23.579, 'M_sunset', 2.2, (1.3334, 0.5, 0.5)),
 (24.436, 'S_dogs', 26.45),
 (25.458, 'A_night', 42.0),
 (27.724, 'A_night', 51.5),
 (29.679, 'U_me_river', 1.53)]   # AI clip (Seedance 2.5): you turn, smile, wave
TITLE = ("SHANGHAI'S", 'Cement Factory', 'turned riverside hangout', 0.0, 3.08, 'headline')
LABELS = [(6.439, 7.787, 'dog-friendly', 540, 560, -4),
 (10.936, 12.074, 'Wild Dock', 540, 1150, -4),
 (14.431, 15.947, '¥180 ≈ $25 / person', 540, 560, -3),
 (15.947, 18.071, 'Gentle Monster', 540, 330, -3),
 (19.871, 21.018, '800m riverfront', 520, 640, -3),
 (21.018, 22.283, 'Lupu Bridge', 540, 420, -3),
 (27.724, 29.679, 'walk to Tank Shanghai', 540, 640, -3)]
PILLS = [(25.458, 27.724, ['Metro Line 11', 'Longyao Rd · Exit 4'], 520)]
FOLLOW = (29.679, None)
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
CAPTION_SKIP = [(3.0, 4.05)]   # 'It's called Gate M' over the GATE M sign
CAPTION_SKIP = CAPTION_SKIP + [(29.58, 32.08)]   # CTA: sticker says it; captions would cover the face
