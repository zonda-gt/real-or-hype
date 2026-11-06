# Report: "¥200 vs ¥6,000 hotel in Shanghai" (ChinaPal reel)

## What I made
| File | What |
|---|---|
| `final_A.mp4` | Hook A, no music (add trending audio in Instagram). 30.8 s, 1080x1920, 30 fps, H.264 CRF 19, AAC 192 kbps / 48 kHz, faststart |
| `final_B.mp4` | Hook B, no music, same body |
| `final_A_music.mp4` | Hook A with a quiet music bed. **The music is procedurally synthesised by `tools/musicbed.py`** (sine pads, plucks, noise shaker), so it is licence-free by construction |
| `caption.txt` | Instagram caption, hotels with district and price per night, CTA, 8 hashtags |
| `sources.csv` | Creator credits: aweme_id, URL, author, likes, shares, seconds used, hotel, price + where confirmed |
| `script.md` | Line-by-line script with a source column |
| `clips/*.md` | Three clip breakdowns + `clips/shortlist.md` (every clip considered and why it was dropped) |
| `reference/breakdown.md` | Breakdown of both reference reels + the editing recipe |
| `qa/watermark_report.json`, `qa/final_contact_sheet.jpg` | Watermark and quality check |
| `tools/` | Every script used, so the next reel can rerun the pipeline |

**Structure (30.8 s):**
- **0–5.5 s:** split-screen hook. Cheapest room on the left, the suite on the right, price tags popping in on the spoken numbers.
- **Three tiers, about 6 s each, cheapest first:** ¥200 Gefei → ¥500 Sheraton → ¥6,000 Banyan Tree, the biggest view last. Shots average about 1.4 s, 4–5 shots per tier.
- **Verdict at 23.0 s (75 %).**
- **CTA card from 26.6 s:** "Comment HOTEL…" both spoken and on screen.

## Decisions I made (and why)
1. **The title is "¥200 vs ¥6,000", not "¥300 vs ¥3,000".** I couldn't find a real ~¥3,000/night Shanghai room with both a confirmed price and usable footage, even after 5 extra targeted searches. The ¥2,000+ options were AI-generated (Peace Hotel, J Hotel), selfie-only (上影CHAO), or had no price at all (Ritz-Carlton, J Hotel). The ¥299 clip (Elegant Hotel) had only 1 s of room footage. I used the prices I could confirm rather than invent a "¥3,000" label. Details are in `clips/shortlist.md`.
2. **Tiers:**
   - **VX Gefei Hotel, North Bund (Huangxing Rd):** ¥200+/night. Spoken: "三天两晚仅需400多…每晚只要200多".
   - **Sheraton Pudong Riverside (浦东滨江喜来登):** ¥500+/night. Spoken: "一千出头 三天两晚 包含双早".
   - **Banyan Tree Shanghai On The Bund, Supreme River View Suite:** ¥6,000+/night. Desc: "6k+/晚的至尊江景套房".
3. **Verdict:** "My pick? The Sheraton. The view, without the suite price." Its footage shows the river and the Bund side from the room. Breakfast is included per the creator. The price is about 1/12 of the suite.
4. **Removing the creators' text:** both cheaper clips have burned-in Chinese subtitles and "广告" labels. I scaled them ×1.3 and cropped, so the top "广告" (Gefei), the second subtitle line and the bottom-right "广告" (Sheraton) fall outside the frame. The main subtitle band then lands under our own opaque, full-width price bar (y 1300–1540), which stays up for the whole tier. The Banyan Tree clip has no text at all. No blur or delogo was needed.
5. **The original clip audio is off.** The mix is voice plus quiet pop/whoosh effects from the channel's existing `sfx/` folder (`pop_es.wav`, `whoosh_es.wav`, from the earshot bank this repo already uses). Loudness is normalised with a two-pass `loudnorm` to −14 LUFS, true peak −1.5 dBTP.
6. **Download route:** most Douyin search results come as **ByteVC2 (`bvc2`), which ffmpeg cannot decode.** I fetched fresh details (`app/v3/fetch_one_video`) and took the HEVC/ByteVC1 1080p `bit_rate` entry, or H.264 1080p from the no-watermark `https://aweme.snssdk.com/aweme/v1/play/?video_id=<play_addr.uri>&ratio=1080p` endpoint. I never used `download_addr`.

## Hooks
- **A:** "Two hundred yuan versus six thousand yuan hotel in Shanghai. Is the expensive one worth thirty times more?" The ¥200+ tag pops at 0.05 s and ¥6,000+ at 1.1 s; the comparison is on screen within 1.2 s.
- **B:** "I plan China trips for a living. Here's what two hundred yuan gets you in Shanghai… versus six thousand." The boxes read CHEAPEST / PRICIEST until the prices pop at 2.05 s and 4.33 s.

The body audio is one ElevenLabs take shared by both versions; each hook was generated separately.

## Voice
- **ElevenLabs "Liam", voice_id `TX3LPaxmHKxFdv7VOQHJ`**, model `eleven_multilingual_v2`, stability 0.45, similarity 0.8, style 0.3, speaker boost.
- **Why Liam:** this API key has no `voices_read` permission (`GET /v1/voices` returned 401 `missing_permissions`), so I couldn't list voices. This repo's skill notes say the creator already picked Liam (a warm, natural young male voice) from an audition of 6 ElevenLabs voices. Reusing it keeps the channel's voice consistent and suits a friendly trip planner. **Reuse this voice_id for later videos.**
- **Pace:** gaps over 0.3 s were shortened, then the audio was sped up ×1.12 (the channel's standard Liam setting). Word timings were rebuilt from the `/with-timestamps` character alignment and shifted through the same edits.

## Spend
- **TikHub:** **about $0.52 at most attributable to this job; see the warning below.**
  - My call log (`search/calls.log`): 59 `douyin/search/fetch_video_search_v2` (3 of them HTTP 400), 6 `fetch_video_search_v3` (all returned empty `data`), 21 `douyin/app/v3/fetch_one_video`, 1 `instagram/v1/fetch_post_by_url`, 1 `tiktok/app/v3/fetch_one_video_by_share_url`, and 5 balance/usage checks.
  - **⚠️ Shared account:** the balance went from **$4.736 → $3.571 (−$1.165)** while this job ran, which on its face passes the $1.00 cap. But TikHub's `get_user_daily_usage` shows the key's account is **shared and active elsewhere**: 241 paid requests today, including endpoints this job never called (`instagram/v2/search_reels` ×71, `tiktok/app/v3/fetch_video_search_result` ×32, Xiaohongshu ×4, `fetch_video_search_v1` ×7, `calculate_price` ×12), and 105 v2 searches against my 59. Pro-rating the day's $1.434 by request count gives this job ≈ $0.52. I can't get an exact per-job figure from the API.
  - When I spotted the drop, I had already finished all TikHub work, and I made no further data calls. **If another job shares this key, give each job its own TikHub key (or sub-key) so the budget can be enforced exactly.**
- **ElevenLabs:** 982 characters of `eleven_multilingual_v2` (hook A 106, hook B 106, body 392 + a tightened re-take of 378). Roughly 1 credit per character, so about 1k credits. The dollar cost depends on the plan; I couldn't read it because the key has no `user_read` permission.
- **OpenAI:** Whisper `whisper-1` on 23 clips (about 11 min of audio, ≈ $0.07) and `gpt-4.1-mini` for 2 translations (< $0.01).

## Uncertain (please check before posting)
- **Prices are creator-quoted and promotional for two tiers.**
  - ¥200+ and ¥500+ are group-buy (团购) package prices averaged per night (¥400+ and ¥1,000+ for 2 nights). Both posts are ads: Gefei is flagged by Douyin's API and has a burned-in "广告" label; Sheraton has a burned-in "广告" label. The Sheraton clip itself says "部分日期需要加价" (some dates cost extra).
  - ¥6,000+ is from the Banyan Tree creator's caption only ("6k+/晚"), with no speech or receipt.
  - The on-screen labels say "Deal price" / "Deal" for the two package prices.
- **Sheraton English name:** the POI is 上海浦东滨江喜来登酒店. "Sheraton Pudong Riverside" is my literal translation, and the official English name may differ.
- **Gefei's location:** the POI says "北外滩黄兴路互联宝地T3店". Huangxing Rd is in Yangpu, not on the riverfront, so "North Bund" is the hotel's own branch name. I didn't claim a walk to the Bund.
- **"That's the Bund outside your window":** this follows the Sheraton creator's "右边是外滩 左边还是外滩" and the river view in the footage. The skyline in the day shot is hazy.
- **Banyan Tree clip engagement:** 124 likes / 13 shares is below the preferred 500 likes / 100 shares. It was the only luxury clip with a price per night I could confirm.
- **USD rate:** 1 USD = 6.6854 CNY (open.er-api.com, 2026-11-05). ¥200 ≈ $30, ¥500 ≈ $75, ¥6,000 ≈ $897, shown as "≈ $900".

## Watermark and quality check
**Result: PASS. All three finals have 0 flags** (`qa/watermark_report.json` → `summary`).

**How it was checked:**
- **Frames:** every 0.5 s at full resolution, plus every frame of the last 2 s. That is 118 frames per final, and for the sources the whole raw clip plus the exact seconds used.
- **OCR:** Tesseract 5 `chi_sim+eng` (psm 11, with psm 6 as a fallback on timeout). It flags 抖音/抖音号/Douyin/TikTok/小红书/小红书号/RED/快手/西瓜/广告, "@handle", numbers of 7+ digits, any confident 2+ character Chinese text, and QR codes.

| File | Frames | Flags | Length | Black frames | Loudness | True peak |
|---|---|---|---|---|---|---|
| final_A.mp4 | 118 | **0** | 30.8 s | 0 | −14.2 LUFS | −1.2 dBTP |
| final_B.mp4 | 118 | **0** | 30.8 s | 0 | −14.3 LUFS | −1.2 dBTP |
| final_A_music.mp4 | 118 | **0** | 30.8 s | 0 | −14.3 LUFS | −1.3 dBTP |

**Source clips.** The raw sources do carry text, and the report records how each was handled:
- **Gefei:** 40/145 raw frames flagged (Chinese subtitles, "广告"). The as-used crop with the price bar has **0** flags.
- **Sheraton:** 11/93 raw frames flagged (Chinese subtitles, "广告"). As-used: **0**.
- **Banyan Tree:** 0 raw flags. 1 as-used frame flagged as an undecoded QR candidate. By eye it is the bathroom window frame, a false positive.

**Problems the QA caught and I fixed before the final pass:**
1. **Hook subtitles:** the hook showed the Gefei subtitles for the first 2 s of B, and about 1 frame of A, because the price box arrived with the spoken price. The boxes are now up from frame 0.
2. **Safe area:** 23 text events crossed the right safe margin (x > 940). Captions now auto-fit, the tags and name lines are smaller, and `render.py` asserts the safe area for every text line. **Now 0 violations.**
3. **Real-world signage:** a Chinese neon bank sign on a building in the hook (real-world signage) was replaced with another shot.
4. **QR false positives:** `QRCodeDetector.detect()` gave false positives on window grids. The check now requires a decodable code, or a large square candidate for manual review.

**Other checks:**
- **Visual check:** I looked at `qa/final_contact_sheet.jpg` (4 corners, top 220 px, bottom 380 px of every final at 17 time points, including the last frames). It shows no logos, handles, app UI or end-screen animations. The only lettering is the Sheraton's own facade sign.
- **Caption sync:** caption on-time is the aligned word start minus 0.05 s. Measured against the voice-only track at every phrase start that follows silence (7 in A, 8 in B), the **max offset is 0.10 s**; mid-phrase captions come from ElevenLabs' character alignment. **No clipping:** sample peak is −1.2 dB.
- **Not committed to git:** videos, audio, downloads, frames and contact sheets. Only text deliverables and `tools/` are committed.
