# Baixiangju (白象居) straight recreation: segment list.
# Each segment: id, video shots [(clip, in, out, speed)], audio:
#   'talk'                         -> his own voice from the (single) shot, same range/speed, loudnormed
#   ('amb', vol)                   -> each shot's own sound at vol
#   ('vo', clip, in, out, speed)   -> his voice from another clip/range laid over the shots
# Subtitle lines: (seg id, exact text). Badges: (seg id, source time of the word, png).
SP = 1.3
S = [
 ('T1', [('IMG_2414', 7.12, 11.25, SP)], 'talk'),
 ('V1', [('IMG_2414', 14.6, 17.6, 1.0)], ('amb', 0.35)),
 ('T2', [('IMG_2414', 19.00, 24.05, SP)], 'talk'),
 ('D1', [('B:7416732680286489856', 0.4, 2.9, 1.0), ('VID_20261011_142543_023', 0.1, 2.2, 1.0)],
        ('vo', 'VID_20261011_140150_020', 42.00, 47.52, SP)),
 ('C1', [('VID_20261011_140150_020', 50.3, 51.5, 1.0), ('VID_20261011_140150_020', 57.0, 58.0, 1.0),
         ('VID_20261011_140150_020', 71.0, 72.2, 1.3), ('VID_20261011_140150_020', 104.4, 105.6, 1.3)], ('amb', 0.35)),
 ('T3', [('VID_20261011_140150_020', 109.40, 114.65, SP)], 'talk'),
 ('T4', [('VID_20261011_140150_020', 130.70, 137.40, SP)], 'talk'),
 ('W1', [('VID_20261011_140150_020', 143.0, 146.0, 1.5)], ('amb', 0.35)),
 ('T5', [('VID_20261011_140150_020', 154.40, 163.30, SP)], 'talk'),
 ('W2', [('VID_20261011_140543_022', 15.0, 17.0, 1.5)], ('amb', 0.35)),
 ('T6', [('VID_20261011_140543_022', 27.60, 35.60, SP)], 'talk'),
 ('T7', [('VID_20261011_140543_022', 40.36, 42.70, SP)], 'talk'),
 ('B1', [('VID_20261011_143016_026', 2.0, 4.6, 1.0)], ('amb', 0.1)),
 ('W3', [('VID_20261011_140543_022', 112.6, 116.5, 1.8)], ('amb', 0.35)),
 ('T8', [('VID_20261011_140543_022', 118.00, 124.05, SP)], 'talk'),
 ('T9', [('VID_20261011_140543_022', 129.80, 133.30, SP)], 'talk'),
 ('E1', [('B:7416732680286489856', 8.6, 11.6, 1.0)], ('amb', 0.0)),
]
LINES = [
 ('T1', "I thought we're at the ground floor of the building, but come check this out."),
 ('T2', "We're actually on the 10th floor of the building, guys. That's crazy!"),
 ('D1', "And this building is 22 floors, but they don't have a lift. So you have to walk all the way up."),
 ('T3', "Oh, this is tiring, guys. It's so tiring. Come, come, come, we're nearly there."),
 ('T4', "It's the 15th floor right now. We're at the 15th floor. So, climbed five floors right now."),
 ('T5', "Wait, what? What? Now it's the 14th floor. How does that make sense? We're just literally at the 15th floor just now and we didn't walk any stairs."),
 ('T6', "Wait, all of a sudden guys, we're on the 12th floor. What's going on? We're literally just on the 14th floor and now we're actually on the 12th floor, guys."),
 ('T7', "This is why Chongqing is called 8D city, guys."),
 ('T8', "Wait, look guys, all of a sudden we're actually on the ground floor again. Oh, we didn't climb any stairs, guys."),
 ('T9', "And where is the actual ground floor in this city?"),
]
# floor badge changes at the word (source time in that segment's clip)
BADGES = [('T2', 21.02, 'badge_10.png'), ('T4', 131.90, 'badge_15.png'), ('T5', 157.08, 'badge_14.png'),
          ('T6', 30.44, 'badge_12.png'), ('T8', 120.82, 'badge_1.png')]
TITLE = ('T1', 'T2')          # hook title shown from start of T1 to end of T2
ENDCARD = 'E1'
