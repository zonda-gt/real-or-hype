# Version B "Iron Man is the villain now": story/news angle. Full-screen Doom hero hook, fast cuts, number cards.
import sys; sys.path.insert(0,'/home/user/real-or-hype/work/avengers-ggw'); from common import *
CAPTION_FIX={k:v for k,v in CAPTION_FIX.items() if k not in ('set','up')}
MUSIC='/home/user/real-or-hype/work/avengers-ggw/B/music.wav'
HERO=(R,8.0,2.1,0.5); COLLAGE=[]
CUES=[
 (9,[(Q,3.2,1.5,0.5)]),                       # is now the villain
 (14,[(R,4.0,1.0,0.5)]),                      # And Doctor Doom
 (17,[(C,10.6,1.6,0.5)]),                     # just landed in Shanghai
 (20,[(L,19.0,0.9,0.5),(L,24.5,0.9,0.5)]),                     # He's sitting outside Grand Gateway
 (25,[(N,1.7,1.3,0.5),(C,28.0,1.1,0.5)]),     # under a giant Avengers logo
 (30,[(Q,8.2,1.0,0.5)]),                      # Shanghai is one of
 (35,[(C,4.8,1.15,0.5),(L,30.0,1.3,0.45)]),     # only nine cities on the global tour
 (41,[(P,16.6,0.65,0.5),(P,2.4,0.7,0.5)]),                     # China gets the movie
 (46,[(R,6.0,1.4,0.5)]),                      # on December 16th
 (48,[(K,2.0,0.9,0.6),(C,13.0,0.9,0.5)]),                      # two days before America
 (52,[(Q,10.6,0.7,0.5),(N,3.2,0.7,0.5)]),                     # and on December 10th
 (56,[(C,18.2,1.0,0.5),(N,6.0,0.9,0.55),(C,28.6,1.4,0.5)]),    # the cast is coming to Shanghai
]
TITLE=["IRON MAN","is the villain now"]; TAG="and he's in Shanghai"
LABELS=[("Doctor Doom",14)]
CARDS=[("Shanghai is 1 of","9 cities","on the global tour",35,41),("in cinemas in China","Dec 16","2 days before the US",46,52)]
CTA=None
