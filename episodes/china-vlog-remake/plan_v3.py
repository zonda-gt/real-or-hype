# Third version (9:16): same beat-aligned cuts as the reference, all-new vertical footage and places
from plan import CUTS
SHOTS = [
    ('7653502221975553700', 4.5, 1.0, 'Tianjin Haihe skyline (title)'),
    ('7157901764602219780', 0.5, 1.0, 'Lingyin Temple gate'),
    ('7665280277241083290', 9.3, 1.0, 'Chongqing hotpot'),
    ('7677181612211669480', 5.0, 1.0, 'Zhouzhuang at night'),
    ('7681615917277183296', 0.5, 1.0, 'Wuzhen canal boats'),
    ('7689364074672443983', 0.3, 1.0, 'Hongcun reflections'),
    ('7674800814074880433', 0.5, 1.0, 'Rice rolls (cheung fun)'),
    ('7677215030135622769', 3.6, 1.0, 'Leshan Giant Buddha'),
    ('7700945103372760802', 3.0, 1.0, 'Tai chi in the park'),
    ('7651124068234408945', 1.0, 1.0, 'Lushan cloud waterfall'),
    ('7498126295269051660', 2.0, 1.0, 'Hanging Temple'),
    ('7673808798214458283', 0.5, 1.0, 'Yingwuzhou Bridge, Wuhan'),
    ('7598481496160946597', 0.1, 1.0, 'Datang Everbright City'),
    ('7662185926873634801', 1.5, 1.0, 'Chaka salt lake'),
    ('7673533308890894065', 0.2, 1.0, 'Yulin Road, Chengdu'),
]
HLG = {'7700945103372760802', '7673533308890894065', '7674800814074880433'}
PRECROP = {'7665280277241083290': '2160:2888:0:480', '7677215030135622769': '1080:1736:0:92'}  # remove letterbox bars
CROP = {}
LABELS = {
    1: ('LINGYIN TEMPLE', 'HANGZHOU'),
    3: ('ZHOUZHUANG', 'JIANGSU'),
    4: ('WUZHEN', 'ZHEJIANG'),
    5: ('HONGCUN', 'ANHUI'),
    7: ('LESHAN GIANT BUDDHA', 'SICHUAN'),
    9: ('LUSHAN', 'JIANGXI'),
    10: ('HANGING TEMPLE', 'DATONG'),
    11: ('YINGWUZHOU BRIDGE', 'WUHAN'),
    12: ('DATANG EVERBRIGHT CITY', "XI'AN"),
    13: ('CHAKA SALT LAKE', 'QINGHAI'),
    14: ('YULIN ROAD', 'CHENGDU'),
}
TITLE = (250, 690, 0.47, 561, 1022)
