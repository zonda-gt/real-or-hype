---
name: free-places-reel
description: Make and post the daily "<City> is expensive, but... these 9 places cost $0" reel for @steven_chinapal - Douyin B-roll, the reference song's cut timing, editorial text, DM CTA, posted as an Instagram trial reel. Use for the daily scheduled run, or when the user asks for a free-places video for a city.
---

# Free-places reel ("<CITY> IS EXPENSIVE, BUT...")

A 31.8 s vertical reel: 2 opening shots, 9 free places x 2 shots each, 2 ending shots, cut on the beat of the reference song (an Awe China reel; its audio is the soundtrack). Text: hook `<CITY> IS EXPENSIVE, BUT...`, each place as a white Anton headline with a yellow `$0 · FREE` bar, ending `DM US FOR A FREE / PERSONALIZED ITINERARY` with DM and FREE in yellow. Posted as an Instagram **trial reel** with the `instagram-trial-reel` skill.

Scripts are in `scripts/` (run with `python3 -I`, paths absolute). Work in a fresh scratchpad folder, e.g. `$W`.

## Daily run

### 1. Pick the city and places
- Cities (top tier, rotate): **Shanghai, Beijing, Hangzhou, Guangzhou, Shenzhen, Chongqing**. Run `scripts/history.py show` and pick the city posted least recently (prefer one with no video yet). Never the same city two days in a row.
- 9 places that are **free** to enter or see, look great in 1.5 s (big interiors, skylines, lights, unusual buildings), have lots of Douyin footage, and are varied (modern + old, day + night).
- **Repeat city**: at least 5 of the 9 places must not have appeared in any earlier video of that city (history.json). Shot choices for repeated places must differ too.
- **Verify "free" with a web search for every place** and drop anything paid (the user caught a "free" bookstore that needed a paid drink). Paid examples: Yu Garden itself, Shanghai Tower deck, Duoyun Bookstore, Raffles sky bridge, cableways, Forbidden City, Summer Palace, West Lake boats. If only part is free, name the free part (e.g. "Yuyuan Bazaar" not "Yu Garden", "Raffles City Mall" not the sky bridge). Driverless taxi rides are not free.
- Labels: short English names (fit one line at 76 px Anton, about 26 characters max).
- Opening: 2 striking shots of the city (night skyline, famous street). Ending: 2 night skyline / landmark shots that read well behind white text in the top third.

### 2. Find footage on Douyin (TikHub, about $0.30)
```bash
python3 -I scripts/dysearch.py $W/search <key> "<Chinese keyword>" 2      # key = short topic id, no underscores
```
One key per place plus `hookA`, `hookB`, `endA`, `endB`; run them in parallel (`&` with `sleep 1`). Use the Chinese name (English names often find nothing). Follow up with 1–2 more keywords where results are thin or off-topic (news reposts, food, apartment ads, talking heads). Choose **vertical** results (h > w), on-topic, high likes, short; download ~6 per topic:
```bash
python3 -I scripts/dydl.py $W/search $W/raw key:awemeid key:awemeid ...
python3 -I scripts/sheet1.py $W/raw $W/s1 1 && python3 -I scripts/topic_sheets.py $W/s1 $W/topic
```

### 3. Pick 22 shots (look at the frames, don't guess)
Read every `$W/topic/<key>.jpg` (1 frame per second, timestamps on each frame). For each slot pick a clip + in-point where the window is one continuous, steady, good-looking shot with no burned-in subtitles, no presenter talking, no letterbox bars. Slot lengths (s): 1.43, 1.17 | then pairs ~1.6/1.3 per place | ending 1.43, 1.60 (exact values: `CUTS` in `scripts/common.py`; with `speed` the clip uses length × speed seconds).

Write `$W/plan.json`:
```json
{"city": "Beijing",
 "shots": [["hookA_7651933270904877563", 2.5, "HOOK"], ["hookB_...", 2.0, "HOOK"],
           ["temple_...", 4.5, "Lama Temple"], ["temple_...", 3.0, "Lama Temple"], ... 9 places x 2 ...,
           ["endA_...", 2.0, "END"], ["endB_...", 3.0, "END"]],
 "blur": {"10": [[220, 1390, 640, 120]]},
 "precrop": {"13": "crop=720:956:0:162"},
 "speed": {"16": 0.76}}
```
`shots` = 22 entries [clip id (file name without .mp4), in-point seconds, label]; both shots of a place carry the same label. `blur`/`precrop`/`speed` keys are 0-based shot indexes.

### 4. QA before rendering (both are required)
```bash
python3 -I scripts/cutscan.py $W/plan.json $W/raw
python3 -I scripts/check.py $W/plan.json $W/raw $W/chkA.jpg 0,1,2,3,4,5,6,7   # then 8-14 and 15-21
```
- `cutscan`: a single score > 0.3 is a cut inside the window: move the in-point (often just 0.05–0.15 s later fixes a cut on the first frame) or slow the shot with `speed` (≥ 0.75) so it ends before the cut. Steady 0.1–0.25 rows are camera motion: fine.
- Read the 0.2 s check sheets: no cut, flash frame, title card, presenter, person walking out of frame, black bars. Burned-in Chinese subtitles or watermarks: grab a gridded frame (`ffmpeg -ss T -i clip -frames:v 1 -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,drawgrid=w=100:h=100:t=1:c=yellow@0.7"`) and add a `blur` box (output 1080×1920 coordinates) or pick another shot. Letterboxed clip: measure the bars and add a `precrop`.

### 5. Render
```bash
scripts/get_song.sh $W        # downloads the reference reel once -> $W/song.mp4 (checks it is 31.84 s)
python3 -I scripts/render.py $W/plan.json $W/raw $W/song.mp4 $W/<city>_free.mp4
```
It must print `unplanned cuts at none`. Then grab frames at 1.0, ~4, ~15, ~25, 30.5 s and look at them: text readable, correct city, no leftover subtitles. Fix and re-render if anything is off.

### 6. Post as a trial reel
Use the `instagram-trial-reel` skill (dry run, then `--yes`) with graduation `MANUAL` and this caption (place names in video order):
```
<City> is expensive… but these 9 places cost $0 🤑

📍 <Place 1>
...
📍 <Place 9>

DM us for a free personalized itinerary 📩

#<city> #chinatravel #<city>travel #freethingstodo #travelchina
```
The user has authorised the daily run to publish without asking each time (scheduled task, Nov 13 2026). Never post more than one reel per day from the daily run.

### 7. Record and report
```bash
python3 -I scripts/history.py add "<City>" <permalink> <media_id> "Place 1|Place 2|...|Place 9"
```
Commit `history.json`, the `.ig.json` logs and `$W/plan.json` (copy to `plans/<date>_<city>.json` in this skill) and push to the working branch. Report: city, places, permalink, TikHub calls used, anything you had to compromise on.

## Known issues
- The song is copyrighted: Instagram blocks each reel in ~22 countries ("may contain content owned by a rights holder"). The user knows. **Never tap or call anything that "restores" a blocked video.**
- Douyin clips belong to their creators (blur their watermarks/subtitles; don't add their handles).
- TikHub search: `scripts/dysearch.py` uses `/api/v1/douyin/search/fetch_video_search_v2` ($0.01 per page). Douyin play URLs expire after a few hours: download the same day you search.
