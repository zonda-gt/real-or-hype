# Panlong Tiandi, video A2: A + AI host clip at the start and under the CTA
END = 28.38
EDL = [(0.0, 'V_host', 0.1), (1.75, 'A_night', 12.3), (3.74, 'C_autumn', 3.0, (1.15, 0.4, 0.4)), (4.56, 'K_flower', 7.5), (5.86, 'A_night', 6.3), (7.64, 'B_dusk', 4.5, (1.25, 0.5, 0.5)), (8.94, 'J_day', 10.05), (10.64, 'I_lotus', 36.1), (11.94, 'D_market', 8.0), (13.49, 'D_market', 37.5), (14.85, 'M_fuhebowl', 2.5, (1.4, 0.0, 0.5)), (15.5, 'L_fuhe', 6.0), (17.21, 'S_me_noodles', 0.5), (20.56, 'E_sunset', 2.5), (21.35, 'F_bluemkt', 0.3), (22.36, 'A_night', 24.3), (25.33, 'V_host', 1.95)]
TITLE = ("SHANGHAI'S", 'Water Town', '1,400 years old, on the metro', 0.0, 4.56, 'headline')
LABELS = [(5.86, 8.94, '700 years old', 540, 330, -3), (10.64, 11.94, '¥50 ≈ $7 boat ride', 540, 330, -3), (11.94, 14.85, 'Fri–Sun floating market', 540, 330, -3), (14.85, 17.21, 'Fuhe Noodles', 540, 330, -3), (19.12, 20.56, '¥36 ≈ $5 / bowl', 540, 1560, -3)]
PILLS = [(22.36, 25.22, ['Metro Line 17', 'Panlong Road · Exit 3'], 520)]
FOLLOW = (25.22, None)
FOLLOW_TEXT = ('COMMENT "WOW"', 'FOR MORE PLACES')
MUSIC = ('music/m3.mp3', 12.0, -11)
CAPTION_REPLACE = {'福和面馆': 'FUHE NOODLES'}
CAPTION_SKIP = [(0.0, 1.70), (25.15, 28.38)]   # host clip: headline carries the hook, face stays clear

def shots():
    out = []
    for i, e in enumerate(EDL):
        t0, src, inn = e[:3]
        t1 = EDL[i + 1][0] if i + 1 < len(EDL) else END
        z, ay, ax = e[3] if len(e) > 3 else (1.0, 0.5, 0.5)
        out.append(dict(i=i, t0=t0, dur=round(t1 - t0, 3), src=src, inn=inn, z=z, ay=ay, ax=ax))
    return out
TITLE_DY = -270   # keep the headline in the sky above the host's head
