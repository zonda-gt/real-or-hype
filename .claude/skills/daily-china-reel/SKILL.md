---
name: daily-china-reel
description: Make and post the daily "If you like X, go to CITY" China travel reel (Douyin B-roll, the creator's ElevenLabs clone voice on v3, Kevin MacLeod CC BY music, ~25 s) as an Instagram trial reel. Use for the scheduled daily run, or when asked to make the next episode, change the content calendar, or rebuild an episode.
---

# Daily China travel reel

One ~25 s reel a day in the format the creator approved on 2026-11-10 ("recreation_30s_clone_v3" + Happy Bee, sped up ~1.2x):
8 lines of "If you like X, go to CITY", each split over two Douyin shots with the cut on "go to", then a 2-line outro.
Captions are small lowercase white text at 79 % height with the place in yellow. Narration is the creator's
own clone voice on `eleven_v3`, place names written in Chinese characters so they're said in Mandarin.
Free CC BY music by Kevin MacLeod sits ducked under the voice and is credited in the caption.
Reels are posted as **trial reels** (non-followers first, graduation MANUAL) on `steven_chinapal`.

Files here:
- `calendar.json`: the content plan, one entry per day. The run takes the first entry without `posted`.
- `history.json`: every Douyin clip id ever used (never reuse one), music in order of use, posted reels.
- `episodes/<date>-<slug>/`: episode.json, caption.txt, timeline.json and vo/lines.json of each reel (no media).
- `scripts/`: `dy.py` (TikHub Douyin search/download), `source.py` (candidates + review sheets per shot),
  `vo.py` (narration), `render.py` (edit + music + loudness), `caption.py`.

Needs env `TIKHUB_API_KEY` (proxy-injected), `ELEVENLABS_API_KEY`, `INSTAGRAM_ACCESS_TOKEN` (+`INSTAGRAM_USER_ID`),
and `pip install faster-whisper librosa`. ffmpeg is preinstalled.

## Daily run (about 20-30 min)

Work in a scratch dir, e.g. `W=/tmp/reel/$(date -u +%F)`. `S=<this skill>/scripts`.

1. **Pick the episode**: first `calendar.json` entry without `posted`. If its status is `built` and
   `/mnt/project-files/daily-reels/<date>-<slug>/` holds the video, skip to step 6.
   If fewer than 3 entries are left, draft 7 more in the same style (alternate a China-wide theme with a
   single-city edition, no city repeated within 7 days, seasonal where it fits) and list them in the report
   so the creator can change them.
2. **Write `$W/episode.json`** from the entry (see `episodes/2026-11-11-winter-china/episode.json` for the shape):
   per line `say` = "If you like X, go to <城市>." , `check` = "if you like X go to", `a.cap` = "if you like X",
   `b.cap` = "go to |City", and Douyin keywords `a.kw` (the X, shot in that place) and `b.kw` (the place's
   signature view, e.g. "<城市> 地标 航拍"). Outro lines: `"split": false`, one shot each. Set `hook` and `tags`.
3. **Narration**: `python3 $S/vo.py $W` (3 takes per line, Whisper must hear every English word, keeps the
   shortest). If a line fails twice, reword X. Voice total should be 21-24 s, giving a ~25 s reel.
4. **B-roll**: `python3 $S/source.py $W`, then look at every `$W/sheets/<shot>.jpg` and pick one clip + in-point per shot.
   - Must be real footage of that place. Reject AI-generated clips (too-perfect castles, painted auroras, drones
     flying in frame), other countries (a Matterhorn showed up in a "Snow Town" search) and look-alikes
     (Shenyang's palace is not the Forbidden City).
   - No big burned-in text or watermarks in the used 1-2 s. Small corner text: crop with `"zoom": 1.2-1.3`.
   - The 1.0-1.6 s after the in-point must be one continuous shot and visually strong.
   - No clip used twice in one reel, none from `history.json`.
   Weak sheet: `source.py $W --only l4b --kw-override "l4b=<新关键词>"`. Write picks as `"clip"`, `"in"` (and `"zoom"`).
5. **Edit**: `python3 $S/render.py $W` (picks the music track that lands most cuts on beats, skipping the last 3
   used), then `python3 $S/caption.py $W`. QA every time:
   - contact sheet `ffmpeg -i $W/final.mp4 -vf "fps=1,scale=180:-2,tile=9x3" -frames:v 1 $W/qa.jpg`, and look at it
     (wrong place, text burn-ins, black frames, a long frozen frame);
   - a Whisper transcript of `final.mp4` (`vo.words()`) reads every line; about -14 LUFS; 22-30 s; under 40 MB.
   Copy the video and `caption.txt` to `/mnt/project-files/daily-reels/<date>-<slug>/`.
6. **Post** with the `instagram-trial-reel` skill (dry run, then `--yes --caption-file $W/caption.txt`, graduation MANUAL),
   but only when `calendar.json` has `"auto_post": true` at the top level, which is set once the creator
   agrees the plan. Otherwise stop after step 5 and report the file for review.
7. **Record**: add the clip ids to `history.json.used_clips`, append the music, add a `posted` row
   (date, slug, permalink); set `posted` on the calendar entry; save episode.json, caption.txt, timeline.json and
   vo/lines.json under `episodes/<date>-<slug>/`; commit and push.
8. **Report** in one short message: the permalink (or the file), the theme, and anything odd.

## Notes
- Voice: `KdPzirZUC0HY6WhfwyeE` ("Real or Hype - creator voice v2"), v3, stability 0.5, similarity 0.9, style 0.15.
  v3 talks slowly, so inner pauses are squeezed and each line sped up (`vo_tempo` 1.3).
- Whisper hears Mandarin city names as nonsense ("Macca" for Mohe); only the English part is checked.
- Douyin streams in ByteVC2 don't decode; `dy.py` takes the H.264 address and rejects the rest.
- Clips belong to their Douyin creators; the caption credits them by nickname. If one objects, take the reel down.
- Tracks (CC BY 4.0, incompetech.com): Happy Bee, Life of Riley, Carefree, Wallpaper, Inspired, Easy Lemon,
  Bright Wish, Hyperfun, Funkorama, Sunshine A, Pamgaea, Merry Go. Downloaded to `music/` (gitignored) on first use.
