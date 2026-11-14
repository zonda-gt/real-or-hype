# GATE M, tight version (33 s): one fact per sentence, nothing repeated.
END=33.55
EDL=[
(0.00,'A_night',0.5),                       # This was the biggest cement factory in Asia.  (title card)
(2.09,'B_gatem',0.0),                       # Now it's Gate M,
(3.36,'A_night',18.5),                      # the West Bund Dream Center,
(4.78,'K_aerial1',12.0),                    # on the Huangpu River.
(5.85,'S_dogs',15.2),                       # It's super dog-friendly,
(7.34,'S_dogs',9.3),                        # so the café terraces are full of dogs.
(9.41,'I_silos',7.2),                       # Inside the old silos,
(10.70,'Q_wilddock',2.37),                  # there's Wild Dock,
(11.72,'Q_wilddock',2.92),                  # where everything is grilled over apple-wood charcoal,
(13.84,'Q_wilddock',5.50),                  # for about 180 yuan
(14.95,'Q_wilddock',0.4),                   # per person.
(15.97,'R_gm',27.3),                        # Gentle Monster opened a store here in September,
(18.16,'R_gm',12.6),(18.96,'R_gm',13.65),   # full of giant face sculptures.
(19.91,'O_river',3.24,(1.5,0.3,0.5)),                     # The 800-meter riverfront
(21.42,'O_river',0.1,(1.5,0.3,0.5)),                      # looks out to Lupu Bridge,
(22.57,'F_blue',0.12),                      # and it's best at blue hour,
(23.89,'M_sunset',2.2,(1.3334,0.5,0.5)),                     # right after sunset.
(24.95,'S_dogs',26.45),                     # It's free to walk around.
(26.15,'A_night',42.0),                     # Take Line 11 to 龙耀路, exit 4,
(28.82,'A_night',51.5),                     # then walk along the river to Tank Shanghai.
(30.80,'B_gatem',38.3)]                     # Follow me for more Shanghai spots worth exploring.
# crop lives on the shot itself: optional 4th item (zoom, anchor_y, anchor_x)
TITLE=('GATE M','West Bund Dream Center','in  Shanghai',0.0,2.05)
LABELS=[(5.85,7.34,'dog-friendly',540,560,-4),(10.70,11.72,'Wild Dock',540,1150,-4),(13.84,15.97,'about ¥180 / person',540,560,-3),
 (15.97,18.16,'Gentle Monster',540,330,-3),(19.91,21.42,'800m riverfront',520,640,-3),(21.42,22.57,'Lupu Bridge',540,420,-3),
 (28.82,30.80,'walk to Tank Shanghai',540,640,-3)]
PILLS=[(26.15,28.82,['Metro Line 11','Longyao Rd · Exit 4'],520)]
FOLLOW=(30.80,None)
MUSIC=('music/m3.mp3',12.0,-9)
CAPTION_REPLACE={'龙耀路':'LONGYAO LU'}
def shots():
    out=[]
    for i,e in enumerate(EDL):
        t0,src,inn=e[:3]
        t1=EDL[i+1][0] if i+1<len(EDL) else END
        z,ay,ax=e[3] if len(e)>3 else (1.0,0.5,0.5)
        out.append(dict(i=i,t0=t0,dur=round(t1-t0,3),src=src,inn=inn,z=z,ay=ay,ax=ax))
    return out
