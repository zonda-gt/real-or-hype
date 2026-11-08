# Shanghai hotels, cheap vs expensive: three reels

**Files (1080×1920, 30 fps, voice and light SFX, no music):**

| File | Angle | Length |
| --- | --- | --- |
| `A_same-tower-3-budgets.mp4` | "You don't need ¥68,000 a night to see this tower from your hotel." ¥500 → ¥1,000+ → ¥68,000 | 33.3 s |
| `B_500-vs-8979-bund-view.mp4` | "¥9,000 a night for a Bund view? Here's what ¥500 gets you." ¥500 vs the Bulgari | 28.4 s |
| `C_1000-vs-68000-tower.mp4` | "¥68,000 a night, or a thousand. Only one of these is worth it." Fanhua vs the room inside the Pearl Tower | 29.5 s |

540p previews are in `review/`. Every reel ends with "OUR PICK" and then "Comment HOTEL … for our Shanghai hotel list" on screen and in the voiceover.

## What I made and why

- **Why these angles.** On Douyin, the strongest hotel content is the single suite *inside* the Oriental Pearl Tower: those clips have 39K–59K shares each, far more than any normal hotel review. A planning audience doesn't need that suite. They need the cheap room that looks at the same tower. That contrast is the hook in A and C. B keeps your original "cheap vs luxury on the Bund" idea, using a real booking-app price.
- **Format, taken from your two references.** Both prices are stamped on screen within the first 2 seconds of a split screen. Each hotel then gets one section with a name chip (English plus the exact Chinese name, so people can search it on Trip.com or Ctrip), a price stamp with a ≈US$ line, and a note on where the price comes from. The verdict is honest and always picks the cheaper option. There's an opinion in the first 2 s of every version.
- **Look.** Full-bleed vertical footage wherever the source allows it, and full-bleed split screens for the comparisons. Landscape sources use a 4:5 frame. Every shot window was picked from per-frame scores (sharpness, shake, exposure), and creator transitions (flash, black and streak frames) were trimmed off both ends of every shot.
- **Prices on screen and their sources** (≈US$ at 6.7 CNY/USD, the September 2026 mid-market rate; rounded):

| Hotel | On screen | Source |
| --- | --- | --- |
| 上海外滩中南海滨酒店 (by Waibaidu Bridge) | ¥500, "package deal, 2025" | 娇子在游玩 [7498215911549046073](https://www.douyin.com/video/7498215911549046073) (Apr 2025): "三天两晚一千出头"; 小王去哪玩 [7241099825075260707](https://www.douyin.com/video/7241099825075260707) (Jun 2023): "相当于入住一晚只需五六百" |
| 沪上·繁花酒店 (北外滩滨江店) | ¥1,000+, "creator quote, Jun 2026" | 🎈潘哒遛娃 [7649926181692667109](https://www.douyin.com/video/7649926181692667109) (Jun 2026): "花1000多住进北外滩一线江景房" |
| 上海宝格丽酒店, Bund-view room | ¥8,979, "booking app, May 2026" | Daisy [7642685720855086065](https://www.douyin.com/video/7642685720855086065) (May 2026), booking screen at 0–6 s: 精选外滩景观房, 均¥8979起, 3晚总价¥26935, 61–62 m², 40–46层 |
| 东方明珠230空中酒店 | ¥68,000, "regular price" | 酒店控戴瑞克 [7000007563282550024](https://www.douyin.com/video/7000007563282550024) (2021) "6万8一晚"; Tracy崔继蓉 [6814673505490160907](https://www.douyin.com/video/6814673505490160907) (2020) "68000一晚"; 猪妹 [7639272604167081267](https://www.douyin.com/video/7639272604167081267) and 哔哔King [7638960623140902629](https://www.douyin.com/video/7638960623140902629) (May 2026) "日常价格6.8万一晚" |

- **Other claims and their sources.** For 中南海滨: "high-floor" (rooms on floors 16–25, from 优贤妈妈 and 小王去哪玩), "by Waibaidu Bridge" and "the Bund is right downstairs" (优贤妈妈, 上海宝藏姐, 曼曼去哪玩). For Fanhua: "floor-to-ceiling glass, river view" (少东, 李好梦想家, 潘哒遛娃). For the tower: "the only suite, 230 m up" (Tracy崔继蓉, 酒店控戴瑞克, OK姐). For Bulgari: "walk-in closet, double sinks, bathtub facing the skyline" (Daisy's own commentary).

## What I tried and dropped

- **The ¥300 vs ¥3,000 brief, done literally.** I couldn't find a ¥3,000 Bund hotel with a sourced price and clean footage. The Bulgari booking screen (¥8,979) was the best-sourced luxury price.
- **The hostel (壹号国际青旅, under ¥100).** The footage was a flat beige pod and a busy lobby. Swapped for 中南海滨 with your OK.
- **Bund Yazhi (under ¥300).** Every room shot scored shaky or soft, and the clip carries a 广告 tag.
- **¥28,888 for the tower.** It only appears in 2022 group-buy clips and in an August 2026 ad that uses AI-generated people. Also dropped: a Douyin "tower suite" clip whose window view showed the Pearl Tower itself, which is impossible from inside the tower.
- **v1/v2 layout (a square window on a blurred background).** It read as a template, so I rebuilt everything full-bleed.
- **Rendering bugs found by the every-frame check and fixed:** HEVC seek smears, a blank first frame from motion interpolation, a 1-px crop offset that turned the first frame of each zoomed shot into a smear, and the audio limiter auto-boosting peaks to 0 dBFS.

## Voice (reuse this)

- ElevenLabs **"Matilda"**, voice id `XrExE9yKIg1WjnnlVkGX`, model `eleven_multilingual_v2`, stability 0.45, similarity 0.75, style 0.30, speaker boost on.
- Leading and trailing silence trimmed, then played at **1.1× (`atempo=1.1`)**. Captions are word-synced from the `/with-timestamps` character alignment.
- Pronunciation checks: "Bund", "yuan" and "Lujiazui" read cleanly. "Waibaidu" comes out close to "Wai-bi-du", which I found acceptable.
- About 3,000 characters rendered in total, including the 3-voice audition and re-takes.

## Spend

- **TikHub:** 23 Douyin searches, 12 single-video (1080p) fetches, and 2 reference-reel lookups.
  - The balance went from $4.135 to $3.289 ($0.85) up to the last searches.
  - The account was then topped up externally (balance $9.39), so the last 4 HD fetches (about $0.01 each at the earlier rate) can't be read off the balance.
  - **Total ≈ $0.87.**
- **OpenAI:** Whisper transcription of about 45 clips, roughly 30 minutes of audio, ≈ $0.2.
- **ElevenLabs:** about 3,000 characters.

## Please double-check before posting

1. **Prices move.** ¥500 (中南海滨) and ¥1,000+ (Fanhua) are creator-quoted deal or package prices. Check today's rate on Trip.com for your audience's dates. If it has drifted a lot, the stamps are a one-line change.
2. **English names are my renderings, not official names:** "Hotel by Waibaidu Bridge" (上海外滩中南海滨酒店) and "Fanhua Hotel · North Bund" (沪上·繁花酒店). The Chinese names are exact, taken from Douyin location tags.
3. **The tower footage is from 2021 (Derek's video), so the interior may have been refreshed since.** The ¥68,000 regular price is quoted as recently as May 2026, and Douyin package deals have appeared below it.
4. **People in shots.** These are the original creators or their models, mostly from behind: Fanhua (幼儿园抢饭王's model at the window) and Bulgari (Daisy's reflection in the mirror). Credit them in the caption (see `sources.csv`).
5. **Foreign guests.** I haven't verified that each hotel accepts foreign passports on the specific booking channel. Worth confirming before you send your list.
6. **Music.** None is baked in, as asked. Add trending audio at about 10–15% under the voice. The voice track sits at about -16 LUFS with peaks around -1.6 dBFS.
7. **Brand names inside shots.** Bulgari's own name is visible on its key card and amenities, which is normal for a hotel review. Nanjing Road street signs appear in one night shot.

## Watermark and text proof

Every frame of every delivered reel was OCR'd: 998 + 852 + 885 = **2,735 frames, at full 1080×1920**. That's a 100% sample, not spot checks. Two renders were checked for each version:

1. **Footage-only render** (same cuts, no graphics or captions), to find any text that comes from the source clips.
2. **Final render.** Every detection was classified as either inside one of our own overlays (prices, labels, captions, CTA), or in-scene, meaning the same box also appears in the footage-only render.

| Version | Frames | Detections in our overlays | In-scene | Unexplained |
| --- | --- | --- | --- | --- |
| A | 998 | 6,134 | 22 | **0** |
| B | 852 | 6,012 | 19 | 1 → checked by eye: a rooftop sign on a Lujiazui skyscraper, identical in the footage-only render |
| C | 885 | 6,333 | 0 | **0** |

**What the in-scene text actually is.** I checked each one by eye: the 南京路步行街 street sign on the Nanjing Road night shot, rooftop signs on the Lujiazui skyline, the tower pod's railing (misread as letters), and the BVLGARI name on the Bulgari key card and on a bath-amenity bag. None of these is a watermark, platform logo, creator handle, 广告 tag or burned-in subtitle.

**How it stays clean.**
- Every shot window was chosen against a 4 fps OCR map of its source, with a 16 px margin around each crop.
- Crops sit entirely above or outside each creator's subtitle band and corner tags.
- Downloads use `play_addr` (watermark-free) only, never `download_addr`.
- Rendering found two problems that I fixed:
  - **Bulgari window sticker.** A faint privacy notice printed on the glass sat in the first 2 s of B's original opening. I moved the shot window past it.
  - **Smeared or black first frames.** Some shots started with a smeared or black frame from decoder warm-up and interpolation. I fixed the renderer.
- The delivered files carry exactly the video stream that was OCR'd. I checked this by md5: only the audio was re-limited afterwards.

**Visual QA at every frame (30 fps)**, checking for black frames, flashes, sub-0.4 s shots and blur dips:
- No black frames, flashes or one-frame shots remain.
- The only flags are 1–2 frame softness dips at section changes, where the hotel-name chip cross-fades. They're intended.
- I also reviewed each reel by eye at **4 frames per second**. The pages are in `review/frames_4fps/`.

Files: `proof/*_clean_ocr.txt` and `*_final_ocr.txt` (all strings found), `*_verify.json` (the classification), and `*_frame_qa.json`.

## Folder contents

- `*.mp4` final reels (gitignored) and `review/` (previews, still boards, voice audition; gitignored).
- `sources.csv`: every clip used, with aweme_id, link, author, Douyin id, date, location tag, versions, source seconds and ranges.
- `proof/`: per-frame OCR results for the footage-only and final renders.
- `pipeline/`: the scripts that made this. Keys are read only from environment variables, and nothing is stored.
