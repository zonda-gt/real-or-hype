---
name: real-or-hype-video
description: Plan, script, review footage for, and edit "Real or Hype?" short-form videos (Instagram Reels / TikTok, under 40 s) where the creator reacts to a viral clip of a place (Shanghai / China travel), visits it, tests the claim and gives a verdict. Use for episode research, narration scripts, footage selection, rough cuts, and re-edits of this series.
---

# Real or Hype? — episode workflow

The creator reacts to a viral video of a place, goes there, tests the claim, and gives a verdict.
Series name **Real or Hype?** (not "Fact or Hype", which belongs to the reference creator @itstundeanthony). Verdict wording: "Trees: real. Mall: hype."
Reference episode: 1000 Trees, final = v13 (Nov 2026). Pipeline: `scripts/v13_render.py` → `scripts/subs.py` (burn with `ass=...:fontsdir=`) → `scripts/add_sfx.py` is the template for new episodes.

## Pre-delivery checklist (run before sending any cut)

1. **Colour**: every HLG/HDR source (`color_transfer=arib-std-b67`, i.e. all iPhone IMG_* clips) is tone-mapped to BT.709; no saturation boost. Make a before/after frame if anything changed.
2. **His real lines end in silence**: `scripts/cutcheck.py "$PWD" scripts/<render>.py` must print **ALL OK** (it exits 1 otherwise). It measures against each clip's own noise floor, because mall noise ~-38 dB defeats a fixed threshold. It needs ≥0.15 s of silence before the cut and no speech within 0.05 s after. **Never accept a FAIL.** If he runs straight into the next word, there is no safe cut: find **another take of the same words** (he usually repeats lines; e.g. "absolutely huge" came from take 1 at IMG_4855 25.50–27.30), splice takes as a jump cut, or end on b-roll.
3. **Don't trust Whisper alone for cut words**: it "completes" clipped words. Use the energy checks above; use Whisper only to confirm the right words are present.
4. **Narration never overlaps**: each AI line ends before the next starts, and the last line ends before the video does.
5. **Graphics sync to sung/spoken word onsets**: measure onsets from the audio envelope (not Whisper word times) and show each word's caption 2 frames *before* its onset.
6. **Subtitles** on every spoken line (`scripts/subs.py`): exact script text, timed from Whisper word stamps on the exact audio used (energy fallback), chunks of ≤3 words, current word yellow, Montserrat ExtraBold 66 px with a 6 px outline, MarginV 430 (hook style MarginV 130, below the viral card). Skip lines whose words are already on screen as big text ($20,000, the verdict ticks).
7. **No phrase said twice in a row** (e.g. the hook voice must not say "Real or hype?" right before the sting sings it).
8. **Scan every chosen shot at 0.1 s for things crossing the frame** (a scooter crossed him in <0.5 s and the 0.5 s review missed it): frame-difference on the lower half, reject spikes.
9. **Loudness**: his real lines are recorded ~19 dB quieter than the narration. Normalise every real-voice segment (`highpass=f=80,loudnorm=I=-16:TP=-1.5:LRA=11`) and check with `ebur128` that each sits within ~3 LU of the narration (-15 LUFS). Quiet line endings feel "cut off" even when they aren't.
10. Total under 40 s. Send a 540p preview, and keep the 1080p file.

## 1. Research (Bright Data only)

- `$BRIGHTDATA_API_TOKEN`. **Never Apify** (the user objected).
- Instagram Posts `gd_lk5ns7kz21pck8jpis`: scrape a reel by URL (trigger → `/progress/{id}` → `/snapshot/{id}`). There's no hashtag/keyword search on Instagram (profile URLs only). The Reels dataset `gd_lyclm20il4r5helnj` fails on single reels.
- TikTok Posts `gd_lu702nij2f790tmv9h`, `type=discover_new&discover_by=keyword`, `[{"search_keyword": "..."}]`: the way to find viral clips by topic. Takes 10–30 min, so run it in the background. The Discover API returns "Not found" on this account.
- Pick clips with a **checkable claim** (price, queue, "free", "thousands of trees"), not just plays. Prefer Shanghai.
- Reaction clip choice: same angle and daylight as his footage, recent, and a claim his test can answer.

## 2. Getting footage

- Never ask for tokens in chat; suggest environment secrets. If pasted anyway: `umask 077`, task use only, then remind him to log out of all devices.
- Alipan share: `POST api.alipan.com/v2/share_link/get_share_token`; list `/adrive/v2/file/list_by_share` (page with `marker`); previews with audio `/v2/file/get_share_link_video_preview_play_info` (Bearer + `x-share-token`), download the m3u8 with `ffmpeg -headers 'Referer: https://www.alipan.com/' -c copy`. Originals via `/v2/file/get_download_url`; files over ~100 MB, or anything after a token refresh, fail, so use the top FHD/QHD preview (`scripts/getfhd.sh`). Tokens last 2 h; refresh at `auth.alipan.com/v2/account/token`.
- Google Drive file: `drive.usercontent.google.com/download?id=<ID>&export=download&confirm=t`. Folder listing: `drive.google.com/embeddedfolderview?id=<FOLDER>`.

## 3. Footage review (before writing a word)

1. Transcribe every clip (`scripts/wtx.py`); check `volumedetect` first, because Whisper invents text on silent clips.
2. 6 frames per clip (`strips.py`), then every 2 s for clips over 20 s (`dense.py`), then **every 0.5 s at ≥200 px** for candidates (`big.py`), then the 0.1 s intrusion scan (checklist #8) on the chosen windows.
3. Choose for **looks**: him and the landmark in one frame, him interacting with the place, interior **architecture** (atrium, escalators, signature columns), and his "we're at the entrance…" piece to camera.
4. Verify each in/out point with a frame grab. Never label what you haven't verified.

## 4. Narration voice

He is **plain, nonchalant, honest**: name the thing, give the number, one flat opinion. No jokes, wordplay or attitude lines ("Don't ask about this chair" was cringe). Read-aloud test: would he say it to a friend? Only words he uses (no "kinda", "lowkey", "bonsai", "unreal"). About 60 words per 40 s.
His phrases: "First you get to this station…", "check this out", "the only thing is, it is $20,000", "absolutely huge", "overall…".

**Voice**: OpenAI `gpt-4o-mini-tts`, voice **cedar** (`scripts/oatts.py`, env `OPENAI_API_KEY`), with the instruction: *"Young guy in his twenties narrating a fast-paced travel reel. Upbeat but relaxed and nonchalant, like telling a friend. Natural and casual, not salesy, not an announcer. Quick pace."*
- Generate one line at a time with retries.
- Trim with `silenceremove ... start_threshold=-55dB:start_silence=0.03` (front) and `start_silence=0.08` (end), so word tails aren't eaten.
- Then `atempo` 1.27 (hook 1.23).
- **One voice for the whole video.** Echo and ballad mispronounce "mall". Fallback if there's no key: edge-tts `en-US-AndrewMultilingualNeural` via `scripts/tts.py`.
- Write verdicts so they can't be misheard: "Overall: trees, real. Mall, hype."

## 5. Edit format (v11 structure, ~39 s)

| Beat | What |
| --- | --- |
| Hook 0–5.3 s | Him full frame (silent deadpan). Viral clip as a rounded card on the left (594×1056 @ 54,634) with the @handle, **window shifted and sped (start 0.5 s, 1.3×) so the claim → turn → landmark reveal all show**. White pill "Real or Hype?". Hook VO states the claim only ("This mall in Shanghai has a thousand trees on it."). Clip music ducked to 0.22. |
| Punch 2 s | Series sting `gd/sting.mp3` ("Is It Real or Hype_.mp3", sung). Envelope onsets: Is 0.01, real 0.51, or 0.99, hype 1.34. Captions IS IT @0, REAL @0.45, OR HYPE? @0.93. Fade out from 1.95 s. |
| Bar | "☐ REAL OR ☐ HYPE 💩" (Anton) at the top until the verdict. |
| Outside ~12 s | Station (clean window), bike with the landmark behind him, panel shot (viral clip inset ONLINE over his grey shot REAL LIFE), him at the planter wall, close-ups, him with the sculptures. |
| Inside ~13 s | His entrance line (captioned), atrium/escalators, "Six floors here. Absolutely huge." (captioned), 1–2 shops, the price tag with his "$20,000" + yellow punch (price stated once). |
| Verdict ~10 s | Ticks are **colour-coded**: REAL = green box with ✓ and green word, plus a click; HYPE = red box with ✗ and red word 💩, plus a low buzz (`v13_verdict.py`, `sfx/buzz.wav`). **Narrated** over interior-architecture b-roll: the reason ("far from the city center, not much inside" → "only two or three days, skip it"), then the ticks TREES ☑ REAL / MALL ☑ HYPE 💩. |

Rules:
- Cuts every 1–2 s.
- **His talking clips 1.4×** (1.15× for one-word lines).
- At most one voice switch in the ending.
- One text style on screen at a time.
- Chinese-word clips (地铁, 商场) belong to a separate language video.
- Leave room for a trending sound added in Instagram.

Technical:
- Tone-map HLG: `zscale=tin=arib-std-b67:min=bt2020nc:pin=bt2020:t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p` (`full()` in the renderer).
- Place narration and overlays from **measured** segment lengths (ffprobe), and re-encode the concat audio with `aresample=async=1` (otherwise it drifts ~0.15 s).
- Overlays are PIL PNGs (`v8_overlays.py`, `v9_overlays_extra.py`); fonts are in `scripts/`.

## 5b. Sound effects (`scripts/add_sfx.py`, assets in `sfx/`)

- Whoosh into each section cut (station, "let's go inside", verdict), with its peak 0.305 s after start, landing on the cut. Pop when the ONLINE/REAL LIFE panel appears. Ding on the price tag (trim 0.45 s, before his voice starts). Click on each checkbox tick. Levels 0.4–0.7 under -15 LUFS speech; the speech window must not get quieter.
- Sources: **Openverse** API (`api.openverse.org/v1/audio/?q=...&license=cc0`, no key needed). Its Freesound results return 403 to automated downloads, so don't try to get around that. Wikimedia Commons results download fine **with a descriptive User-Agent** (they return 429 without one), but most "whoosh"/"pop" hits there are people saying the word. `ding.wav` (typewriter ding) and `click.wav` (karabiner) are CC0 from Wikimedia. `whoosh.wav` and `pop.wav` are synthesized (`scripts/synth_sfx.py`).
- Don't add a music bed: he adds a trending Instagram sound when posting.
- Tools assessed (Nov 2026): **Openverse** = yes, for SFX. **HyperFrames** (HeyGen, HTML→MP4, Node ≥22 + ffmpeg, `npx skills add heygen-com/hyperframes`) = optional, for animated captions (pop-in/bounce); not used yet. The "earshot" plugin = Claude Code notification sounds, not useful for videos.

## 6. Delivery

540p preview via SendUserFile; full file in the working directory. Script and shot list live in the user's Claude Doc "Shanghai: Fact or Hype? — Content Plan & Scripts".

## Mistakes log (why each rule exists)

| Mistake | Rule |
| --- | --- |
| Used Apify | Bright Data only |
| Scripted from thumbnails, no audio | Transcribe and do frame review first |
| 6 frames per clip; missed the best shots | 2 s / 0.5 s / 0.1 s passes |
| Picked the first usable second | Pick for looks |
| No interior architecture or entrance piece | Always include both |
| Caption-style jokes in narration | Plain voice rules (section 4) |
| Labelled an unverified model | Verify before labelling |
| Cropped the reaction video | Natural framing |
| Trusted Whisper on silent clips / on clipped words | Volume check; energy-based cut check |
| Words of his lines cut short (three times) | `cutcheck.py`, ≥0.15 s tail, cut in the energy dip |
| Audio drift ~0.15 s | Measured segment lengths |
| Parallel TTS requests failed | One at a time with retries |
| HDR clips not tone-mapped (washed, slightly off) | Tone-map HLG, no saturation boost |
| Hook VO and sting both said "real or hype" | No phrase twice in a row |
| "OR HYPE?" caption lagged the singing | Sync to envelope onsets, 2 frames early |
| Scooter crossed the shot unnoticed | 0.1 s intrusion scan |
| "huge" clipped again: the old checker used a fixed -38 dB threshold, which mall noise defeats, and a CUT result was accepted | Noise-relative `cutcheck.py`, never accept FAIL, use another take |
| Verdict ticks looked the same for REAL and HYPE | Green ✓ for REAL, red ✗ for HYPE, different sounds |
| His real lines ~19 dB quieter than the narration | loudnorm real-voice segments to -16 LUFS |
