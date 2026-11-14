# GATE M, angle 2 (re-cut, gatem6b): "one evening in Shanghai" plan (John v3). CTA: plan your trip.
END = 28.17
EDL = [   # re-cut with footage video 1 does NOT use, different order
 (0.00, 'F_blue', 6.0),                          # One evening in Shanghai?   (blue-hour terrace)
 (1.24, 'A_night', 30.0),                        # Spend it at Asia's biggest old
 (2.88, 'I_silos', 12.8),                        # cement factory.   (silos by day)
 (3.66, 'K_aerial1', 7.0),                       # It's called Gate M,   (GATE M letters on the roof, aerial)
 (4.61, 'A_night', 11.0),                         # on the West Bund.
 (5.42, 'O_river', 10.6, (1.5, 0.3, 0.5)),       # Get there an hour before sunset,
 (6.81, 'R_gm', 18.4),                           # and start at Gentle Monster,   (store interior)
 (7.55, 'R_gm', 13.65), (8.75, 'R_gm', 12.4),    # full of giant face sculptures.   (close first, then wide)
 (9.86, 'I_silos', 5.3, (1.3334, 0.5, 0.5)),     # Then grab a spot on the 800-meter riverfront   (pink umbrellas)
 (11.30, 'F_blue', 4.2),                         # for blue hour,
 (12.83, 'O_river', 1.75, (1.5, 0.3, 0.5)),      # looking out to Lupu Bridge.   (bench, bridge)
 (14.22, 'T_wdsign', 52.65, (1.6, 0.0, 0.5)),    # For dinner, head inside the old silos   (Wild Dock interior)
 (15.85, 'T_wdsign', 6.76, (1.6, 0.0, 0.1)),     # to Wild Dock.   (neon sign)
 (16.91, 'T_wdsign', 7.86, (1.6, 0.0, 0.5)),     # Everything's grilled   (roast meats)
 (17.86, 'Q_wilddock', 8.57),                    # over apple-wood charcoal,   (dish)
 (18.81, 'V_me_wd', 0.6),                        # about 25 dollars per person, so book the river terrace ahead.  (AI: you eating)
 (21.92, 'S_dogs', 29.3),                        # It's free to walk around.
 (23.03, 'J_escal', 8.3),                        # Take Line 11 to 龙耀路, exit 4.
 (25.52, 'U_me_river', 1.2)]                     # Comment WOW, and we'll plan your trip for you.  (AI: you wave)
TITLE = ('ONE EVENING IN', 'Shanghai', 'at an old cement factory', 0.0, 3.66, 'headline')
LABELS = [(6.81, 8.17, 'Gentle Monster', 540, 330, -3), (9.86, 11.30, '800m riverfront', 520, 640, -3),
          (11.30, 12.83, 'blue hour', 540, 520, -3), (12.83, 14.22, 'Lupu Bridge', 540, 420, -3),
          (18.81, 21.92, '¥180 ≈ $25 / person', 540, 1560, -3)]
PILLS = [(23.03, 25.52, ['Metro Line 11', 'Longyao Rd · Exit 4'], 520)]
FOLLOW = (25.52, None)
FOLLOW_TEXT = ('COMMENT "WOW"', 'WE PLAN YOUR TRIP')
MUSIC = ('music/m3.mp3', 12.0, -11)
CAPTION_REPLACE = {'龙耀路': 'LONGYAO LU'}
CAPTION_SKIP = [(3.6, 4.6), (25.45, 28.17)]   # GATE M sign shot; CTA (sticker says it, face stays clear)

def shots():
    out = []
    for i, e in enumerate(EDL):
        t0, src, inn = e[:3]
        t1 = EDL[i + 1][0] if i + 1 < len(EDL) else END
        z, ay, ax = e[3] if len(e) > 3 else (1.0, 0.5, 0.5)
        out.append(dict(i=i, t0=t0, dur=round(t1 - t0, 3), src=src, inn=inn, z=z, ay=ay, ax=ax))
    return out
