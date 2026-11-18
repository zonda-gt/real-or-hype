# Re-draw <workdir>/ov/title.png with the title block at a custom y (default graphics.py puts it at 760, over the subject).
# usage: title_at.py <workdir> <y> [x of the first line, default 500]   (run after graphics.py; reuses graphics.py's own drawing code)
import sys,re
G='/home/user/real-or-hype/.claude/skills/china-spot-video/scripts/graphics.py'
W,Y=sys.argv[1],int(sys.argv[2]); X=sys.argv[3] if len(sys.argv)>3 else '500'; src=open(G).read()
head=src.split("im=new(); y=760")[0]; title=src.split("im=new(); y=760")[1].split("for k,(txt,_)")[0]
sys.argv=[G,W]; g={'__file__':G}; exec(head,g); exec(f"im=new(); y={Y}"+title.replace("500+80*k",f"{X}+40*k"),g); print('title at y',Y)
