# --- shared header (Huzhou Giraffe Manor H/I/J). Cues are found by PHRASE in words.json, so the plan survives a new voice take
# (Whisper may write "9 a.m.", "wake-up" or "wake" "-up"; matching runs on the words joined without spaces or punctuation).
import json,os,re
_W=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'words.json')))
_N=[re.sub(r'[^a-z0-9]','',w[2].lower()) for w in _W]; _S=''.join(_N); _O=[sum(len(x) for x in _N[:i]) for i in range(len(_N))]
def at(phrase,k=1):
    """index of the first word of the k-th occurrence of phrase"""
    p=re.sub(r'[^a-z0-9]','',phrase.lower()); pos=-1
    for _ in range(k):
        pos=_S.find(p,pos+1)
        if pos<0: raise SystemExit(f'plan: cue phrase not in words.json: {phrase!r}')
    return max(i for i,o in enumerate(_O) if o<=pos)
B2='7653507861812628772'; G='7651132730540887336'; R='7653362319732886150'   # 4K vlogs (burned subtitles: cut)
W2='7685311414965524923'      # 1080x1440: sunny restaurant; giraffe face 0.8-1.9, outside 5.93-8.77, neck over diners 12.83-17.13, at the table by a child 17.13-24.8
WAKE='7702806207996158385'    # raccoon wake-up call (HLG vertical): room 4.83-34.7, at the glass door 46.2-51.9
BIRTH='7650310001970073807'   # 4K (keepers' video, 12 Jun 2026): the June 2026 calf, on the straw 8.2-11.6, standing by its mother 18.7-21.96, 21.96-25.46, 28.48-31.5
MILK='7651279604527986664'    # vertical: keeper bottle-feeds a calf (14 Jun 2026)
CALF2='7653265250729437775'   # vertical: calf in the giraffe house 0-4, keeper's hand on its head 4.5-8
CALF='7665754019054754033'    # vertical 720p: calf face to camera 0-7.7
BABY='7673338456038363624'    # vertical 60 fps: bottle in front of calf 6-15, calf walks up to camera 15.5-19
WINTER='7604799138752724410'  # 1080p winter vlog: misty hills 4.5-6.0, bamboo path 25.13-27.8, indoor giraffe house 47.0-49.73, drone 63.63-
SKY='7706044234537230691'     # vertical: giraffe against the sky (generic, for the Kenya line)
BON='7654958528349001123'     # vertical 42 fps: bonfire show at night (title card at 0-0.05)
AIB='ai25_me_breakfast'; AIW='ai25_me_walkway'; AIR='ai25_me_raccoon'; AIF='ai25_me_bonfire'   # the creator, Seedance 2.5, 720p 24 fps
SRC={B2:{'cut':0.14},G:{'cut':0.14},R:{'cut':0.18},W2:{},WAKE:{},BIRTH:{'cut':0.14},MILK:{},CALF2:{},CALF:{},BABY:{},WINTER:{'cut':0.19},SKY:{},BON:{},AIB:{},AIW:{},AIR:{},AIF:{}}
# Version H "A day at China's giraffe hotel": the day in order, second person. HERO hook, relaxed pace (~1.6 s a shot), handwritten time-of-day labels. Voice: John.
HERO=(W2,21.10,3.65,0.50)                                 # giraffe at the breakfast table beside a child
CUES=[
 (at('looks like')+2,   [(AIR,0.00,2.45,0.5)]),             # Nine AM. Your wake-up call is an animal (creator wakes up, raccoon trots in)
 (at('and sometimes'),  [(WAKE,46.30,2.60,0.5),(WAKE,20.00,2.0,0.5)]),  # sometimes, a raccoon trots into your room
 (at('then breakfast'), [(B2,14.80,1.20,0.5)]),              # Then breakfast.
 (at('a giraffe pushes'),[(R,75.75,1.40,0.68),(W2,13.00,2.5,0.5)]),     # A giraffe pushes its head through the window, right next to your plate
 (at('and yes'),        [(AIB,2.60,1.44,0.5),(G,26.00,1.5,0.35)]),             # And yes, you can give it a pat (creator laughs, pats it)
 (at('after breakfast'),[(B2,7.10,1.05,0.5),(B2,40.10,1.25,0.5)]),         # After breakfast, you walk the bamboo forest
 (at('and giraffes stroll'),[(B2,4.25,1.20,0.5),(AIW,1.30,1.75,0.5)]),  # and giraffes stroll right past the fence (creator looks up)
 (at('down by the pond'),[(B2,31.85,1.70,0.5)]),            # Down by the pond, capybaras are soaking
 (at('and red'),        [(B2,28.50,1.20,0.5),(B2,29.75,1.6,0.5)]),             # and red-crowned cranes stand in the mist
 (at('at night'),       [(BON,0.60,2.80,0.5),(AIF,0.60,0.85,0.5)]),  # At night, there's a bonfire show, with music and dancing
 (at('then you sleep'), [(G,9.90,1.50,0.5),(R,62.10,1.2,0.5)]),         # Then you sleep in a villa, deep in the bamboo
 (at('giraffe manor'),  [(G,104.35,1.40,0.5)]),             # It's Giraffe Manor, in Huzhou
 (at('two hours'),      [(G,102.95,1.35,0.5)]),             # two hours from Shanghai
 (at('comment'),        [(W2,0.85,1.00,0.5),(B2,97.75,2.4,0.5)]),  # Comment the word giraffe
]
TAIL=1.3
TITLE=["A DAY AT","China's Giraffe Hotel"]; TAG="wake-up call to bonfire"
LABELS=[("9 AM: wake-up call",at('looks like')+2),("breakfast",at('then breakfast')),("bamboo walk",at('after breakfast')),
        ("capybara",at('down by the pond')),("red-crowned crane",at('and red')),("night: bonfire show",at('at night')),("your villa",at('then you sleep'))]
CARDS=[]
CTA=('Comment "GIRAFFE"',at('comment'))
MUSIC_DB=-8
