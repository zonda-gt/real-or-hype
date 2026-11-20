# Version A "The VIP walkthrough": her structure. 2x2 collage hook of the doctors at work, medium pace, a card for the report.
import sys,os; sys.path.insert(0,'/home/user/real-or-hype/work/xmedic'); from common import loader
words,idx=loader(os.path.dirname(os.path.abspath(__file__)))
SRC={'dy':{'cut':0.12}}   # dy = Douyin CT clip 7438392919872130364 (720p; burned subtitles at the very bottom)
COLLAGE=[('053',12.0,4.0,0.5),('dy',12.5,4.0,0.5),('048',1.2,3.0,0.5),('047',0.5,4.0,0.5)]   # TL neck, TR CT scanner, BL knee tap, BR stethoscope
b=idx('booked'); fr=idx('front'); vip=idx('vip'); th=idx('then',1,vip)
CUES=[
 (b,[('067',0.0,2.6,0.5),('066',0.2,2.2,0.5)]),             # I booked ... at XMEDIC -> the sign
 (fr,[('040',21.5,2.6,0.5)]),                                # At the front desk
 (idx('english'),[('041',30.0,1.2,0.5),('043',2.5,2.5,0.5)]),    # with English-speaking staff -> receptionist, led away
 (vip,[('043',39.8,0.6,0.5),('043',41.9,1.8,0.5)]),          # your own VIP room -> sign, the room
 (th,[('039',0.0,1.25,0.5),('049',0.0,0.83,0.5),('045',0.5,2.0,0.5)]),  # one room after another -> door signs
 (idx('height'),[('060',0.5,2.5,0.5)]),                      # Height and weight
 (idx('blood'),[('058',4.0,2.5,0.5)]),                       # Blood pressure
 (idx('heart'),[('047',0.3,2.5,0.5)]),                       # Heart and lungs
 (idx('stomach'),[('046',4.0,2.2,0.5)]),                     # your stomach
 (idx('spine'),[('047',8.0,2.0,0.5)]),                       # your spine
 (idx('reflexes'),[('048',1.4,2.4,0.5)]),                    # even your reflexes
 (idx('ecg') if any('ecg' in w[2].lower() for w in words) else idx('ekg'),[('055',47.0,3.0,0.5),('055',58.0,2.0,0.5)]),
 (idx('ct'),[('CT',3.4,0.9,0.5),('dy',30.2,2.0,0.5)]),                         # and a CT scan -> CT console, scans on screen
 (idx('expected'),[('044',1.0,3.0,0.5)]),                         # I'm not gonna lie, I expected a hospital
 (idx('hotel'),[('043',12.0,2.6,0.5)]),                      # felt more like a hotel -> corridor
 (idx('when',1,idx('hotel')),[('070',0.0,1.1,0.5),('069',1.4,2.0,0.5)]),  # breakfast is waiting in your room -> him at the tray, congee close-up (private room)
 (idx('and',1,idx('waiting')),[('033',12.8,1.2,0.5),('034',1.2,1.8,0.5)]),  # And they even send a private shuttle -> the seats, him in one
 (idx('whole'),[('036',5.0,3.0,0.5)]),                       # The whole thing took about three hours -> lobby walk
 (idx('report'),[('054',4.0,1.8,0.5),('050',0.3,2.2,0.5)]),                      # the full English report ... comes in three days
 (idx('comment'),[('071',0.0,2.4,0.5),('035',6.0,3.0,0.5)]),# CTA
]
TAIL=1.3
TITLE_STYLE="stack"; TITLE_Y=825; TITLE=["My health check-up in Shanghai","6 Doctors, 1 Morning"]; TAG=None
LABELS=[("knee reflex",idx('reflexes'))]
CARDS=[("","3 hours","English report in 3 days",idx('whole'),idx('comment'))]
CTA=('Comment "CHECKUP"',idx('comment'))
CAPTION_FIX={'XMedic':'XMEDIC','X-Medic':'XMEDIC','Xmedic':'XMEDIC'}
