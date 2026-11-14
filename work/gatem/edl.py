# t0 (final timeline, s), source, in-point (s), zoom, anchor-y (0 top..1 bottom), anchor-x
END=50.45
EDL=[
(0.00,'A_night',0.5),(1.90,'K_aerial1',9.5),(3.24,'B_gatem',34.6),(4.45,'B_gatem',42.0),
(5.59,'B_gatem',0.0),(6.94,'A_night',18.5),(8.52,'K_aerial1',12.0),(10.00,'J_escal',0.5),
(11.89,'I_silos',1.6),(13.95,'I_silos',7.2),(15.32,'I_silos',12.8),(16.37,'N_rooftop',4.0),
(17.38,'N_rooftop',7.25),(19.24,'N_rooftop',9.25),(20.52,'K_aerial1',5.2),(21.24,'F_blue',2.0),
(22.31,'O_river',3.22),(23.90,'I_silos',5.2),(25.71,'M_sunset',2.2),(26.94,'F_blue',0.0),
(28.01,'A_night',20.5),(29.39,'B_gatem',2.4),(30.58,'B_gatem',10.0),(31.87,'E_concert',16.4),
(33.53,'C_xmas',0.3),(34.48,'D_tree',7.25),(35.86,'D_tree',0.2),(38.01,'C_xmas',18.1),
(39.33,'A_night',42.0),(41.34,'B_gatem',45.5),(42.20,'A_night',51.5),(45.23,'H_light',38.0),
(47.22,'B_gatem',38.3)]
CROP={11:(1.4,0.0,0.5),12:(1.4,0.0,0.5),13:(1.4,0.0,0.5),16:(1.3,0.45,0.5),17:(1.3334,0.5,0.5),18:(1.3334,0.5,0.5)}  # idx -> (zoom, ay, ax)
def shots():
    out=[]
    for i,(t0,src,inn) in enumerate(EDL):
        t1=EDL[i+1][0] if i+1<len(EDL) else END
        z,ay,ax=CROP.get(i,(1.0,0.5,0.5))
        out.append(dict(i=i,t0=t0,dur=round(t1-t0,3),src=src,inn=inn,z=z,ay=ay,ax=ax))
    return out
