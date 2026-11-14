# GATE M, angle 2: "one evening in Shanghai" plan (John v3). CTA: plan your trip.
END = 28.17
EDL = [
 (0.00, 'A_night', 0.5),                         # One evening in Shanghai? Spend it at Asia's biggest old
 (2.88, 'B_gatem', 34.6),                        # cement factory.   (lit silos)
 (3.66, 'B_gatem', 0.0),                         # It's called Gate M,   (sign)
 (4.61, 'A_night', 18.5),                        # on the West Bund.
 (5.42, 'M_sunset', 2.2, (1.3334, 0.5, 0.5)),    # Get there an hour before sunset,
 (6.81, 'R_gm', 27.3),                           # and start at Gentle Monster,
 (8.17, 'R_gm', 12.6), (8.86, 'R_gm', 13.62),    # full of giant face sculptures.
 (9.86, 'O_river', 3.24, (1.5, 0.3, 0.5)),       # Then grab a spot on the 800-meter riverfront
 (11.30, 'F_blue', 2.0),                         # for blue hour,
 (12.83, 'O_river', 0.1, (1.5, 0.3, 0.5)),       # looking out to Lupu Bridge.
 (14.22, 'I_silos', 7.2),                        # For dinner, head inside the old silos
 (16.15, 'Q_wilddock', 2.37),                    # to Wild Dock. Everything's grilled over apple-wood charcoal,  (logo -> grill -> dish)
 (18.81, 'V_me_wd', 0.6),                        # about 25 dollars per person, so book the river terrace ahead.  (AI clip: you eating)
 (21.92, 'S_dogs', 26.45),                       # It's free to walk around.
 (23.03, 'A_night', 42.0),                       # Take Line 11 to 龙耀路, exit 4.
 (25.52, 'U_me_river', 1.2)]                     # Comment WOW, and we'll plan your trip for you.  (AI clip: you wave)
TITLE = ('ONE EVENING IN', 'Shanghai', 'at an old cement factory', 0.0, 3.66, 'headline')
LABELS = [(6.81, 8.17, 'Gentle Monster', 540, 330, -3), (9.86, 11.30, '800m riverfront', 520, 640, -3),
          (11.30, 12.83, 'blue hour', 540, 520, -3), (12.83, 14.22, 'Lupu Bridge', 540, 420, -3),
          (16.15, 16.91, 'Wild Dock', 540, 1250, -4), (18.81, 21.92, '¥180 ≈ $25 / person', 540, 1560, -3)]
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
