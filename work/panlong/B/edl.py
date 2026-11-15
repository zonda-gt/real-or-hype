# Panlong Tiandi, video B
END = 25.53
EDL = [(0.0, 'P_sky', 1.5), (1.23, 'C_autumn', 21.0, (1.15, 0.4, 0.4)), (2.91, 'J_day', 0.5), (4.87, 'C_autumn', 6.5, (1.15, 0.4, 0.4)), (6.11, 'G_xmas', 8.0), (7.59, 'F_bluemkt', 4.5), (8.72, 'O_lotusmkt', 12.3), (9.83, 'K_flower', 10.8), (11.0, 'B_dusk', 10.6, (1.25, 0.5, 0.5)), (11.84, 'D_market', 20.0), (13.13, 'D_market', 34.0), (14.75, 'N_fishboat', 8.3), (16.66, 'F_bluemkt', 12.3), (18.24, 'U_dog', 22.3), (19.84, 'H_perform', 5.5), (22.81, 'T_me_boat', 1.28)]
TITLE = ('NO NEED TO LEAVE', 'Shanghai', 'for a water town', 0.0, 2.91, 'headline')
LABELS = [(9.83, 11.0, 'covered bridge', 540, 330, -3), (11.0, 11.84, '¥50 ≈ $7 boat ride', 540, 330, -3), (11.84, 14.75, 'weekend floating market', 540, 330, -3), (14.75, 16.66, 'yakitori · Niaoxun', 540, 330, -3), (16.66, 18.24, '¥142 ≈ $20 / person', 540, 1500, -3), (18.24, 19.84, 'pet-friendly', 540, 330, -3)]
PILLS = [(19.84, 22.81, ['Metro Line 17', 'Panlong Road · Exit 3'], 520)]
FOLLOW = (22.81, None)
FOLLOW_TEXT = ('COMMENT "WOW"', 'WE PLAN YOUR TRIP')
MUSIC = ('music/m3.mp3', 30.0, -11)
CAPTION_REPLACE = {'福和面馆': 'FUHE NOODLES'}
CAPTION_SKIP = [(22.74, 25.53)]

def shots():
    out = []
    for i, e in enumerate(EDL):
        t0, src, inn = e[:3]
        t1 = EDL[i + 1][0] if i + 1 < len(EDL) else END
        z, ay, ax = e[3] if len(e) > 3 else (1.0, 0.5, 0.5)
        out.append(dict(i=i, t0=t0, dur=round(t1 - t0, 3), src=src, inn=inn, z=z, ay=ay, ax=ax))
    return out
