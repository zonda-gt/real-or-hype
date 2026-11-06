# Internal review reel of luxury-tier candidates (not for posting)
import subprocess, os
os.makedirs("work/review", exist_ok=True)
C = [  # (label lines, aweme_id, [(start, end), ...])
 ("NOW IN THE REEL (for comparison)\\NBanyan Tree On The Bund · suite ¥6,000+/night\\N1080p but dark, soft, shaky", "7672385530935491529", [(12.4, 13.5), (36.9, 38.9)]),
 ("OPTION 1 · Banyan Tree On The Bund (other room)\\N≈ ¥5,000/night (creator: 我住的这一晚将近5千)\\N1080p daylight · 13k likes · ad-flagged", "7679431597737452470", [(8.3, 9.6), (9.6, 10.6), (10.6, 15.6), (16.0, 20.5)]),
 ("OPTION 2 · Seagull Regent (海鸥丽晶), Bund river view\\N¥5,000/night (desc: 五千一晚)\\N720p only · overcast · 33 likes / 113 shares", "7703776884844711857", [(3.0, 5.5), (9.5, 12.0), (16.5, 18.5), (25.0, 30.0), (32.0, 35.0)]),
 ("OPTION 3 · Bulgari Shanghai\\N¥6,762/night base room (booking screenshot at 0 s)\\N1080p · pool only, no room/bathroom shots · subtitles", "7692449574867712502", [(0.0, 0.9), (1.0, 3.0), (20.0, 24.0)]),
]
parts = []; ass_ev = []; t = 0.0
for i, (lab, aid, segs) in enumerate(C):
    t0 = t
    for j, (a, b) in enumerate(segs):
        p = f"work/review/c{i}_{j}.mp4"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(a), "-t", str(b - a), "-i", f"raw/best/{aid}.mp4", "-an",
                        "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,format=yuv420p",
                        "-c:v", "libx264", "-crf", "18", "-preset", "fast", p], check=True)
        parts.append(p); t += b - a
    ass_ev.append((t0, t, lab))
open("work/review/list.txt", "w").write("".join(f"file '{os.path.abspath(p)}'\n" for p in parts))
def ts(x): return f"0:{int(x//60):02d}:{x%60:05.2f}"
ass = """[Script Info]
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: L,Montserrat ExtraBold,44,&H00FFFFFF,&H00FFFFFF,&H00000000,&HB0000000,0,0,0,0,100,100,0,0,3,14,0,8,40,40,250,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""" + "".join(f"Dialogue: 0,{ts(a)},{ts(b)},L,,0,0,0,,{l}\n" for a, b, l in ass_ev)
open("work/review/labels.ass", "w").write(ass)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "work/review/list.txt", "-vf", "subtitles=work/review/labels.ass:fontsdir=work/fonts",
                "-c:v", "libx264", "-crf", "20", "-preset", "medium", "-movflags", "+faststart", "luxury_candidates_review.mp4"], check=True)
print("total", round(t, 1), "s")
