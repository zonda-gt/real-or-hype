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
# Version I "The baby giraffes": two calves born at the hotel, then the grown-ups at breakfast. 2x2 calf collage, medium pace (~1.3 s), labels + one card. Voice: John.
COLLAGE=[(CALF,0.00,3.90,0.5),(BIRTH,21.97,3.45,0.45),(MILK,2.00,3.90,0.5),(BABY,15.50,3.40,0.5)]   # TL calf face, TR newborn by its mother, BL bottle, BR calf walks up
CUES=[
 (at('the first'),      [(CALF2,0.00,1.60,0.5),(BABY,20.00,2.0,0.5)]),           # The first, in April 2024, was six foot one on day one (card)
 (at('the second'),     [(BIRTH,25.55,2.80,0.45)]),           # The second arrived this June.
 (at('here it is'),     [(BIRTH,18.75,1.60,0.42),(BIRTH,28.55,1.6,0.45)]),  # Here it is, just born, right beside its mom
 (at('keepers'),        [(BABY,6.20,1.40,0.5),(MILK,12.00,1.4,0.5)]),       # Keepers bottle-feed the babies
 (at('and every morning'),[(CALF2,4.60,1.50,0.5),(CALF2,9.6,1.3,0.5)]),     # and every morning starts with a head rub
 (at('and the grown'),  [(G,3.90,1.40,0.5)]),               # And the grown-ups?
 (at('they come to'),   [(AIB,0.65,0.65,0.5),(W2,13.00,1.3,0.5)]),  # They come to breakfast (creator at the table as a head comes in)
 (at('one pushes'),     [(R,75.75,1.40,0.68),(G,28.00,1.6,0.40)]),             # One pushes its whole head through the window
 (at('and takes'),      [(G,17.15,1.10,0.6),(B2,20.60,1.4,0.45)]),  # and takes a carrot right from your hand
 (at('outside'),        [(AIW,1.25,1.90,0.5),(G,104.35,1.2,0.5)]),  # Outside, they walk right past you on the bamboo trail (creator looks up)
 (at('its called'),     [(B2,17.20,1.30,0.5),(G,9.90,1.4,0.5)]),    # It's called Giraffe Manor, a hotel in a bamboo forest
 (at('in huzhou'),      [(G,102.95,1.00,0.5),(B2,78.50,1.5,0.5)]),             # in Huzhou, two hours from Shanghai
 (at('comment'),        [(CALF,4.00,1.50,0.5),(MILK,18.00,1.4,0.5),(CALF2,22.00,1.7,0.5)]),            # Comment the word giraffe (back to the calf)
]
TAIL=1.3
TITLE=["BORN AT","a Hotel in China"]; TAG="2 baby giraffes"
LABELS=[("calf #2: June 2026",at('the second')),("bottle time",at('keepers')),("good morning",at('and every morning')),
        ("the grown-ups",at('and the grown')),("Giraffe Manor, Huzhou",at('its called'))]
CARDS=[("the first one","6 ft 1 in","(1.85 m) at birth",at('the first'),at('the second'))]
CTA=('Comment "GIRAFFE"',at('comment'))
MUSIC_DB=-8
