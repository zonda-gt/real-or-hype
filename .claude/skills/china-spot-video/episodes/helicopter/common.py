# Shared sources for the helicopter episode (all New Sky Helicopter / 新空直升机 flights over the Huangpu River, Shanghai)
H='7458592909487541556'   # 1086x1920 60fps, clean: New Sky Bell 429 over the river by the Bund, cockpit, pad, past the Lujiazui towers
Z='7431589602789444901'   # 720p clean: cabin selfie with the Pearl, Pearl top-down, river + Shanghai Tower
N1='7439413571622079780'  # 720p clean, night: helicopter past Shanghai Tower, red Pearl, cabin, Pearl top-down
NB='7524000840521174287'  # 720p 25fps clean, Fuxing Island night pad + take-off, Pearl at blue hour
R='R7498344434271440180'  # 1080p day, top caption pre-cropped (broll/R....mp4): cockpit, Nanpu Bridge top-down, pilot, Pearl top-down
N3='7496478607096319286'  # 1080p clean, night (New Sky's own account): Pearl below, Jin Mao, Shanghai Tower
N4='7457153339210435877'  # 1080p HLG 60fps clean, night: Shanghai Tower, lit towers
N2='7494937678434602300'  # 4K HLG, night through the window
F='7553921427490409754'   # 720p day, Fuxing Island: towers, Pearl, helicopter on pad, river (subs at 0.69, ad tag top-left)
L='7431793093734698298'   # 720p day, Longhua: route map, boarding, aerials (subs at 0.78, ad tag top-left)
N6='7464147842022509833'  # 1080p night, Xingye: boarding card, headset, helicopter on pad (subs at 0.78)
N5='7530265011562810650'  # 720p night, Fuxing: Pearl sphere, Jin Mao top-down, Bund, SWFC (subs at 0.75)
G='7553958117086022969'   # 720p golden hour: Lujiazui, Jin Mao (subs at 0.74, ad tag 0.88)
K='7564365602241776933'   # 4K HLG 50fps night cabin (subs at 0.65)
SRC={H:{},Z:{},N1:{},NB:{},R:{},N3:{},N4:{},N2:{},F:{'cut':0.33},L:{'cut':0.27},N6:{'cut':0.25},N5:{'cut':0.28},G:{'cut':0.30},K:{'cut':0.40}}
CAPTION_FIX={'Wangpu':'Huangpu','Huangpo':'Huangpu','Lu':'Lujiazui,','Jiazui,':'','Jiazui.':''}
PH='7542771600833236251'  # 1080p clean: hazy Lujiazui seen from the Park Hyatt (SWFC 79F+), tiny helicopter passing
ML='7141608301732629791'  # 720p 60fps, Moon Lake (新辰直升机 月湖店, Songjiang): red Robinson R44 short hop (subs at 0.72)
SRC.update({PH:{},ML:{'cut':0.30}})
