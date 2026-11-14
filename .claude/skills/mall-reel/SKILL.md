---
name: mall-reel
description: Make a 60-75 s Instagram Reel / TikTok that introduces a multi-spot place in Shanghai (mall, lifestyle district, street, old town, park) from Douyin b-roll plus an AI narration, in the style of travel creator @wynnejael — named highlights, one shot per phrase, small one-word captions, serif title card, handwritten labels. Covers research (Douyin + Doubao), footage search and checks, script, voice, edit, mix, QA and delivery. Use when asked for a video "like her", a mall/district intro video, or a re-edit of one.
---

# mall-reel

A **many-spot place** explained in 60–75 s: what it is, 4–6 named highlights with one concrete detail each, how to get there, what's next door. Example: `episodes/gatem/` (GATE M West Bund Dream Center, Nov 2026, 66 s). Look at these before starting:

- `reference/style_frames.jpg` — every on-screen text style, annotated with font, size and position.
- `reference/gatem_shots.jpg` — first/middle/last frame of all 46 shots of the GATE M video: the pace and how each shot matches its words.
- `reference/script_example.md` — the GATE M script beat by beat, with the reasons.
- `scripts/gfx.py` — the exact text styles in code. **Never restyle by hand; change gfx.py.**

All scripts run from the **project dir** (e.g. `work/<place>/`), as `python3 -I .claude/skills/mall-reel/scripts/<x>.py` (below: `$S/<x>.py`). Put downloaded clips in their own folders; they are third-party footage and stay out of git.

## Target numbers (measured from her reels, matched by GATE M)

| | Her reels | Use |
|---|---|---|
| Length | 48–86 s | 60–75 s |
| Voice pace | 200–240 wpm, voice covers ~100% of runtime | 205–215 wpm after tightening |
| Pauses | 0.2–0.5 s, never longer | max 0.30 s |
| Shot length | median 1.2–1.6 s, min ~0.7 | same; 2–3 s only for the hero/ending |
| Cuts | hard cuts only, no transitions | cut 0.07 s before the word |
| Music | steady bed 6–11 dB under the voice, no ducking (or SFX only) | music −9 dB after −16 LUFS normalise |
| Loudness | −14 LUFS | −14 LUFS, true peak ≤ −1.5 dBTP |

## 1. Research (three steps, ~$0.20 TikHub + a few cents Doubao)

1. **Broad Douyin search = what people actually go to.** Most-liked, last 180 days:
   `$S/tikhub.py search r_1.json "西岸梦中心 必逛" --sort 1 --days 180` (also `探店`, `攻略`, `新店`, the bare name), then
   `$S/tikhub.py descs r_*.json --days 200`. Descriptions list shops for free (one GATE M post listed 35+ with building numbers). Note what comes up repeatedly.
2. **Doubao verifies and adds detail** (`$ARK_API_KEY`, model `doubao-seed-2-1-lite-260915` with `web_search`; the pro model times out at the proxy's 30 s):
   `$S/doubao.py q1.json "<question>"` — ask per spot: what it is + English name, building/floor, **open now (latest dated source)**, the one most filmable detail (signature item, price, installation). Template in `episodes/gatem/research_notes.md`. Keep its sources.
   - Pick 4–6 spots: popular on Douyin **and** confirmed open **and** (step 3) with clean footage.
   - Doubao can be stale: if the newest source is >6 months old (GATE M: the silo rooftop, the McDonald's concept store), don't present it as current.
3. **Per-spot Douyin search = the footage.** `$S/tikhub.py search p_wd.json "野渡 西岸梦中心" --sort 1 --days 0 --dur 0-1` (sort 1 and 0). Specific names return focused clips; broad searches return talking-head guides with burned-in subtitles. The silo rooftop shots only appeared for `西岸梦中心 筒仓天台`.

Also run an English check (WebSearch) for official English names and what tourists already know. My WebSearch is US/English only — useless for shop-level facts, which is why Doubao exists here.

## 2. Footage

- Triage cheaply: `$S/tikhub.py list p_*.json`, then `$S/tikhub.py preview prev/ "p_*.json" <ids>` (576–720p from search results), then `$S/dense.py prev sheets 2.5 110 3` and **look at every sheet**.
- **Douyin only**, no TikTok.
- **Reject**: burned-in subtitles in the middle of the frame, watermarks you can't crop, talking heads, celebrities/brand ambassadors (crop to the product or skip), the reference creator's own videos, landscape clips (too soft when cropped to 9:16), rotated/sideways files.
- Bottom captions / letterbox bars are fixable with `CROP` (zoom 1.4 top-anchored drops text at 74–80%; letterboxed 720×960 content → 1.3334). Text in the middle of the frame is not fixable.
- HD for the clips you use: `$S/tikhub.py hd hd/ <ids>`. Takes 1080p HEVC when offered; **ByteVC2 (`is_h265=2`) can't be decoded**, so those fall back to 720p H.264 automatically.
- Name sources `A_night.mp4`, `Q_wilddock.mp4`… in `src/`. Shot catalogue: `$S/catalog.py <project>` (writes `cat/<clip>.jpg`, `shots.json`).
- Make `out/footage_sources.txt` (creator nickname, Douyin ID, link) for every clip used: the user credits or asks permission before posting.

## 3. Script (read `reference/script_example.md`)

Beats: **hook** (surprise + fact + "Shanghai", ≤5 s) → **name + where** → **walkthrough, one named spot after another** (name + one concrete detail: dish, price, size, year, what's inside) → **night/second wind** → **practical** (free?, metro line + station + exit) → **next door** ("Afterward, you can walk to…, so it's easy to make a whole evening out of it") → **"Follow me for more Shanghai spots worth exploring."**

- 200–240 words. Full joined sentences, second person, movement words ("Down by the water…", "Inside the silos…", "Once it gets dark…").
- Every noun needs a shot. **No clean footage → cut the spot from the script.**
- Present tense only for things confirmed current; old seasonal footage → "Last winter, they even had…".
- Chinese place names you want said in Mandarin: write them in characters (`龙耀路`), and add the caption replacement in `CAPTION_REPLACE`.
- Avoid: jokes, hype words, "here's the thing", "you won't believe", anything she wouldn't say to a friend.

## 4. Voice: ElevenLabs v3 "Matilda" (`XrExE9yKIg1WjnnlVkGX`)

Chosen by comparing 14 takes of 8 female voices with her real narration (speaker-embedding similarity 0.53 vs ≤0.38 for the rest, same pitch, pitch range 13 vs her 11.8 semitones). `$S/vsim.py` repeats that comparison (needs a venv with `torch speechbrain soundfile`, and her voice separated with `demucs --two-stems=vocals`).

1. `script.txt` starts with `[excited] ` (v3 tag). Generate 3 takes, one at a time:
   `$S/el.py XrExE9yKIg1WjnnlVkGX eleven_v3 vo/take1 '{"stability":0.5,"similarity_boost":0.8}' "$(cat script.txt)"` (key `$ELEVENLABS_API_KEY`; `mp3_44100_128` only — 192 needs a higher tier).
2. Whisper-check each take against the script (see `qa.py` logic) and keep the one with no real word errors.
3. `$S/tighten.py 1.08 take2` (in the project dir): shrinks pauses >0.30 s to 0.24 s, speeds up 8%, loudnorms, and writes `vo/narr.wav` + `vo/words.json` (word, start, end on the final timeline, from ElevenLabs' character alignment; matches Whisper within ~0.03 s).

## 5. Music

ElevenLabs Music (`POST /v1/music`), prompt in `episodes/gatem/music_prompt.txt`. Ask for **15 s more than the video** (tracks fade early) and "no breakdown, no fade-out"; generate 2–3, check level over time and that a Demucs vocal stem is silent (< −60 dB). Start the track past its quiet intro (`MUSIC` offset). Or leave music to an Instagram trending sound and render with very low music.

## 6. Edit

Copy `templates/edl_template.py` to `edl.py` (full example: `episodes/gatem/edl.py`).
- One shot per phrase; list items get one shot each. `t0` = the word's onset from `vo/words.json`; the renderer cuts 0.07 s earlier.
- Open on the most beautiful wide shot (title card over the first 2 shots, ~3 s). End on a striking shot that holds ~3 s under the follow sticker.
- Labels: one per highlight shot (name, or one fact like `about ¥180 / person`), placed near the subject, never over a face. One info pill for the metro. Captions run all the time.
- Checks before rendering (all from the project dir):
  - `$S/checkshots.py` → look at **every** tile (crop applied): no burned-in text, no bars, no celebrity, no wrong shot.
  - `$S/slivercheck.py` → must print **ALL OK** (a shot must not clip 1–4 frames of a neighbouring source shot; GATE M had 5 at first, including a celebrity frame).
  - `$S/stylecheck.py out/style.jpg` → compare with `reference/style_frames.jpg` (its frames are uncropped sources, ignore their own text).
- `$S/render.py` (~4 min for 66 s): segments → graphics → mix → `out/final_1080.mp4`, `out/upload_ig.mp4` (CRF 20, for upload), `out/final_540.mp4` (preview).

## 7. QA and delivery

- `$S/qa.py` → must print **QA PASS**: −14 ±1 LUFS, true peak ≤ −1.5, every script word heard over the music (spelling-only diffs are fine), no flash/black frames.
- Send `final_540.mp4` as the preview and `upload_ig.mp4` + `instagram_caption.txt` + `footage_sources.txt` as files.
- Caption format (`episodes/gatem/instagram_caption.txt`): hook line + emoji, 📍 name (Chinese) · address, 🚇 metro, then one line per highlight with building/price/tip, the "check before you go" caveats, then hashtags.
- Commit the project's scripts, edl, script, vo, music and the upload file; never `src/`, `segs/`, previews or intermediates (`.gitignore` like `work/gatem/.gitignore`).

## Costs (Nov 2026)

TikHub Douyin search $0.01/call (by far the main cost), video fetch $0.001. **Douyin only** (the user's choice): no TikTok searches or footage. GATE M deep version: ~30 searches + ~40 fetches ≈ $0.35. Doubao lite with web search: a few cents for 6–10 questions. ElevenLabs: ~3 v3 takes × ~1,300 characters + 1–3 music tracks.

## Mistakes log

| Mistake | Rule |
|---|---|
| First version said "shops, cafés and restaurants": generic, no depth | 4–6 named spots, each with one concrete detail; research before scripting |
| Broad Douyin searches gave ~1 usable clip in 4 (burned-in subtitles) | Search per spot name for footage |
| Doubao suggested spots with no 2026 evidence (rooftop, McDonald's) | Present only what has a recent dated source; otherwise past tense or caption caveat |
| BLOOMARKET and McDonald's had no clean footage | Cut the spot rather than show the wrong footage |
| Renderer shifted in-points back with the cut lead and exposed frames of the previous source shot | In-points are used exactly; `slivercheck.py` must pass |
| Celebrity frame 1 frame inside a Gentle Monster shot | Scan brand/event clips at 0.25 s, keep windows inside clean shots |
| 3:4 source was squashed | Renderer fills 9:16 with `force_original_aspect_ratio=increase` + centre crop |
| Music tracks faded out at ~45 s of 53 | Generate 15 s longer, use an offset, fade yourself |
| `urllib` default User-Agent got 403 from TikHub | Send `User-Agent: curl/8.5.0` |
| Doubao pro + web search returned 502 after 30 s | Use the lite model for web-search questions |
