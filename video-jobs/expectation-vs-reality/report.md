# Expectation vs reality: China spots, three versions

## What's in this folder

| File | What |
| --- | --- |
| `A_wrong-week_1080p.mp4` | **A, "Wrong week"** (34.8 s). Hook: *"China isn't too crowded. You just booked the wrong week."* |
| `B_photo-scam_1080p.mp4` | **B, "照骗 / photo scam"** (38.7 s). Hook: *"Every famous China photo has a trick. Here's the trick."* |
| `C_lets-get-real_1080p.mp4` | **C, "Let's get real"** (23.5 s), the flip from your IG reference. Hook: *"I knew it. China travel photos are fake."* |
| `previews/*_540p.mp4` | Small previews for your phone |
| `sources.csv` | Every clip used: aweme_id, link, author, Douyin ID, role, spot, seconds used per version, original caption |
| `qa/` | Watermark and face check proof: a CSV for every frame, plus the contact sheets I checked by eye |
| `pipeline/` | Scripts and the voiceover script, so the edit can be redone. API keys are read from the environment only. |

All three are 1080×1920, 30 fps, H.264 + AAC. They have **no music**: just the voiceover, word-by-word subtitles and three sound effects (a quiz buzzer on each REAL LIFE, a ding on each fix, a whoosh between spots). Loudness is -15.4 LUFS with true peak -2.2 dBTP, so there's room under trending audio at 10–15 %. They're ready for Instagram Trial Reels: same spots, different angle.

## What I made and why

Each spot gets three beats: **ONLINE** (yellow tag) → **REAL LIFE** (red tag + buzzer, the laugh) → **the fix** (green tag + ding: the time, viewpoint or quieter twin). The fix is the planner moment. It turns "don't go" into "go, but like this", and the ending sends people to **Comment "SPOTS"** for the best times.

The spots are the Bund and Wukang Mansion (Shanghai), Hongyadong (Chongqing) and the Great Wall (Badaling vs Jinshanling). I chose them because they had the strongest real contrasts on Douyin in the last 180 days, and each one had a fix I could show with real footage:

- **Bund**: Golden Week and summer crowds vs the same Bund at 5 a.m., empty (that clip's own caption says 早上5点).
- **Wukang**: the crowd on the crossing vs the empty-street shot.
- **Hongyadong**: the riverside packed in August vs the view from the Two Rivers night cruise.
- **Great Wall**: the misty, golden shots everyone saves are **Jinshanling** (the creators tag 金山岭). Badaling is the one with the queue. This is the strongest "planner" reveal, so B opens with it.

What I found during research shaped the angle. Almost every crowd clip was posted during Golden Week (Oct 1–7), the summer holidays or a weekend. So version A's opinion line is "you just booked the wrong week". B plays the 照骗 genre. C copies the structure of your IG reference (accuse, "let's get real", reveal) but in reverse: the crowds are real, and so are the photos if you go at the right time.

## Scripts (as spoken)

**A**: China isn't too crowded. / You just booked the wrong week. / The Bund. Summer holidays. / Same Bund, early morning. Go on a weekday. / Wukang Mansion. You came for the building. / You got the crossing. / Get there before eight. / Hongyadong online. / Hongyadong in August. / Watch it from the river instead. / And that misty Great Wall photo? / That's not Badaling. This is Badaling. / The photo is Jinshanling. Further out, way quieter. / Same China, right week. Comment SPOTS and I'll send you the best times.

**B**: Every famous China photo has a trick. / Here's the trick. / This Great Wall photo isn't Badaling. / This is Badaling. / The photo is Jinshanling. Trick one: go there. / The Bund at night, online. / The Bund at night, in summer. / Trick two: go at sunrise. / Wukang Mansion, with nobody around. / Wukang Mansion, with everybody. / Trick three: before eight a.m. / Hongyadong, shot by drone. / Hongyadong from the ground. / Trick four: see it from the river. / The photos aren't fake. They're just well timed. Comment SPOTS for the best times.

**C**: I knew it. China travel photos are fake. / Look at this. *(crowd montage: Bund, Wukang, Hongyadong, Badaling)* / Let's get real. / The Bund, at sunrise. / Wukang Mansion, before eight. / Hongyadong, from the river. / The Great Wall, at Jinshanling. / Same China. Just planned right. Comment SPOTS for the best times to go.

The only Chinese text I added is the 照骗? on B's opening card.

## Voice

The voice is ElevenLabs **Liam** (`TX3LPaxmHKxFdv7VOQHJ`), the same voice and settings as the Real or Hype series: `eleven_multilingual_v2`, stability 0.4, similarity 0.75, style 0.35, speaker boost on. Each line was trimmed, then sped up to 1.12×. There was no `video-jobs/hotel/report.md` in the repo, so you confirmed Liam.

Liam mangled some place names: "Badaling" came out as "bottling". I fed it phonetic spellings instead (Bah-dah-ling, Hong-yah-dong, Woo-kahng). The subtitles show the correct spelling. A Whisper re-transcription now hears "Badaling", "Hongyadong" and "Jinshanling". Whisper still writes Wukang as "Wukong", which is its own bias; the audio says woo-kahng. Give it one listen.

Word timings come from ElevenLabs' `/with-timestamps` endpoint. The subtitles and the COMMENT "SPOTS" card are timed from those, and the card lands 2 frames before "Comment".

## Spend

- **TikHub: about $0.55** (balance $4.135 → $3.581 while I worked). That covers 29 Douyin searches at $0.01, plus the reference reels and a few calls to `calculate_price`, which turned out to cost money. All video downloads went straight from Douyin's CDN at no cost. The balance now reads $9.39, so someone topped it up after I finished. I made no paid TikHub calls after $3.581.
- **ElevenLabs:** about 1,300 characters for the final lines, plus about 600 for the pronunciation fixes.
- **OpenAI:** a few minutes of Whisper, used to transcribe the reference reels and to check pronunciation (cents).

## Tips: where each one comes from (please double-check the ones marked ⚠️)

| Tip / claim on screen | Source |
| --- | --- |
| Misty / sunrise Great Wall shots are **Jinshanling** | **Sources**: the creators tag 金山岭长城 (长城老郭, 长城摄影师杨东) |
| Jinshanling is "further out, way quieter" than Badaling | **Well established** (Jinshanling is in Hebei, Badaling is the main Beijing tourist section). I gave no hours or distances. |
| Bund empty in the early morning / "at sunrise" | **Source**: clip 7657542861315213541's caption says 早上5点 (5 a.m.). ⚠️ The VO says "early morning" / "sunrise", not a time. |
| "Go on a weekday" | **Well established** (weekend and holiday peaks). Not from a specific clip. |
| Bund crowd = **Golden Week** | **Source**: clip 7691696825632647355, captioned 国庆假期第一天 and posted Oct 1 |
| Bund crowd = **summer holidays** | **Source**: clip 7666811861115543985, posted Jul 26. I'm reading the posting date as the filming date. |
| Hongyadong crowd "in August" | **Source**: clip 7676478856703111562, posted Aug 21. ⚠️ Filming date assumed to be the posting date. |
| Hongyadong "watch it from the river" | **Source**: clip 7684303159230392179's caption says the Two Rivers night cruise past Hongyadong wasn't crowded that night. ⚠️ That's one night; check the cruise times and prices you'd recommend. |
| Wukang "before 8 a.m." | ⚠️ **Well established advice, not from a source.** The empty-street shot under it has no stated filming time, so treat it as illustrative. |
| B: "Hongyadong, shot by drone" | **Source**: clip 7672366988765931195 is tagged #航拍重庆 |
| B: "The Bund at night, online" | ⚠️ That clip is the Pudong skyline light show seen *from* the Bund (外滩灯光秀), which is the view people mean by "the Bund at night". |

I used no queue times, prices or headcounts anywhere.

## Proof the watermark check passed

1. **Downloads:** every clip came from `play_addr` / `play_addr_h264`, the watermark-free stream. No `download_addr`.
2. **Clip windows:** before cutting, I reviewed each source at 1 s and then at 0.2–0.5 s steps. I chose in and out points that avoid creator text. For example, the 5 a.m. Bund clip puts captions (机位1/2…) on screen from 3.8 s, so I cut at 3.7 s.
3. **Automated OCR on every frame:** I rendered each version's footage on its own, before adding any of my text, and ran RapidOCR (Chinese + English) on **all 2,912 frames** (A 1,045 / B 1,162 / C 705). Every hit was scene text in the world: building signs (洪崖洞 / 洪崖洞民俗风貌区, 中国平安, 鹏景科技, a 武康大楼官方文创店 shop sign), a POLICE van and a T-shirt print. There were **0 creator handles, 0 抖音 / platform logos, 0 广告 tags and 0 burned-in creator subtitles.** Per-frame results are in `qa/A|B|C_every_frame.csv`, and close-ups of the hits are in `qa/ocr_hits_scene_text.jpg`.
4. **Manual pass:** I looked at every 0.5 s of each version myself (`qa/*_manual_check_*.jpg`). One white square on a Jinshanling watchtower turned out to be a blank plaque on the tower.
5. **Same footage as checked:** the final files are built from the exact footage render that was checked. I verified the files are byte-identical (md5) and then only added my own labels, subtitles and end card.

## Faces

Faces were scanned on every frame with the YuNet detector, flagging any face taller than 6 % of the frame. That check made me **drop ground-level Bund crowd shots** where faces were big and identifiable. I replaced them with crowds shot from behind or from above. I also cropped the Wukang crowd shot 1.25× from the top so the people at the bottom edge are out of frame. After those changes, 1 frame per version was flagged, and all three are false positives: a reflection, a car edge and a watchtower (`qa/face_flags_false_positives.jpg`). No faces of passers-by appear in close-up.

## Tried and dropped

- **Yu Garden:** beautiful night shots, but no strong recent "reality" crowd clip. **1000 Trees:** only 2 relevant posts in 180 days.
- **West Lake** (Hangzhou): a great pair exists. The Broken Bridge on Oct 5 (Golden Week) vs the empty causeway in the early morning (7692998034519438946 / 7641371707550340025). I left it out to keep to 4 spots. **It's ready for a part 2.**
- **Zhangjiajie 照骗:** the results were mostly news about AI-faked collapse rumours. Off-brand.
- Clips with burned-in creator marks I avoided: Wukang crowd 7642003356257288179 and 7670947833462599114 (photographer signature in the sky), Lujiazui aerial 7651606133589192372 (creator handle), and compilation 7703168335873877370 (subtitles, mixes in other cities).
- Cheaper TikHub search endpoints (`app/v3`, `web` search, $0.001–0.002) now return 404. Only the $0.01 v2 search worked.

## Posting notes

- Credit the creators in the caption. Their names and Douyin IDs are in `sources.csv`.
- Suggested test: post all three as Trial Reels with the same trending sound, then keep the one with the best watch time. My bet is A for saves and shares ("send to the friend you're going with"), and C for raw reach.
