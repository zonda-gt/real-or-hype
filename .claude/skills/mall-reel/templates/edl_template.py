# Copy to <project>/edl.py and fill in. Times are seconds on the FINAL timeline, taken from vo/words.json word onsets.
# Real example: episodes/gatem_edl.py (GATE M, 66 s, 46 shots).
END = 0.0   # = last word end + ~0.6 s (the follow card holds)

# (t0 = onset of the word this shot belongs to, source clip name in src/ without .mp4, in-point in that clip[, crop])
# Optional crop = (zoom, anchor_y, anchor_x), kept ON the shot so it can't drift when shots are added or removed.
# zoom 1.4 with anchor_y 0.0 keeps the top 71% (drops captions burned in at 74-80%); letterboxed 720x1280 clips with
# 720x960 content: (1.3334, 0.5, 0.5); a corner watermark at ~80%: (1.5, 0.3, 0.5).
# A shot runs until the next t0. Aim for 0.7-2.0 s per shot, median ~1.4 s. One shot per phrase; a list gets one shot per item.
EDL = [
    (0.00, 'A_night', 0.5),
    # (19.61, 'N_rooftop', 7.25, (1.4, 0.0, 0.5)),   # crop example
]


TITLE = ('GATE M', 'West Bund Dream Center', 'in  Shanghai', 0.0, 3.15)   # line1, line2 (italic), line3, start, end
LABELS = [  # (start, end, text, centre_x, centre_y, angle) handwritten label on the shot that shows that spot
    # (19.61, 21.27, 'silo rooftop', 560, 520, -4),
]
PILLS = [   # (start, end, [lines], top_y) practical info, e.g. metro
    # (54.50, 57.43, ['Metro Line 11', 'Longyao Rd · Exit 4'], 520),
]
FOLLOW = (0.0, None)        # start of the follow card (= onset of "Follow"), None = until the end
MUSIC = ('music/bed.mp3', 6.0, -9)   # file, offset into the track (skip a quiet intro), level dB after -16 LUFS normalise
CAPTION_REPLACE = {'龙耀路': 'LONGYAO LU'}   # Chinese written for the voice -> Latin for the caption font


def shots():
    out = []
    for i, e in enumerate(EDL):
        t0, src, inn = e[:3]
        t1 = EDL[i + 1][0] if i + 1 < len(EDL) else END
        z, ay, ax = e[3] if len(e) > 3 else (1.0, 0.5, 0.5)
        out.append(dict(i=i, t0=t0, dur=round(t1 - t0, 3), src=src, inn=inn, z=z, ay=ay, ax=ax))
    return out
