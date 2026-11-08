"""Validate every shot of a spec against the OCR map: no detected text inside crop (+margin) over the used source range."""
import sys,os,json,importlib.util
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
s=importlib.util.spec_from_file_location('spec',sys.argv[1]); m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
B=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
bad=0; acc=0
for bi,b in enumerate(m.BEATS):
    for sh in b['shots']:
        d=json.load(open(f"{B}/ocr/{sh['clip']}.json")); x,y,w,h=sh['crop']; mg=16
        t0=sh['t']; t1=t0+(0.05 if sh.get('freeze') else b['dur']*sh.get('speed',1.0))
        assert x>=0 and y>=0 and x+w<=d['w'] and y+h<=d['h'], ('crop out of frame',sh)
        hits=[(fr['t'],bx[4]) for fr in d['frames'] if t0-0.12<=fr['t']<=t1+0.12 for bx in fr['boxes'] if bx[2]>x-mg and bx[0]<x+w+mg and bx[3]>y-mg and bx[1]<y+h+mg]
        st='CLEAN' if not hits else f'TEXT {hits[:4]}'
        if hits: bad+=1
        print(f"beat{bi} @{acc:5.2f} {b['layout']:6} {sh['clip']} src {t0:.2f}-{t1:.2f} {st}")
    acc+=b['dur']
print('total',round(acc,2),'s;', 'ALL CLEAN' if not bad else f'{bad} DIRTY')
sys.exit(1 if bad else 0)
