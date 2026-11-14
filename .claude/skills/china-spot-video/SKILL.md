---
name: china-spot-video
description: Research, script, voice and edit narrated B-roll reels (Instagram / TikTok, 30–45 s) about one place in China that the creator has NOT necessarily visited: a hotel, attraction, restaurant or experience (first episode: Huzhou Giraffe Manor). Clips-first workflow modelled on @wynnejael's reels: place research with sources, Douyin footage via TikHub, script written to the shots, one continuous lively AI narration take, picture cut on the spoken nouns, collage + serif-title hook, handwritten labels, comment-keyword CTA. Use for "make a video about <place>", new variants, voice auditions, or studying a reference creator. Not for the "Real or Hype?" reaction series (that is real-or-hype-video).
---

# China spot video (B-roll explainer series)

Separate series from Real or Hype?: no reaction, no sting, no verdict, and the creator usually hasn't been there.
Reference style: **@wynnejael** (Shanghai). Study notes with numbers: `reference/wynnejael_study.md`. Worked example: `episodes/giraffe-manor/`.

Order matters: **research → footage → shot inventory → script → voice → cut → graphics → mix → QA → CTA → deliver.**
The first giraffe cuts wrote the script before the footage arrived and generated narration line by line. Both made the edit worse (loose clip matching, stop-start voice). Never do that again.

Scripts are in `scripts/` (paths below are relative to this skill). An episode lives in a work dir (e.g. `work/<slug>/`, gitignored) with `broll/`, `plan.py`, `script.txt`.

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
- Credit: list the source aweme ids and creators in the episode README, and tag the creators in the post caption.

## 3. Shot inventory, then the script
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
CUES=[(word_idx,[(src,t_in,max_src_secs,x),...]),]  # shot(s) starting LEAD=0.10 s before that word
TAIL=1.3                                            # seconds after the last word
TITLE=["CHINA'S","Giraffe Hotel"]; TAG="breakfast included"
LABELS=[("capybara",word_idx),...]                  # handwritten label from that word to the next cut
CARDS=[("1 night + breakfast","¥1,000","about $140",i0,i1),...]
CTA=('Comment "GIRAFFE"',word_idx)                  # optional sticker at the end
```
- Shots fill their slot in order; if the slot is longer than the shots, they slow down. Flagged below 0.72× for 50/60 fps sources and 0.9× for 30 fps: then add a second shot instead.
- Cut rhythm like hers: 1.2–1.9 s per shot, a new shot on every listed noun (EKG, ENT, dental… each gets its own shot).
- Frame-exact (total frames = round(T·30)). HLG sources are tone-mapped automatically.

## 6. Graphics (her look): `scripts/graphics.py <workdir>`
- **Hook**: a 2×2 collage of the four best shots + a title in **DM Serif Display** on **pale-yellow highlight boxes** (like her "SHANGHAI'S / Basement Seafood"), plus a small handwritten tag (Chewy). Visible from frame 1.
- **Labels** on things in handwriting ("capybara", "6:30 AM"), like her "crispy pork belly".
- **Cards** (serif, big line on yellow) for numbers: price, comparison, a record ("1.85 m at birth").
- **Captions** (in finish.py): **one word at a time**, Poppins SemiBold 54, uppercase, centred (the creator wanted captions centred and not heavy), hidden under the title, cards and CTA.
- No emoji in fonts. DM Serif has no "≈", so write "about $140".

## 7. Mix + master: `scripts/finish.py <workdir> <name>`
VO + music bed (default `sfx/music_marimba_el.mp3`, ElevenLabs Music, earshot "strong" for a light, happy travel video) loudnormed, -8 dB (at -6 Whisper misheard words in the mix), sidechain-ducked under the voice; a whoosh out of the collage; soft pops on labels and cards. Master: **-15 LUFS, true peak ≤ -1 dBTP** (limiter 0.84). Writes `<name>_1080.mp4` + `<name>_540.mp4`.

## 8. QA (before sending)
1. `scripts/sheet.py <name>_1080.mp4 0.5`: every cue shows its noun; no burned subtitles, watermarks or UI; labels sit on the right shot; nothing crops the subject's head off.
2. Whisper the final mix (real-or-hype-video `scripts/wtx.py`): every line is intelligible over the music.
3. Loudness printed by finish.py: -15 LUFS ±0.5, TP ≤ -1.
4. Facts on screen match the fact sheet (prices labelled "about", deals called deals).
5. Under ~45 s unless the creator asks for longer.

## 9. CTA (agreed with the creator)
- In the video, the last ~3 s: **comment-keyword offer**, specific to this place: "Comment **GIRAFFE** and I'll send you how to get there from Shanghai." plus a handwritten sticker (`CTA` in plan.py). Comments are the strongest ranking signal, and DMs build a list.
- Caption: the series promise "Follow for more places in China worth the trip" + credit tags.
- Deliver what was promised: a one-page guide (Chinese name for taxis and Trip.com, how to get there, booking and prices with the date checked, the best-time tip, nearby, apps: Alipay / DiDi / Trip.com, and a footer "Want a full China itinerary? Reply PLAN"). The creator handles DMs (or uses ManyChat; Instagram messaging API needs app review).
- A/B as trial reels with the same music: comment-keyword CTA vs "Follow for more".

## 10. The creator on screen, and AI video
- The best personal touch is **real footage of the creator**: a reaction to the clip on his phone, browsing the booking page, on-the-move B-roll, a to-camera hook and CTA. Never let the narration claim he was there.
- **Don't generate AI clips of him at a place he hasn't visited** (it misleads viewers, and Instagram expects an AI label on realistic AI video of people).
- Seedance (Volcano Engine Ark, `ark.cn-beijing.volces.com`, key proxy-injected). **Default model: Seedance 2.5 `doubao-seedance-2-5-260628`** (creator's choice from Nov 2026; activated 14 Nov 2026; clip length 4–30 s per provider docs, so generate 4 s). Fallbacks: `doubao-seedance-2-0-260128`, `-2-0-mini-260615`. Costs measured on 2.0: 480p 4 s ≈ 40.6k tokens ≈ ¥1.9; 720p 4 s = 87.3k tokens ≈ ¥4.0. **2.5 pricing not yet measured: read `usage.completion_tokens` from the first 2.5 job and record it here.**
- The creator **may** choose to appear via Seedance (his decision; done on E2me at his request; he chose no AI label and no source credits in captions). Recipe: his verified portrait asset `asset://asset-20261114110202-8gttx` (real faces only work as verified assets; a `group-…` id is rejected) + a 9:16 frame of the real place as a second `reference_image` (data URL), Chinese prompt describing one simple action + "竖屏，手机实拍质感，自然柔和的日光，真实感，镜头轻微手持晃动", model `doubao-seedance-2-5-260628`, 720p, `generate_audio:false`, `watermark:false`. Poll `GET /api/v3/contents/generations/tasks/<id>`, download `content.video_url` (expires in 24 h). **Cut AI shots like every other shot** (same 1.0–1.7 s rhythm, on the matching words; no special time limit, the creator's final call after trying 1 s / 0.5 s / 0.8 s / ≤1 s). **Prompt for natural, understated behaviour** (one calm action; "表情自然平静，带一点淡淡的微笑，动作缓慢自然，不夸张，不大笑"): "惊喜地笑着" produced an over-animated face. Use 2+ clips in different scenes (breakfast window, capybara pool…) so they don't read as one moment. Ask before paid jobs above 480p; the classifier blocks unconfirmed ones.

## 11. Deliver
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
