# Version A "The VIP walkthrough": her structure. 2x2 collage hook of the doctors at work, medium pace, a card for the report.
import sys,os; sys.path.insert(0,'/home/user/real-or-hype/work/xmedic'); from common import loader
words,idx=loader(os.path.dirname(os.path.abspath(__file__)))
SRC={}
COLLAGE=[('053',12.0,4.0,0.5),('047',0.5,4.0,0.5),('048',1.2,3.0,0.5),('055',47.0,4.0,0.5)]
b=idx('booked'); fr=idx('front'); vip=idx('vip'); th=idx('then',1,vip)
CUES=[
 (b,[('067',0.0,2.6,0.5),('066',0.2,2.2,0.5)]),             # I booked ... at XMEDIC -> the sign
 (idx('they',1,b),[('033',0.8,0.7,0.5),('033',12.8,1.6,0.5)]),  # they even send a shuttle -> walking to the bus, the seats
 (fr,[('040',21.5,2.6,0.5)]),                                # At the front desk
 (idx('check',1,fr),[('041',30.0,0.9,0.5),('043',2.5,2.5,0.5)]),  # you just check in -> receptionist, led away
 (vip,[('043',39.8,0.6,0.5),('043',41.9,1.8,0.5)]),          # your own VIP room -> sign, the room
 (th,[('039',0.2,0.9,0.5),('049',0.0,0.83,0.5),('045',0.5,2.0,0.5)]),  # one room after another -> door signs
 (idx('height'),[('060',0.5,2.5,0.5)]),                      # Height and weight
 (idx('blood'),[('058',4.0,2.5,0.5)]),                       # Blood pressure
 (idx('heart'),[('047',0.3,2.5,0.5)]),                       # Heart and lungs
 (idx('stomach'),[('046',4.0,2.2,0.5)]),                     # your stomach
 (idx('spine'),[('047',8.0,2.0,0.5)]),                       # your spine
 (idx('reflexes'),[('048',1.4,2.4,0.5)]),                    # even your reflexes
 (idx('ecg') if any('ecg' in w[2].lower() for w in words) else idx('ekg'),[('055',47.0,3.0,0.5),('055',58.0,2.0,0.5)]),
 (idx('ct'),[('CT',3.4,1.85,0.5)]),                         # and a CT scan -> CT console, scans on screen
 (idx('lie'),[('044',1.0,3.0,0.5)]),                         # I'm not gonna lie, I expected a hospital
 (idx('hotel'),[('043',12.0,2.6,0.5)]),                      # felt more like a hotel -> corridor
 (idx('when',1,idx('hotel')),[('062',0.5,1.0,0.5),('061',12.3,1.8,0.5)]),                  # breakfast is waiting -> steamer lid
 (idx('bamboo'),[('061',4.4,2.3,0.5)]),                      # Bamboo steamers full of buns
 (idx('congee'),[('069',1.4,2.4,0.5)]),                      # congee
 (idx('eggs'),[('065',0.8,3.0,0.5)]),                        # eggs -> eating by the window
 (idx('whole'),[('036',5.0,3.0,0.5)]),                       # The whole thing took about three hours -> lobby walk
 (idx('report'),[('054',4.0,3.0,0.5)]),                      # the full report comes in five days
 (idx('comment'),[('071',0.0,2.4,0.5),('033',15.5,3.0,0.5)]),# CTA
]
TAIL=1.3
TITLE=["SHANGHAI","Health Check-up"]; TAG="6 doctors, 1 morning"
LABELS=[("knee reflex",idx('reflexes'))]
CARDS=[("full report in","5 days","about 3 hours in total",idx('whole'),idx('comment'))]
CTA=('Comment "CHECKUP"',idx('comment'))
CAPTION_FIX={'XMedic':'XMEDIC','X-Medic':'XMEDIC','Xmedic':'XMEDIC'}
