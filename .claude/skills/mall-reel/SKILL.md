---
name: mall-reel
description: Make a dense 30-60 s Instagram Reel / TikTok that introduces a multi-spot place in Shanghai (mall, lifestyle district, street, old town, park) from Douyin b-roll plus an AI narration, in the style of travel creator @wynnejael — named highlights, one shot per phrase, small one-word captions, serif title card, handwritten labels. Covers research (Douyin + Doubao), footage search and checks, script, voice, edit, mix, QA and delivery. Use when asked for a video "like her", a mall/district intro video, or a re-edit of one.
---

# mall-reel

A **many-spot place** explained so that **every sentence tells the viewer something new**: what it is, 4–6 named highlights with one concrete detail each, how to get there, what's next door. **Length is not the goal, density is**: cut every sentence that doesn't add a fact; the video is as long as the facts. Example: `episodes/gatem/` (GATE M West Bund Dream Center, Nov 2026, final 33 s; `long_66s/` is the earlier version the user found padded). Look at these before starting:

- `reference/style_frames.jpg` — every on-screen text style, annotated with font, size and position.
- `reference/gatem_shots.jpg` — first/middle/last frame of the 46 shots of the long GATE M version: the pace and how each shot matches its words.
- `reference/script_example.md` — the final dense GATE M script, plus the padded 66 s version with what was wrong with each line.
- `scripts/gfx.py` — the exact text styles in code. **Never restyle by hand; change gfx.py.**

All scripts run from the **project dir** (e.g. `work/<place>/`), as `python3 -I .claude/skills/mall-reel/scripts/<x>.py` (below: `$S/<x>.py`). Put downloaded clips in their own folders; they are third-party footage and stay out of git.

## Target numbers (measured from her reels, matched by GATE M)

| | Her reels | Use |
|---|---|---|
| Length | 48–86 s | whatever the facts need (GATE M: 33 s). Never pad to reach a length |
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

**Density first** (the user's rule): every sentence must earn its place and keep attention. Before generating any voice run
`$S/script_audit.py` → must print **AUDIT PASS**. It fails on a content word said 3+ times (the 66 s version said "river" 8 times),
filler phrases ("one of the coolest places", "the whole place lights up", "full of shops and cafés", "everywhere") and any sentence
with no name / number / price / how-to. Then ask of each sentence: *would the viewer miss it if it were gone?* If not, cut it.

**The first 2–3 s must say WHAT and WHERE, in the voice AND on screen** (most viewers start muted and decide in 1–2 s; a place name like "GATE M" means nothing to a tourist):
- Voice hook: Shanghai + the surprise + a reveal, e.g. `Shanghai turned Asia's biggest cement factory into this.` (cut to the reveal shot on "into this").
- On screen: a **context headline**, not the name: `TITLE = ("SHANGHAI'S", 'Cement Factory', 'turned riverside hangout', 0.0, <start of the name line>, 'headline')`. Her equivalents: "Full body health checkup in Shanghai", "SHANGHAI'S Basement Seafood". The name comes next, with its sign shot.

Beats: **hook** (Shanghai + surprise + reveal, ≤3 s) → **name + where** → **walkthrough, one named spot after another** (name + one concrete detail: dish, price, size, year, what's inside) → **night/second wind** → **practical** (free?, metro line + station + exit) → **next door** ("then walk along the river to Tank Shanghai") → **CTA** (below).

- ~100–200 words, as few as the facts allow. Short joined sentences, second person, one idea per sentence.
- Say each thing once: the river, the silos, the name. Don't restate the hook later ("the silos are still standing" after "cement factory").
- No vague mood lines ("lights up", "chill vibes") and no seasonal events that are over (light festival, last winter's rink) unless the video is about them.
- Every noun needs a shot. **No clean footage → cut the spot from the script.**
- Present tense only for things confirmed current; old seasonal footage → "Last winter, they even had…".
- Chinese place names you want said in Mandarin: write them in characters (`龙耀路`), and add the caption replacement in `CAPTION_REPLACE`.
- Avoid: jokes, hype words, "here's the thing", "you won't believe", anything she wouldn't say to a friend.
- Prices: say them in **dollars** for the international audience ("about 25 dollars per person"); the label shows both (`¥180 ≈ $25 / person`). John's accent turned "yuan" into "yen".

### CTA (the account is a China travel agency: itinerary planning, bookings, on-the-ground help)
- **One ask, ~3 s, in "we" voice.** Two versions being tested (GATE M: `work/gatem5` vs `work/gatem5c`):
  - A `Comment WOW, and we'll plan your trip for you.` → sticker `('COMMENT "WOW"', 'WE PLAN YOUR TRIP')` (fewer, warmer leads)
  - C `Comment WOW for more incredible places in Shanghai.` → sticker `('COMMENT "WOW"', 'FOR MORE PLACES')` (more comments; the DM must deliver a real list of 8–10 places with pins, then the soft offer)
- Why: a comment is a lead (auto-DM it) and boosts reach; her reels' top comments are "address please / where is this", so people want this.
- Never stack asks (comment + follow + link). Agency pitch lives in the bio and the caption's last line, never as a hard sell in the voice.
- Caption line 1 repeats the CTA: `Comment WOW and we'll plan this into your Shanghai trip 👇`; the auto-DM sends the pin + route, then "we can book X and fit it into your itinerary" + one WhatsApp/booking link.
- A/B: render the same video with each ending (splice the new CTA line onto the same narration, see `work/gatem5c`) and post both as trial reels; compare comments + DMs per 1,000 views. "Follow us" (`work/gatem4b`) is the weakest ending for an agency. Later, a unique keyword per video (e.g. `GATEM`) tells you which video a lead came from.

## 4. Voice (always ElevenLabs **v3**: it's far livelier than v2 for the same voice — John: 11.9 vs 6.5 semitones of pitch movement)

| Voice | ID | When |
|---|---|---|
| **John - Passionate Founder** (young male, Korean-accented English, "energetic founder who loves to talk") | `PXo7njgt8slUVdtKa3La` | **Current default** (user's choice, Nov 2026). Shared-library voice; our key can use it directly. Music at −11 dB (−9 masked "Tank"/"Dock") |
| Matilda (female, closest to @wynnejael) | `XrExE9yKIg1WjnnlVkGX` | her-style female narration |

Find other library voices: `GET https://api.elevenlabs.io/v1/shared-voices?search=<name>&language=<ko|en…>&gender=male&page_size=30` (works with our key, unlike `/v1/voices`).

Matilda was chosen by comparing 14 takes of 8 female voices with her real narration (speaker-embedding similarity 0.53 vs ≤0.38 for the rest, same pitch, pitch range 13 vs her 11.8 semitones). `$S/vsim.py` repeats that comparison (needs a venv with `torch speechbrain soundfile`, and her voice separated with `demucs --two-stems=vocals`).

1. `script.txt` starts with `[excited] ` (v3 tag). Generate 3 takes, one at a time:
   `$S/el.py PXo7njgt8slUVdtKa3La eleven_v3 vo/take1 '{"stability":0.5,"similarity_boost":0.8}' "$(cat script.txt)"` (key `$ELEVENLABS_API_KEY`; `mp3_44100_128` only — 192 needs a higher tier).
2. Whisper-check each take against the script (see `qa.py` logic) and keep the one with no real word errors.
3. `$S/tighten.py 1.10 take2` (in the project dir; John needed 1.12, Matilda 1.08–1.17): shrinks pauses >0.30 s to 0.24 s, speeds up (1.08–1.17: pick the factor that lands 200–210 wpm; it prints wpm), loudnorms, and writes `vo/narr.wav` + `vo/words.json` (word, start, end on the final timeline, from ElevenLabs' character alignment; matches Whisper within ~0.03 s).

**Changing the voice or the CTA of a finished edit**: new project dir with the new `vo/` (tightened), then `$S/revoice.py <old_project>` re-times every cut, label and pill to the same words in the new narration (changed words are mapped proportionally), then `slivercheck.py` (timing shifts can create slivers; nudge the in-point or move a cut to a nearby word) and render.

## 4b. AI clip of the creator (Seedance 2.5, optional)

Ark video API (`$ARK_API_KEY`): `POST /api/v3/contents/generations/tasks`, model `doubao-seedance-2-5-260628`, `resolution 720p`, `ratio 9:16`, `duration 4` (minimum), `generate_audio false`, `watermark false`; poll `GET …/tasks/<id>`; download `content.video_url` within 24 h.
- The creator's face is a pre-registered Ark asset: `{"type":"image_url","image_url":{"url":"asset://asset-20261114110202-8gttx"},"role":"reference_image"}` (group `group-20261114110124-fsxjq`). Real faces can't be sent as plain images.
- Add real frames from the episode's footage as more `reference_image`s (base64 data URLs) and say in the prompt which is which (图片1 = person, 图片2 = scene, 图片3 = dish). Prompt in Chinese; end with 画面中只有这一个人物，无字幕，无文字，无水印.
- **Put him INSIDE a named spot from the script** (Wild Dock counter with the logo behind him, Gentle Monster's sculptures), not a generic view: the riverfront version looked like any river (user feedback).
- Cost: 4 s 720p = 87,300 tokens × ¥70/M = **¥6.11** per try (2.0 would be ~¥4.0 at ¥46/M). ~2 min per clip. Show it to the user before cutting it in.
- Cut in under the CTA (he waves / nods while the CTA plays); `CAPTION_SKIP` over it so captions don't cover the face. Example: `work/ai_clip/`, used in `work/gatem5`.
- Label the post with Instagram's AI info label.

## 5. Music

ElevenLabs Music (`POST /v1/music`), prompt in `episodes/gatem/music_prompt.txt`. Ask for **15 s more than the video** (tracks fade early) and "no breakdown, no fade-out"; generate 2–3, check level over time and that a Demucs vocal stem is silent (< −60 dB). Start the track past its quiet intro (`MUSIC` offset). Or leave music to an Instagram trending sound and render with very low music.

## 6. Edit

Copy `templates/edl_template.py` to `edl.py` (full example: `episodes/gatem/edl.py`). Crops are the optional 4th item of a shot, so they can't land on the wrong shot when shots are added or removed (that happened once: black bars on the sunset shot).
- One shot per phrase; list items get one shot each. `t0` = the word's onset from `vo/words.json`; the renderer cuts 0.07 s earlier.
- Open on the most beautiful wide shot (title card over the first ~2 s). End on a striking shot that holds ~3 s under the CTA sticker (it auto-shrinks to fit long text).
- **Captions sit in the screen centre** (y = 960, the user's choice), one word at a time. `CAPTION_SKIP = [(start, end)]` hides them while the same words are already on screen (the GATE M sign shot). Keep labels and pills off the centre band (y 880–1040).
- Labels: one per highlight shot (name, or one fact like `about ¥180 / person`), placed near the subject, never over a face. One info pill for the metro. Captions run all the time.
- Checks before rendering (all from the project dir):
  - `$S/checkshots.py` → look at **every** tile (crop applied): no burned-in text, no bars, no celebrity, no wrong shot.
  - `$S/slivercheck.py` → must print **ALL OK** (a shot must not clip 1–4 frames of a neighbouring source shot; GATE M had 5 at first, including a celebrity frame).
  - `$S/stylecheck.py out/style.jpg` → compare with `reference/style_frames.jpg` (its frames are uncropped sources, ignore their own text).
- `$S/render.py` (~4 min for 66 s): segments → graphics → mix → `out/final_1080.mp4`, `out/upload_ig.mp4` (CRF 20, for upload), `out/final_540.mp4` (preview).

## 7. QA and delivery

- `$S/script_audit.py` again (with `vo/words.json` it prints seconds per sentence) and `$S/qa.py` → must print **AUDIT PASS** / **QA PASS**: −14 ±1 LUFS, true peak ≤ −1.5, every script word heard over the music (spelling-only diffs are fine), no flash/black frames.
- Send `final_540.mp4` as the preview and `upload_ig.mp4` + `instagram_caption.txt` + `footage_sources.txt` as files.
- Caption format (`episodes/gatem/instagram_caption.txt`): hook line + emoji, 📍 name (Chinese) · address, 🚇 metro, then one line per highlight with building/price/tip, the "check before you go" caveats, then hashtags.
- Commit the project's scripts, edl, script, vo, music and the upload file; never `src/`, `segs/`, previews or intermediates (`.gitignore` like `work/gatem/.gitignore`).

## Costs (Nov 2026)

TikHub Douyin search $0.01/call (by far the main cost), video fetch $0.001. **Douyin only** (the user's choice): no TikTok searches or footage. GATE M deep version: ~30 searches + ~40 fetches ≈ $0.35. Doubao lite with web search: a few cents for 6–10 questions. ElevenLabs: ~3 v3 takes × ~1,300 characters + 1–3 music tracks.

## Mistakes log

| Mistake | Rule |
|---|---|
| 66 s version: good facts spread thin, "river" 8×, mood lines, an over festival and last winter's rink | `script_audit.py` must pass; length follows the facts |
| First version said "shops, cafés and restaurants": generic, no depth | 4–6 named spots, each with one concrete detail; research before scripting |
| Broad Douyin searches gave ~1 usable clip in 4 (burned-in subtitles) | Search per spot name for footage |
| Doubao suggested spots with no 2026 evidence (rooftop, McDonald's) | Present only what has a recent dated source; otherwise past tense or caption caveat |
| BLOOMARKET and McDonald's had no clean footage | Cut the spot rather than show the wrong footage |
| Renderer shifted in-points back with the cut lead and exposed frames of the previous source shot | In-points are used exactly; `slivercheck.py` must pass |
| Celebrity frame 1 frame inside a Gentle Monster shot | Scan brand/event clips at 0.25 s, keep windows inside clean shots |
| Crop given by shot index drifted onto the wrong shot after a re-edit | Crop is part of the shot entry |
| Tight script dropped "Shanghai" from the hook and the title said "GATE M": no context for a muted tourist | Hook says Shanghai; headline title gives context; name comes second |
| Centred caption "GATE" sat on the GATE M sign | `CAPTION_SKIP` for shots that already show the words |
| John said "yuan" like "yen" | Say prices in dollars; label shows ¥ and $ |
| Music at −9 dB masked "Tank" under the male voice | −11 dB for John; qa.py lists words lost in the mix |
| Watermark signature at ~80% height survived a 1.3 crop | Check the cropped frames; (1.5, 0.3) for corner signatures |
| 3:4 source was squashed | Renderer fills 9:16 with `force_original_aspect_ratio=increase` + centre crop |
| Music tracks faded out at ~45 s of 53 | Generate 15 s longer, use an offset, fade yourself |
| `urllib` default User-Agent got 403 from TikHub | Send `User-Agent: curl/8.5.0` |
| Doubao pro + web search returned 502 after 30 s | Use the lite model for web-search questions |
