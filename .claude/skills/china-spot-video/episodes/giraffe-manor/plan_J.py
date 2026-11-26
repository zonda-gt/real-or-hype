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
# Version J "Is it worth it?": the wow, the Kenya price gap, then the honest watch-outs. HERO hook on the creator, fast pace (~1 s a shot), heads-up labels + 2 cards. Voice: John.
HERO=(AIB,0.95,1.75,0.5)                                    # the creator at breakfast as a giraffe pushes its head in (startled)
CUES=[
 (at('worth it'),       [(W2,0.85,1.00,0.5)]),              # ...worth it?
 (at('heres the wow'),  [(G,0.05,1.30,0.5)]),               # Here's the wow.
 (at('at breakfast'),   [(W2,13.00,1.10,0.5),(B2,23.00,1.0,0.4),(R,76.10,1.0,0.66)]),  # At breakfast, giraffes push their heads right through the window
 (at('they eat'),       [(R,70.60,1.10,0.45),(G,17.15,1.10,0.6)]),             # They eat carrots from your hand
 (at('a raccoon'),      [(AIR,2.50,1.54,0.5),(WAKE,20.00,1.0,0.5)]),             # A raccoon can be your wake-up call (creator crouches, raccoon at his hand)
 (at('and capybaras'),  [(B2,2.40,1.10,0.5),(B2,36.20,1.3,0.5)]),              # And capybaras soak in the pond outside
 (at('the famous'),     [(SKY,0.00,1.40,0.5),(SKY,13.40,1.1,0.5),(R,74.40,1.1,0.6),(B2,26.65,1.6,0.42)]),           # The famous one in Kenya ... $1,400+ (card)
 (at('here its a fraction'),        [(B2,19.00,1.40,0.45),(G,26.00,1.2,0.35)]),           # Here, it's a fraction of the price (card)  [Whisper: "Here, it's a" -> "heresa"? see at()]
 (at('now the honest'), [(WINTER,0.05,0.80,0.6),(WINTER,4.55,1.0,0.5)]),          # Now, the honest part.
 (at('weekends'),       [(B2,55.85,0.80,0.5),(B2,57.80,0.8,0.5),(B2,59.15,1.0,0.5)]),            # Weekends and holidays book up fast
 (at('window tables'),  [(B2,14.80,1.15,0.5),(G,20.05,0.95,0.5),(R,36.75,1.3,0.5)]),              # Window tables go first, so line up by six thirty
 (at('and on cold'),    [(WINTER,25.20,1.30,0.5),(B2,29.75,1.3,0.5)]),         # And on cold, rainy days,
 (at('may stay'),       [(WINTER,47.65,2.05,0.40)]),        # the giraffes may stay inside (indoor giraffe house)
 (at('so go on'),       [(W2,6.00,1.40,0.5),(G,4.0,1.2,0.45)]),               # So go on a warm weekday,
 (at('and yes'),        [(W2,1.95,0.85,0.5),(AIW,3.15,0.89,0.5)]),             # and yes, it's worth it (creator grins at camera)
 (at('giraffe manor'),  [(R,62.10,0.80,0.5),(G,9.90,1.0,0.5)]),              # It's Giraffe Manor, in Huzhou
 (at('two hours'),      [(WINTER,63.70,0.80,0.5),(G,102.95,1.0,0.5)]),         # two hours from Shanghai
 (at('comment'),        [(R,0.05,1.0,0.40),(W2,17.20,0.9,0.5),(G,105.85,1.0,0.5),(B2,97.75,2.1,0.5)]),  # Comment the word giraffe
]
TAIL=1.3
TITLE=["IS IT","Worth It?"]; TAG="China's giraffe hotel"
LABELS=[("the wow",at('heres the wow')),("book ahead",at('weekends')),("6:30 AM",at('window tables')),("cold or rainy?",at('and on cold'))]
CARDS=[("the one in Kenya","$1,400+","a night, per person",at('the famous'),at('here its a fraction')),
       ("here","a fraction","of the price",at('here its a fraction'),at('now the honest'))]
CTA=('Comment "GIRAFFE"',at('comment'))
MUSIC_DB=-8
