# Edit list: (t0 on final timeline = word onset, source clip, in-point). Shot runs until the next t0.
END=65.65
EDL=[
(0.00,'A_night',0.5),(1.85,'K_aerial1',9.5),(3.23,'B_gatem',34.6),(4.42,'B_gatem',42.0),
(5.56,'B_gatem',0.0),(6.90,'A_night',18.5),(8.71,'K_aerial1',12.0),
(10.18,'J_escal',0.5),(12.20,'S_dogs',23.5),(12.89,'S_dogs',3.5),(13.63,'S_dogs',15.2),(15.22,'S_dogs',9.3),
(17.24,'I_silos',7.2),(18.52,'I_silos',12.8),(19.61,'N_rooftop',7.25),(21.27,'N_rooftop',9.25),
(22.11,'T_wdsign',52.65),(23.30,'Q_wilddock',2.37),(24.38,'Q_wilddock',2.9),(25.62,'Q_wilddock',3.64),
(26.62,'Q_wilddock',5.47),(28.52,'Q_wilddock',0.1),(29.30,'A_night',45.5),
(31.08,'R_gm',27.3),(32.95,'R_gm',18.35),(33.62,'R_gm',12.6),(34.62,'R_gm',13.62),(35.90,'R_gm',22.4),
(37.18,'F_blue',2.0),(38.33,'O_river',3.27),(39.80,'I_silos',5.2),(41.11,'M_sunset',2.2),
(42.32,'F_blue',0.12),(43.33,'A_night',20.5),(44.69,'B_gatem',2.4),(45.84,'B_gatem',10.0),(47.28,'E_concert',16.4),
(48.95,'C_xmas',0.3),(49.95,'D_tree',7.25),(51.29,'D_tree',0.2),(53.12,'C_xmas',18.1),
(54.50,'A_night',42.0),(56.63,'B_gatem',45.5),(57.43,'A_night',51.5),(60.43,'H_light',38.0),(62.44,'B_gatem',38.3)]
# idx -> (zoom, anchor-y, anchor-x): crops out burned-in captions / letterbox bars
CROP={14:(1.4,0.0,0.5),15:(1.4,0.0,0.5),16:(1.5,0.0,0.5),29:(1.3,0.45,0.5),30:(1.3334,0.5,0.5),31:(1.3334,0.5,0.5)}
# on-screen graphics, times on the final timeline
TITLE=('GATE M','West Bund Dream Center','in  Shanghai',0.0,3.15)
LABELS=[ # (start, end, text, centre-x, centre-y, angle)
 (13.63,15.22,'dog-friendly',540,560,-4),(19.61,21.27,'silo rooftop',560,520,-4),(23.30,24.38,'Wild Dock',540,520,-4),
 (26.62,28.52,'about ¥180 / person',540,560,-3),(31.08,32.95,'Gentle Monster',540,330,-3),(38.33,39.80,'800m riverfront',520,640,-3),
 (45.84,47.28,'light show on the silos',540,1180,-3),(49.95,51.29,'ice rink, last winter',540,330,-3),(57.43,60.43,'walk to Tank Shanghai',540,640,-3)]
PILLS=[(54.50,57.43,['Metro Line 11','Longyao Rd · Exit 4'],520)]
FOLLOW=(62.44,None)
def shots():
    out=[]
    for i,(t0,src,inn) in enumerate(EDL):
        t1=EDL[i+1][0] if i+1<len(EDL) else END
        z,ay,ax=CROP.get(i,(1.0,0.5,0.5))
        out.append(dict(i=i,t0=t0,dur=round(t1-t0,3),src=src,inn=inn,z=z,ay=ay,ax=ax))
    return out
MUSIC=('music/m3.mp3',6.0,-9)
CAPTION_REPLACE={'龙耀路':'LONGYAO LU'}
