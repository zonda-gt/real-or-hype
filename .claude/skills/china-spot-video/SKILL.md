---
name: china-spot-video
description: End to end, from place to posted reel with automatic DMs. Research, script, voice and edit narrated B-roll reels (Instagram / TikTok, 30–45 s) about one place in China that the creator has NOT necessarily visited: a hotel, attraction, restaurant or experience (first episode: Huzhou Giraffe Manor). Clips-first workflow modelled on @wynnejael's reels: place research with sources, Douyin footage via TikHub, script written to the shots, one continuous lively AI narration take, picture cut on the spoken nouns, collage + serif-title hook, handwritten labels, comment-keyword CTA, then set up that keyword's automatic DM reply and guide page on chinapal.co and post the reel (instagram-trial-reel skill). Makes three versions per place by default, each a different angle chosen from the research. Use for "make a video about <place>", new variants, voice auditions, or studying a reference creator. Not for the "Real or Hype?" reaction series (that is real-or-hype-video).
---

# China spot video (B-roll explainer series)

Separate series from Real or Hype?: no reaction, no sting, no verdict, and the creator usually hasn't been there.
Reference style: **@wynnejael** (Shanghai). Study notes with numbers: `reference/wynnejael_study.md`. Worked example: `episodes/giraffe-manor/`.

Order matters: **research → footage → shot inventory → script → voice → cut → graphics → mix → QA → CTA → deliver.**
The first giraffe cuts wrote the script before the footage arrived and generated narration line by line. Both made the edit worse (loose clip matching, stop-start voice). Never do that again.

Scripts are in `scripts/` (paths below are relative to this skill). An episode lives in a work dir (e.g. `work/<slug>/`, gitignored) with `broll/`, `plan.py`, `script.txt`.

## 0. Pick the place
Master list of every scouted place (status, hook, sources): `reference/places.csv`. Update it when a place is done, dropped or verified; details in `reference/scouting_2026-11.md`.

## 1. Research the place (always, before any footage)
Goal: a **fact sheet** in the episode README, where every claim has a source URL and a confidence (2+ sources / single / unverified).
- Basics: official name in **Chinese characters** (people search it on Trip.com, Dianping and Didi), district, address, opening year, how to get there from Shanghai or Hangzhou, opening hours.
- Prices: check them today on Trip.com/Ctrip, plus Douyin deal posts. Say whether a price is a deal or a list price. Convert to USD, and say "about".
- **The surprising stuff that makes people stop**, which is what the video is built around. Search English + Chinese: `<name> 攻略`, `<name> 叫早`, `<name> 宝宝 / 出生`, `<name> 多少只`, `<name> 夜晚`, `<name> 避雷` (criticisms), news (潮新闻, 浙江日报, local 日报).
  Giraffe Manor examples: an **animal wake-up call** (a raccoon or monkey comes to your villa), **giraffe calves born there** (one 1.85 m at birth), giraffes at the breakfast window.
- Comparisons that frame the value (Kenya's Giraffe Manor ~US$1,410+/person/night against ~¥1,000 here).
- Criticisms (animal welfare, crowds, "giraffes didn't come"). Know them even if they're not in the video.
- Run it as a background research agent while you search Douyin; it's quick. Use WebSearch plus the web-fetch agent; **no Apify**.
- **Douyin is a research source too, not just footage.** Guest videos reveal experiences that never get written up: the web researcher found no written source for the wake-up call, while 4 guest videos showed it. Record such facts as "✱ guest videos (ids)" and word them carefully ("Sometimes, a raccoon walks into your room").
- Do a second, deeper pass before scripting, and ask the research agent for *ranked, video-worthy* facts with figures and confidence. On the giraffe episode the second pass found the two best beats.
- Write the fact sheet into `episodes/<slug>/README.md` (see the giraffe one) together with a trip-guide outline for the CTA.

## 2. Footage (Douyin via TikHub; key is proxy-injected, header `Authorization: Bearer $TIKHUB_API_KEY`)
- Find clips: `python3 scripts/dysearch.py "<关键词>" out.json 1` (1 = most likes, 0 = relevance). Use several keywords: the place, each surprising fact (`长颈鹿庄园 叫早`), `<place> 早餐`, `<place> 房间`. A browser User-Agent is built in (without it Cloudflare returns 403 / 1010).
- Download originals: `scripts/dl_douyin.sh <workdir> <id> ...` gives 4K60 for good vlogs and checks each file's size. Big files at ~1.5 MB/s, so run 2–3 copies in parallel on **disjoint** id lists, in the background.
- Review: `scripts/sheet.py <clip> 2` (then 0.5 s for candidates), `scripts/cuts.sh <clip>` for the source's own cut points (an in/out must never cross one).
- Check each candidate for: burned-in subtitles (bottom band, so set `cut` in plan.py; 0.14 for most vlogs, 0.18 when the subtitle sits higher), watermarks (keep the crop away), camera-app UI ("4K 60FPS REC" means skip), **"虚拟演绎 仅供娱乐" labels (staged or AI: never present as real)**, a different branch of the same brand (there are Giraffe Manors in Dezhou, Xiamen, Jinan… check the location tag).
- 9:16 crops from 16:9 sources: test the crop x on single frames first (`render_cut` crops full height minus `cut`). The giraffe's head is usually off-centre.
- Record the source aweme ids in the episode README (internal only; captions never mention sources).

## 3. Shot inventory, then the script
**Every place gets THREE versions by default** (the creator's rule, Nov 2026): three different angles on the same place. Each has its own script and its own cut that **feels like a different video**. The keyword, CTA and caption stay the same on all three, so the trial reels compare the angle and nothing else.

**Different cuts, same clips allowed** (creator's rule): reusing the best clips is fine. What must differ is the feel:
- **Opening**: a different hook (the first 1.5 seconds) and hook format, e.g. a 2×2 collage, one full-screen hero shot, or a price/title card over a shot. Never the same opening moment.
- **Order**: a different shot order, following that version's script (walkthrough, comparison or numbered list). No two versions in roughly the same sequence.
- **Rhythm**: a different pace, e.g. one fast (about 0.8 s a shot), one relaxed (about 1.5 s), one in between. Cut on different words.
- **Graphics**: each version's own treatment, e.g. handwritten labels, price cards, or numbered #1–#4 stickers.
- **Reused clips**: if one appears in two versions, use a different moment or crop of it where possible.

**You choose the three angles** from the research and the footage. There's no fixed template, because a hotel, a bakery, a shop and a cave each have different stories. Find the three strongest *different* reasons someone would stop scrolling for this place. A good angle:
- has a hook you can say in one line and **show on frame 1**
- is backed by checked facts (the fact sheet) and real footage (the shot inventory). Drop an angle you can't show.
- answers a different question from the other two, so one version doesn't just reword another

Angles to consider (pick what fits; invent better ones):
- **the experience walkthrough**: what it's like, in the order you'd live it
- **a comparison**: the famous or expensive version elsewhere, the usual tourist choice, or the price punchline
- **an insider list**: "N things nobody tells you", practical tips plus one honest heads-up
- **the one signature thing**: a bakery's famous bun, a shop's strangest item
- **the story behind it**: the maker, the history, the "why does this exist"
- **a myth vs reality, or numbers** angle: a record, a size, a queue, a price

The giraffe trio is one example of a good set:
- **E2me "the full experience"**: [DfwVcgvFL6b](https://www.instagram.com/reel/DfwVcgvFL6b/), `script_E2.txt`
- **F "Kenya vs China"**: [DfwVlUTDETB](https://www.instagram.com/reel/DfwVlUTDETB/), `script_F.txt`
- **G "4 things nobody tells you"**: [DfwVrTRjjJK](https://www.instagram.com/reel/DfwVrTRjjJK/), `script_G.txt`

Write the three chosen angles, one line each with why, at the top of the episode README before scripting.
- Never repeat a hook line across versions.
- Use the creator's Seedance shots (section 10) in each version, on different lines.
- Name the files `<place>_A`, `_B` and `_C`, and send the three previews together.
- All three go out as trial reels with one caption. The Facebook reel is the creator's pick, or the leader by likes after a day.

- Make a table: shot (src, in, max length, crop x) and what it shows. Only real, verified content goes in (look at the frames).
- Write the script **from** the table. Her skeleton (see the study):
  1. Hook from frame 1: a surprising claim with a concrete detail ("There's a hotel in China where giraffes join you for breakfast.")
  2. Name + where + how far (from Shanghai)
  3. Walkthrough in the order you'd experience it, chained with movement words ("From the restaurant… Then one stops at your window… Outside…")
  4. The surprising facts from research, one line each
  5. A pivot: "But here's the part nobody expects."
  6. Price, with the comparison
  7. One practical tip ("Get there by six thirty for a window table.")
  8. CTA (section 9)
- Every sentence names something we can show; **nouns are cue points**. 120–150 words for 35–45 s. Short sentences, second person ("you"), concrete numbers. No "I" unless the creator really went there.
- Words TTS stumbles on: write Chinese place names in the most pronounceable form and Whisper-check them (John said "Huzhou" fine in 1 of 3 takes); "yuan" is often heard as "when". Keep it inside a phrase ("a thousand yuan"), or say "RMB".

## 4. Voice
- Approved voices (creator's shortlist, Nov 2026, all ElevenLabs library voices usable by id):
  | voice | id | notes |
  |---|---|---|
  | **John "Passionate Founder"** (Korean accent) | `PXo7njgt8slUVdtKa3La` | **default**, liveliest of 30+ tested |
  | Andy Lin (Chinese accent, warm) | `h1i3CVVBUuF6s46cxUGG` | needs ~1.3× speed-up |
  | Chris "Light, Swift" (Chinese accent) | `Ph60oYke4Ty8rl2Wgtsn` | natural pace already fast |
- Settings (lively preset in `scripts/eleven.py`): multilingual v2, stability 0.3, similarity 0.75, style 0.55, speaker boost, `mp3_44100_128` (192 needs a higher tier).
- **One continuous take**: `python3 scripts/vo_take.py <workdir> <voice_id> 3 200` makes 3 takes, squeezes pauses, speeds up to ~200 wpm (max 1.25×), picks the take Whisper hears word-perfect, shrinks gaps over 0.35 s to 0.30 s, then writes `vo.wav` + `words.json` and prints `index:word@time` (indices = cue points).
- New voices: `scripts/voice_search.py --gender male --search "chinese accent"`, then `scripts/voice_audition.py lines.txt <dir> 20 Name:id ...` (same lines, fitted to 20 s, Whisper-checked, one reel to pick by ear; set `EARSHOT=<venv python>` to add a liveliness rank). Let the creator choose by ear; automatic similarity scores are only a guide.
- **Never clone a real third person's voice** (e.g. the reference creator). Your own clone is fine. If the creator appears on camera, the narration should be his own voice (or he appears silently); another person's voice over his face reads as dubbing.

## 5. Cut picture to the voice: `plan.py` + `scripts/render_cut.py <workdir>`
plan.py (see `episodes/giraffe-manor/plan_E2.py`):
```python
SRC={'<aweme_id>':{'cut':0.14}, ...}                 # bottom fraction to crop off (burned subtitles)
COLLAGE=[(src,t_in,max_src_secs,x)]*4               # TL,TR,BL,BR hook panels, until the first cue
HERO=(src,t_in,max_src_secs,x)                      # OR one full-screen hook shot instead of the collage (set COLLAGE=[])
CUES=[(word_idx,[(src,t_in,max_src_secs,x),...]),]  # shot(s) starting LEAD=0.10 s before that word
TAIL=1.3                                            # seconds after the last word
TITLE=["CHINA'S","Giraffe Hotel"]; TAG="breakfast included"
LABELS=[("capybara",word_idx),...]                  # handwritten label from that word to the next cut
CARDS=[("1 night + breakfast","¥1,000","about $140",i0,i1),...]
CTA=('Comment "GIRAFFE"',word_idx)                  # optional sticker at the end
```
- Shots fill their slot in order; if the slot is longer than the shots, they slow down. Flagged below 0.72× for 50/60 fps sources and 0.9× for 30 fps: then add a second shot instead.
- Cut rhythm like hers: 1.2–1.9 s per shot, a new shot on every listed noun (EKG, ENT, dental… each gets its own shot).
- **Looks beat novelty** (creator's rule): pick the most beautiful shot for each line (4K, good light, clean frame, subject well placed) even if another version already uses it. Variants may share B-roll; don't swap in weaker footage just to be different.
- Frame-exact (total frames = round(T·30)). HLG sources are tone-mapped automatically.

## 6. Graphics (her look): `scripts/graphics.py <workdir>`
- **Hook**: a 2×2 collage of the four best shots + a title in **DM Serif Display** on **pale-yellow highlight boxes** (like her "SHANGHAI'S / Basement Seafood"), plus a small handwritten tag (Chewy). Visible from frame 1.
- **Labels** on things in handwriting ("capybara", "6:30 AM"), like her "crispy pork belly".
- **Cards** (serif, big line on yellow) for numbers: price, comparison, a record ("1.85 m at birth").
- **Captions** (in finish.py): **one word at a time**, Poppins SemiBold **120** (`CAPTION_SIZE` in plan.py; the creator asked for bigger in Nov 2026: 54 was too small and 80 barely showed), uppercase, centred, not heavy, hidden under the title, cards and CTA.
- No emoji in fonts. DM Serif has no "≈", so write "about $140".

## 7. Mix + master: `scripts/finish.py <workdir> <name>`
VO + music bed (default `sfx/music_marimba_el.mp3`, ElevenLabs Music, earshot "strong" for a light, happy travel video) loudnormed, -8 dB (at -6 Whisper misheard words in the mix), sidechain-ducked under the voice; a whoosh out of the collage; soft pops on labels and cards. Master: **-15 LUFS, true peak ≤ -1 dBTP** (limiter 0.84). Writes `<name>_1080.mp4` + `<name>_540.mp4`.

## 8. QA (before sending)
- **Do the three feel different?** Run `python3 scripts/compare_cuts.py <workdirA> <workdirB> <workdirC>` after `render_cut.py`. It flags pairs with the same opening, a similar shot order or the same rhythm. Shared clips are listed for information only. Re-cut any flagged pair, then look at the three contact sheets side by side.
1. `scripts/sheet.py <name>_1080.mp4 0.5`: every cue shows its noun; no burned subtitles, watermarks or UI; labels sit on the right shot; nothing crops the subject's head off.
2. Whisper the final mix (real-or-hype-video `scripts/wtx.py`): every line is intelligible over the music.
3. Loudness printed by finish.py: -15 LUFS ±0.5, TP ≤ -1.
4. Facts on screen match the fact sheet (prices labelled "about", deals called deals).
5. Under ~45 s unless the creator asks for longer.

## 9. CTA (agreed with the creator)
- **Choose the keyword** while writing the script:
  - **One word** that names the place's hook, in capitals in the video (GIRAFFE, PANDA, CAVE, PEARL). Easy to spell on a phone; no spaces, numbers or emoji.
  - **Not already used:** check `CODE_RULES` in ChinaPal's `src/lib/inbox/code-rules.ts`. Avoid words people type anyway (CHINA, WOW, LOVE, HOTEL), which already trigger other replies or fire by accident.
  - **If a word is taken**, use the place's second hook (REDPANDA → PANDAHOTEL, for example) and keep the same word in the voice-over, the end sticker and the caption.
- In the video, the last ~3 s: **comment-keyword offer**, specific to this place: "Comment **the word castle**, and we'll send you the full guide." Say "the word" (the voice blurred "Comment castle" into "Comet castle"), and say "we", since the team replies. plus a handwritten sticker (`CTA` in plan.py). Comments are the strongest ranking signal, and DMs build a list.
- Caption: hook + CTA keyword + 3–5 hashtags. **Never mention AI-generated clips or footage sources (Douyin etc.)** in captions (creator's standing rule).
- Deliver what was promised: a one-page guide (Chinese name for taxis and Trip.com, how to get there, booking and prices with the date checked, the best-time tip, nearby, apps: Alipay / DiDi / Trip.com, and a footer "Want a full China itinerary? Reply PLAN"). It is sent automatically: see "The DM side of the CTA" below.
- A/B as trial reels with the same music: comment-keyword CTA vs "Follow for more".

### The DM side of the CTA (ChinaPal repo, `zonda-gt/ChinaPal`): automatic, never by hand
The creator does NOT use the /comment page. Every reel with a "Comment KEYWORD" CTA gets its reply in code, and it goes **live before the reel is posted**:
1. **Guide page:** an itinerary-style place page at `/itinerary/p/<slug>`, built with ChinaPal's `itinerary-builder` skill. It has a cover, "Good to know" facts, a sample day or trip around the place with photos and Douyin videos, nearby picks, and "Want a plan like this?".
   - Publish it with `build_page.py <spec> --code` (step 6b of that skill), which needs no database access.
   - Examples: `giraffe-hotel-v2` and `hogwarts-bakery-shanghai` (spec in `episodes/apoli-bakery/README.md`).
   - The older format, a `/discover/<city>/<slug>` JSON (`src/data/discover/`), is fine for a single venue; if the place already has one, link the new page to it.
   - Photos go in `public/uploads/...`, never `/media/`, because that path never reaches the site.
   - Build it from the episode fact sheet and hedge single-source facts.
2. **The reply**: add an entry to `src/lib/inbox/code-rules.ts` with a NEW random UUID (`python3 -c "import uuid;print(uuid.uuid4())"`).
   - Fields:
     - **keyword:** lower-case, matching the video's CTA
     - **public replies:** 2 options, one per line
     - **opener:** short, one line plus 👇
     - **button:** at most 20 characters
     - **message:** guide link + 3 tips
     - **follow-up**
     - `explore: true`
   - `media_id: null` (every post) is fine when the keyword is unique; otherwise use the reel's media id.
   - For Shanghai places the team now uses `trip: true` (the trip questions after the guide) instead of `explore: true`. CASTLE is an example.
3. **Explore cards**: add the place to a vibe in `src/lib/inbox/explore-data.ts` with `guide:` set, and a 1200×628 photo in `public/uploads/explore/` with no captions or watermarks.
4. Run `npm run test:inbox`, `npx tsc --noEmit` and `npx next build`.
5. Open a PR, wait for the Vercel check, then merge. The creator asked for this to be automatic, so merging is pre-approved for this flow.
6. Check that `https://www.chinapal.co/discover/<city>/<slug>` and its photos return 200. **Only then post the reel.**

What happens after that:
- The site copies the reply into the database after the next Instagram webhook. The first time, it also answers matching comments from the last 7 days, so a reel posted before its reply still gets its DMs.
- Each comment gets one DM at most.

Then people go through: the button → the guide link → explore buttons (more places by vibe, or Plan my trip → 4 one-tap questions) → the sales agent. Who answered what, and who's a 🔥 hot lead, shows on /comment → People. That page is read-only for these replies.

Same rule as the captions: DMs and guide pages never mention AI clips or where footage came from.

## 10. The creator on screen, and AI video
- The best personal touch is **real footage of the creator**: a reaction to the clip on his phone, browsing the booking page, on-the-move B-roll, a to-camera hook and CTA. Never let the narration claim he was there.
- **Don't generate AI clips of him at a place he hasn't visited** (it misleads viewers, and Instagram expects an AI label on realistic AI video of people).
- Seedance (Volcano Engine Ark, `ark.cn-beijing.volces.com`, key proxy-injected). **Default model: Seedance 2.5 `doubao-seedance-2-5-260628`** (creator's choice from Nov 2026; activated 14 Nov 2026; clip length 4–30 s per provider docs, so generate 4 s). Fallbacks: `doubao-seedance-2-0-260128`, `-2-0-mini-260615`. Costs measured on 2.0: 480p 4 s ≈ 40.6k tokens ≈ ¥1.9; 720p 4 s = 87.3k tokens ≈ ¥4.0. Measured on 2.5 (22 Nov 2026): 720p 9:16 5 s, text only, no audio = 108.9k tokens.
- The creator **may** choose to appear via Seedance (his decision; done on E2me at his request; he chose no AI label and no source credits in captions). Recipe: his verified portrait asset `asset://asset-20261114110202-8gttx` (real faces only work as verified assets; a `group-…` id is rejected) + a 9:16 frame of the real place as a second `reference_image` (data URL), Chinese prompt describing one simple action + "竖屏，手机实拍质感，自然柔和的日光，真实感，镜头轻微手持晃动", model `doubao-seedance-2-5-260628`, 720p, `generate_audio:false`, `watermark:false`. Poll `GET /api/v3/contents/generations/tasks/<id>`, download `content.video_url` (expires in 24 h). **Cut AI shots like every other shot** (same 1.0–1.7 s rhythm, on the matching words; no special time limit, the creator's final call after trying 1 s / 0.5 s / 0.8 s / ≤1 s). **Prompt for natural, understated behaviour** (one calm action; "表情自然平静，带一点淡淡的微笑，动作缓慢自然，不夸张，不大笑"): "惊喜地笑着" produced an over-animated face. Use 2+ clips in different scenes (breakfast window, capybara pool…) so they don't read as one moment. Ask before paid jobs above 480p; the classifier blocks unconfirmed ones.

## 11. Deliver: the whole order, end to end
When the creator says "make a video about <place>" (and post it), do all of this without asking them to touch any page:
1. Steps 0–8 for **all three versions** (section 3): research, footage, choose three angles, three scripts with the same keyword, voice, cut, graphics, mix, QA.
2. **Send the three previews** (540p) together, and get the creator's OK on the edits.
3. **Set up the DM side** ("The DM side of the CTA" above): guide page, the reply in `code-rules.ts`, explore card, tests, PR, wait for Vercel, merge, then check the guide link answers 200. ChinaPal must be in the session: `add_repo` zonda-gt/ChinaPal with push access.
4. **Post all three** as trial reels with the `instagram-trial-reel` skill: same caption on all three, the keyword in the caption, no AI or source mentions. Then post the creator's pick, or the leader by likes after a day, as the Facebook reel (the recipe is in that skill). That skill shows the creator the files and caption once and asks "Post these?" before publishing.
5. **After posting**, check within the hour that keyword comments are getting replies. Count the comments that have our public reply under them (the Graph API `/{media}/comments` with `replies`), and report the count.

540p previews via SendUserFile; keep the 1080p in the work dir (not committed, too big; tell the creator it's lost when the session ends unless uploaded). Commit the episode's plan, script, words.json, fact sheet and README under `episodes/<slug>/`. Trial reels: the `instagram-trial-reel` skill.

## Study a new reference creator
`scripts/ig_fetch.py <reel_url> <dir>` (TikHub) → `scripts/study_ref.py <dir>/<code>.mp4`: wpm, pauses, cut rhythm, a sheet of every shot with the words said over it, voice pitch range. Write the findings into `reference/<creator>_study.md`.

## Mistakes log
| Mistake | Rule |
|---|---|
| Script written before the footage was reviewed; lines with no matching shot | Shot inventory first, script from it |
| Narration made line by line, 0.2–0.5 s silences between lines; flat voice | One continuous take, lively preset, ~200 wpm, squeeze gaps |
| Facts gathered ad hoc; the most interesting facts (wake-up call, newborn calves) found only on a second pass | Research step with surprising-facts search, run first |
| Crops cut off giraffe heads | Test crop x on single frames; check the sheet |
| R-source subtitles leaked at cut 0.14 | Check the bottom band per source (0.18 there) |
| Hook title invisible on frame 1 (fade from t=0) | No fade for overlays starting at 0 |
| `urllib` to TikHub, 403 / error 1010 | Browser User-Agent |
| ElevenLabs `mp3_44100_192` returned 403 (tier) | `mp3_44100_128` |
| faster-whisper generator consumed twice (empty text) | `list(model.transcribe(...)[0])` |
| av version error in faster-whisper decode | Decode with ffmpeg to float32 and pass the array |
| A "wild reaction" clip carried 虚拟演绎 (staged) and another looked AI-made | Check labels; prefer real reactions at the venue |
| Kenya line shown over China footage | The card must name the place ("the one in Kenya") |
| Pop SFX fired on the word a label names; Whisper heard "Happy boroughs" / "your aff" | Pops land before the trigger word, at 0.18 (finish.py does this) |
| John said "capybaras" so Whisper heard "Happy bars" when the sentence started with it | A leading word ("Outside, capybaras…"); vo_take.py re-checks the FINAL vo.wav |
| Music at -6 dB blurred "Hold out" and "yuan" in the mix | Music at -8 dB (default); Whisper the full mix |
| Labels stay up until the next cue, not the next shot | Put a label on the cue word whose first shot shows the thing |
| The creator said "Apollo Cafe, the Harry Potter café"; it was APOLI ITABAKERY, a castle-style Italian bakery, not licensed Harry Potter | Pin down the real place (Chinese name, Douyin location tags) before downloading; say "the bakery people call Shanghai's Hogwarts", never official or themed |
| "Comment castle" was heard as "Comet Castle" / "Common Castle" | "Comment the word castle" |
| "yuan" heard as "wen" again | Say the dollar figure in the voice; show ¥ on the price card |
| Whisper writes made-up names as separate words ("a Polly") | Merge them in words.json before writing plan.py (indexes shift); don't use CAPTION_FIX for common words like "a" |
| compare_cuts flagged "same order" because one long walk-through source covers many scenes | It now compares source + 4 s windows; a scene change inside one file counts as a new moment |
