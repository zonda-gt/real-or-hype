# Version B "What I expected vs what I got": one full-screen hero hook, quicker cuts on every "Instead",
# door signs on the specialities, his real line at the buffet.
import sys,os,json; sys.path.insert(0,'/home/user/real-or-hype/work/xmedic'); from common import loader
D=os.path.dirname(os.path.abspath(__file__)); words,idx=loader(D)
SRC={'dy':{'cut':0.12},'dyF':{'cut':0.32}}   # dy = Douyin CT clip 7438392919872130364 (720p; burned subtitles at the very bottom)
HERO=('053',11.5,2.4,0.5)                                    # hook: doctor checking his neck
i1=idx('instead',1); i2=idx('instead',2); i3=idx('instead',3); i4=idx('instead',4)
real=json.load(open(f'{D}/real.json')) if os.path.exists(f'{D}/real.json') else None
CUES=[
 (idx('long'),[('dy',12.5,1.0,0.5),('048',1.4,1.0,0.5)]),  # ...long queues and crowded hallways -> stethoscope, knee reflex
 (idx('heres'),[('043',12.0,1.6,0.5)]),                     # Here's what I actually got -> a bit of the hallway walk
 (i1,[('033',12.6,2.4,0.5)]),                                # Instead of a taxi, the clinic's shuttle
 (idx('leather'),[('034',0.3,3.0,0.5)]),                     # with leather recliners
 (i2,[('043',2.5,2.5,0.5)]),                                 # Instead of a queue, someone walks you
 (idx('vip'),[('043',39.8,0.4,0.5),('043',41.9,1.8,0.5)]),   # your own VIP room
 (i3,[('057',4.5,3.0,0.5)]),                                 # Instead of a paper gown
 (idx('matching'),[('048',5.2,0.8,0.5),('060',0.5,2.0,0.5)]),# matching navy pyjamas
 (i4,[('053',6.0,2.5,0.5)]),                                 # And instead of one rushed doctor
 (idx('six'),[('046',7.0,2.5,0.5)]),                         # it's six doctors, room after room
 (idx('surgery'),[('049',0.0,0.8,0.5),('053',20.0,1.5,0.5)]),# Surgery -> door 213
 (idx('eyes'),[('039',0.0,1.3,0.5)]),                        # Eyes -> door 208
 (idx('heart'),[('047',0.3,2.2,0.5)]),                       # Heart and lungs
 (idx('ecg') if any('ecg' in w[2].lower() for w in words) else idx('ekg'),[('055',47.0,3.0,0.5)]),
 (idx('ct'),[('CT',3.4,1.85,0.5)]),                         # and a CT scan -> CT console, scans on screen
 (idx('crowds'),[('038',3.0,2.5,0.5)]),                      # No crowds
 (idx('quiet'),[('043',26.0,2.6,0.5)]),                      # just these quiet corridors
 (idx('favourite') if any('favo' in w[2].lower() for w in words) else idx('favorite'),[('062',0.0,3.0,0.5)]),
 (idx('breakfast'),[('061',12.3,1.8,0.5)]),                  # breakfast is waiting
]
if real: CUES.append((real['idx'],[('061',real['voiced0']-0.10,real['clip_out']-real['voiced0']+0.8,0.5)]))  # his real line, synced
CUES+=[
 (idx('zero'),[('065',0.8,3.0,0.5)]),                        # Zero complaints
 (idx('called'),[('067',0.0,2.8,0.5),('066',0.2,2.2,0.5)]),  # It's called XMEDIC
 (idx('report'),[('054',4.0,3.0,0.5)]),                      # the full report comes in five days
 (idx('comment'),[('043',41.9,1.8,0.5),('033',15.5,3.0,0.5)]), # CTA
]
TAIL=1.3
TITLE_UNTIL=i1
TITLE=["WHAT I EXPECTED","vs What I Got"]; TAG="health check-up in Shanghai"
LABELS=[("6 doctors",idx('six')),("VIP Room 10",idx('vip'))]
CARDS=[]
CTA=('Comment "CHECKUP"',idx('comment'))
CAPTION_FIX={'XMedic':'XMEDIC','X-Medic':'XMEDIC','Xmedic':'XMEDIC'}
