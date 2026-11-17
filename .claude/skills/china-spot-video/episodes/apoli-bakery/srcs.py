# shared source ids + bottom-crop fractions (burned subtitles sit at ~0.77 of height; Q's at ~0.66)
P='7662654833274632698'  # 720p wide, clean, 2026: entrance 0-9.8, counter 9.8-19.4, desserts 19.4-26.5, crowds 26.5-37.3, wheel 38.3-43.1, arches/exit 43.1-
L='7417095420498726144'  # 720p clean: ceiling 14-18.9, window 23.5-26.8, eclair 29.7-32, TOP2 32-34.3, TOP1 choc 36.2-38.6, pistachio tarts 41.5-44, buns 44-52
G='7413386842168397107'  # 1080p 120fps: woman w/ plate 0.5-3.37, castle door 3.37-4.5, sconce 4.5-5.97, Wukang 5.97-7.23, tray 8.67-10.5, interior 10.5-18, burger 22.9-24.3, coffee 55-57.6, tiramisu 65.9-68, swirls 70.9-75.6
S='7556148391236128058'  # 720p: walk in door 4.9-8.1, hall 8.1-10.8, counter 17.5-22.2, desserts 27.3-32.7, TOP1 strawberry 38.9-45.7
Q='7414326013427060009'  # 1080p: facade 1.8-5.4, interior 8.8-20.8, crowd 20.8-37.5, tongs+plate 65.5-71.7
R='7426794630210981178'  # 720p: chandelier 3.9-6.9, sign 15.2-18.3, queue 23.2-25.9, exterior 25.9-30
T='7418168285440593179'  # 1080p: queue 7.1-9, crowd 12-14.2, candle 14.2-16.3, branches 16.3-18.6, tongs 22.6-24.2, street crowd 24.2-27
H='7413297549991218486'  # 1080p HORIZONTAL: ceiling 8.1-10.1, worker w/ tray 13.3-15.4, sandwich 26.4-28.3, green donut 29.9-33.3, coffee 33.3-36.5
SRC={P:{},L:{},G:{'cut':0.26},S:{'cut':0.26},Q:{'cut':0.36},R:{'cut':0.26},T:{'cut':0.26},H:{'cut':0.18}}
