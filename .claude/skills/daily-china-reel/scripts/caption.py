#!/usr/bin/env python3
"""Write EPISODE_DIR/caption.txt: hook, the places, a question, music credit (CC BY), Douyin clip credits, hashtags.

  caption.py EPISODE_DIR [--hook "..."] [--tags "#chinatravel #harbin"]
"""
import argparse, json, os

p = argparse.ArgumentParser()
p.add_argument("ep"); p.add_argument("--hook", default=None); p.add_argument("--tags", default=None)
x = p.parse_args()
ep = json.load(open(f"{x.ep}/episode.json"))
meta = json.load(open(f"{x.ep}/clips/meta.json"))
places = [ln["b"]["cap"].split("|")[-1] for ln in ep["lines"] if ln.get("b")]
hook = x.hook or ep.get("hook") or f"{ep['title']}: save this for your China trip"
authors = []
for ln in ep["lines"]:
    for side in ("a", "b"):
        c = (ln.get(side) or {}).get("clip")
        a = (meta.get(c) or {}).get("author")
        if a and a not in authors:
            authors.append(a)
tags = x.tags or ep.get("tags") or "#chinatravel #travelchina #visitchina #china #traveltips"
music = ep.get("music", "Happy Bee")
text = (f"{hook}\n\n" + " · ".join(places) + "\n\nWhich one would you go to first? 👇\n\n"
        f"Music: \"{music}\" by Kevin MacLeod (incompetech.com), licensed under CC BY 4.0\n"
        f"Clips: Douyin creators {', '.join(authors)}\n\n{tags}\n")
open(f"{x.ep}/caption.txt", "w").write(text)
print(text); print(len(text), "chars")
