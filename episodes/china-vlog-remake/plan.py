# slot cut times from the reference (beat-aligned at ~123 BPM)
CUTS = [0.0, 3.0, 3.467, 3.967, 5.433, 6.367, 7.8, 9.267, 10.233, 12.167, 14.067, 16.5, 17.433, 18.933, 20.333, 21.966]
# (clip id, source start seconds, speed factor (<1 = slow-mo), label)
SHOTS = [
    ('7536157470457695531', 5.0, 1.0, 'Guangzhou Canton Tower (title)'),
    ('7665079382855191854', 7.18, 0.86, 'Temple gate'),
    ('7243240214632680743', 8.3, 1.0, 'Teppanyaki flame'),
    ('7244825772140105016', 14.0, 1.0, 'Xitang lantern boats'),
    ('7572870227614518735', 3.0, 1.0, 'Guilin Li River raft'),
    ('7695357803590686646', 3.0, 1.0, 'Lizhuang ancient town sunset'),
    ('7449403524397485339', 0.0, 1.0, 'Steaming pot kitchen'),
    ('7701334294639540297', 0.5, 1.0, 'Potala Palace, Lhasa'),
    ('7703784750254877878', 8.0, 1.0, 'Park circle dance'),
    ('7685403242537289802', 0.0, 1.0, 'Jiuzhaigou autumn'),
    ('7690080863061851310', 10.0, 1.0, 'Zhangjiajie in mist'),
    ('7661513526356788462', 5.0, 1.0, 'Chongqing skyline'),
    ('7622310743648183110', 2.0, 1.0, 'Fish lanterns + fireworks'),
    ('7694273741970340721', 3.4, 1.0, 'Yangshuo golden hour'),
    ('7290578707402476837', 0.2, 1.0, 'Street life'),
]

HLG = {'7572870227614518735', '7703784750254877878', '7690080863061851310'}
# extra crop (zoom factor, anchor x 0..1, anchor y 0..1) to remove watermarks
CROP = {'7665079382855191854': (1.2, 1.0, 0.0)}
