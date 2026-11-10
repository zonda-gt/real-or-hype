---
name: real-or-hype-video
description: Plan, script, review footage for, and edit "Real or Hype?" short-form videos (Instagram Reels / TikTok, under 40 s) where the creator reacts to a viral clip of a place (Shanghai / China travel), visits it, tests the claim and gives a verdict. Use for episode research, narration scripts, footage selection, rough cuts, and re-edits of this series.
---

# Real or Hype? — episode workflow

The creator reacts to a viral video of a place, goes there, tests the claim, and gives a verdict.
Series name **Real or Hype?** (not "Fact or Hype", which belongs to the reference creator @itstundeanthony). Verdict wording: "Trees: real. Mall: hype."
Reference episode: 1000 Trees, final = trial reels A/B/C (Nov 2026). Pipeline: `scripts/vr_all.sh <dir> A B C` = `vr_render.py` (segments from `variants.py`; no creator handle) → `cutcheck.py` → `subs.py` → `add_sfx.py` → earshot `measure`. `v13_render.py` is the older single-video renderer and still shows the handle, so don't use it is the template for new episodes.

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
- Aliyun Drive (阿里云盘 / Alipan): use the `aliyunpan-login` skill. He approves a QR login once, then the CLI downloads originals of any size from his own drive. For a share link, have him save it to his drive first. **Always check every source**: each downloaded file's size must match the drive listing.
- Google Drive file: `drive.usercontent.google.com/download?id=<ID>&export=download&confirm=t`. Folder listing: `drive.google.com/embeddedfolderview?id=<FOLDER>`.

## 2b. Douyin B-roll (TikHub)

For real footage to replace or support shots (city aerials, robots, pandas, festivals), search Douyin through TikHub (`api.tikhub.io`, the key is injected by the proxy):
- `scripts/douyin_search.py "<中文关键词>" out.json 1` lists clips under 1 min sorted by likes (id, size, duration, likes, caption). Chinese keywords work best ("上海陆家嘴夜景航拍", "宇树机器人功夫").
- `scripts/douyin_dl.py <dir> <id> ...` downloads the best decodable version. **Search results only carry ByteDance `bvc2` streams (ffmpeg shows `codec unknown`) or 576p H.264**; the downloader calls `web/fetch_one_video`, which has H.264 1080p.
- Prefer landscape sources for a 4:3 or 16:9 frame; crop vertical ones only around a centred subject. Reject clips with burned-in titles, channel logos or subtitles.
- Run a frame-difference scan on each chosen window: Douyin edits have whip transitions and hard cuts that a 1 s contact sheet misses. If a shot is a few frames short, slow it slightly (50/60 fps sources take ~0.94× invisibly).
- Keep a shot list with each clip's author and link (`deliverables/shotlist.md`) for credits.

## 3. Footage review (before writing a word)

1. Transcribe every clip (`scripts/wtx.py`); check `volumedetect` first, because Whisper invents text on silent clips.
2. 6 frames per clip (`strips.py`), then every 2 s for clips over 20 s (`dense.py`), then **every 0.5 s at ≥200 px** for candidates (`big.py`), then the 0.1 s intrusion scan (checklist #8) on the chosen windows.
3. Choose for **looks**: him and the landmark in one frame, him interacting with the place, interior **architecture** (atrium, escalators, signature columns), and his "we're at the entrance…" piece to camera.
4. Verify each in/out point with a frame grab. Never label what you haven't verified.

## 4. Narration voice

He is **plain, nonchalant, honest**: name the thing, give the number, one flat opinion. No jokes, wordplay or attitude lines ("Don't ask about this chair" was cringe). Read-aloud test: would he say it to a friend? Only words he uses (no "kinda", "lowkey", "bonsai", "unreal"). About 60 words per 40 s.
His phrases: "First you get to this station…", "check this out", "the only thing is, it is $20,000", "absolutely huge", "overall…".

**Script style: keep the plain style above (variant A).** We tested another successful creator's formula (variant D: "Don't go… until you watch this", "First thing?", "But here's the thing…", "Would you still go?"). The creator judged that **the original script is better**, so don't use that formula.

**Hook narration: being tested.** A = one claim line ("This mall in Shanghai has a thousand trees on it."). **A0 = no hook narration at all**: the reaction and the viral clip's own captions and audio carry it, and the clip's audio is raised to 0.95 (`HOOKVOL`) so the hook matches the body's loudness (check both with `ebur128`; it was 4.5 dB quieter at 0.55). Whichever wins on watch time becomes the rule. **A hook without narration still gets one on-screen context line** (most viewers start muted): e.g. `The viral "1000 Trees" mall` with `Shanghai` in yellow underneath, Montserrat ExtraBold 64/48 px with a black outline, centred at the top (y≈120–260, above the "Real or Hype?" pill and clear of his face), from the first frame until the sting (`CONTEXT_TEXT` in `variants.py`). If narration is used, it only names the place or claim, under ~2.5 s, and never sounds salesy.

**Voice (fallback since the creator's clone, see below): ElevenLabs "Liam"** (voice id `TX3LPaxmHKxFdv7VOQHJ`, model `eleven_multilingual_v2`, stability 0.4, similarity 0.75, style 0.35, speaker boost), chosen by the creator from an audition of 6 ElevenLabs voices plus Cedar. Script: `scripts/eltts.py - <voice_id> "<text>" out.mp3` (`-` reads `ELEVENLABS_API_KEY`). Key: env `ELEVENLABS_API_KEY` (this key has text-to-speech and sound-generation permission only; it can't list voices or read the account, so use known voice ids).
- Trim with `silenceremove ... start_threshold=-55dB:start_silence=0.03` (front) and `start_silence=0.08` (end), then **`atempo=1.12`**. Liam's natural pace is close to Cedar at 1.27×.
- **After changing voice, check every line fits its shot** (line end + 0.05 s before the next line or real-voice segment starts). Lengthen the b-roll shot under a long line rather than speeding the voice past ~1.15×.
- To audition voices, render the same 3 lines per voice into one mp3 each and let the creator pick by ear. Measurements only rule out mispronunciations: Will and Charlie said "maul".
- **One male voice for the whole video**, matching the on-camera creator (a female narrator reads as an unseen co-host; only worth an A/B trial reel). His own cloned voice is now an option (below).
- **DEFAULT NARRATOR (from Nov 2026): his own cloned voice**, ElevenLabs Instant Voice Clone `KdPzirZUC0HY6WhfwyeE` ("Real or Hype - creator voice v2"). Made from a clean 63 s read of the series script in a quiet room (Voice Memos, 48 kHz), only `highpass=f=60,loudnorm=I=-18:TP=-2`, no noise removal. The first clone (from noisy mall to-camera clips) sounded wrong and was deleted: **clone only from clean, quiet reads**. If he records more of the script (the full read is ~2.5 min), re-clone from all of it. Liam stays the fallback. The key needs **Voices: Write** to create or delete voices.
  - Settings: stability 0.5, similarity 0.9, style 0.15, speaker boost, `eleven_multilingual_v2` (`scripts/eltts_s.py <keyfile> <voice_id> "<text>" out.mp3 '<settings json>'`). Same trim, then **`atempo=1.2`**: his natural pace is ~10% slower than Liam's, and at 1.12 the 1000 Trees cut ran 41 s.
  - Every line: generate, Whisper-check against the script, regenerate on mismatch (up to 3 takes).
  - **"mall" said alone ("Mall, hype.") comes out as "mole/more"** on every model. Test lines in the **final mix** (the SFX pre-roll can mask a word) and keep "mall" inside a phrase: verdict **"Overall: the trees are real. The mall is hype."** passed 4/4 mixed checks. In a narrated line ("This mall in Shanghai…") it's fine.
  - Slower voice means wider slots: run the gap check (each line ends ≥0.05 s before the next line or real-voice clip). A b-roll shot can't grow past the end of its source clip (O3 couldn't), so widen the neighbouring shot and take the time from an un-narrated shot. Variant `A0me` holds the result (`VODIRS`, `_ME_DUR`, `TICKS['A0me']`).
- **Chinese place names: write them in Chinese characters** ("Take line 3 or 4 to 中潭路."). `eleven_v3` then says them in Mandarin and the creator loved it; pinyin, even with tone marks, stays English-sounding. Subtitles show pinyin + "Lu" ("Zhongtan Lu."), since Montserrat has no CJK glyphs. Whisper may hear 中坛路 for 中潭路 (same sound); accept it.
  - **v3 for a whole script (variant `A0v3`, being tested)**: costs the same as v2 (~1 credit/char; Turbo/Flash 2.5 are 0.5). But v3 talks ~40% slower; the `speed` setting, stability 0/1 and "[speaking quickly]" tags barely help. Recipe: 3–6 takes per long line, keep the shortest one that passes Whisper, squeeze inner pauses (`silenceremove=stop_periods=-1:stop_duration=0.14:stop_threshold=-45dB:stop_silence=0.12`), per-line atempo 1.15–1.35 only as much as its shot needs, extend b-roll within its source length. 1000 Trees ran 40.6 s this way. `scripts/eltts_m.py` = `eltts_s.py` + model arg.
  - Fitting check: the verdict must END ≥0.3 s before the video ends (an earlier fit script checked the wrong direction).
- Fallbacks: OpenAI `gpt-4o-mini-tts` voice `cedar` (`scripts/oatts.py`, the instruction text is in its history), then edge-tts.
- Write verdicts so they can't be misheard: "Overall: trees, real. Mall, hype."

## 5. Edit format (v11 structure, ~39 s)

| Beat | What |
| --- | --- |
| Hook 0–5.3 s | Him full frame (silent deadpan). Viral clip as a rounded card on the left (594×1056 @ 54,634), **with no creator handle or credit on screen** (the creator's decision; suggest tagging the original creator in the post caption instead), **window shifted and sped (start 0.5 s, 1.3×) so the claim → turn → landmark reveal all show**. White pill "Real or Hype?". Hook VO states the claim only ("This mall in Shanghai has a thousand trees on it."). Clip music ducked to 0.22. |
| Punch 2 s | Series sting `gd/sting.mp3` ("Is It Real or Hype_.mp3", sung). Envelope onsets: Is 0.01, real 0.51, or 0.99, hype 1.34. Captions IS IT @0, REAL @0.45, OR HYPE? @0.93. Fade out from 1.95 s. |
| Bar | "☐ REAL OR ☐ HYPE 💩" (Anton) at the top until the verdict. |
| Outside ~12 s | Station (clean window), bike with the landmark behind him, panel shot (viral clip inset ONLINE over his grey shot REAL LIFE), him at the planter wall, close-ups, him with the sculptures. |
| Inside ~13 s | His entrance line (captioned), atrium/escalators, "Six floors here. Absolutely huge." (captioned), 1–2 shops, the price tag with his "$20,000" + yellow punch (price stated once). |
| Verdict ~10 s | Ticks are **colour-coded**: REAL = green box with ✓ and green word, plus the `mallet/up4` success chime; HYPE = red box with ✗ and red word 💩, plus a low buzz (`v13_verdict.py`, `sfx/buzz.wav`). **Narrated** over interior-architecture b-roll: the reason ("far from the city center, not much inside" → "only two or three days, skip it"), then the ticks TREES ☑ REAL / MALL ☑ HYPE 💩. |

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

## 5b. Sound effects and audio QA with earshot

**earshot** ([Leonxlnx/earshot](https://github.com/Leonxlnx/earshot), MIT, CPU only, no key) gives the agent "ears". Install once per session (~3 min + 1.1 GB of models):
```bash
git clone --depth 1 https://github.com/Leonxlnx/earshot && cd earshot && python3 -m venv .venv \
 && .venv/bin/python -m pip install -q torch --index-url https://download.pytorch.org/whl/cpu \
 && .venv/bin/python -m pip install -q -e . && .venv/bin/python -m earshot doctor --fetch
```
- **Pick effects by ranking, not by guessing**: render 5–7 candidates from its 252-sound bank (`earshot sfx render <id> -o x.wav [--dur 0.6 --apex 0.30]`), include the current sound, then `earshot rank "<what the moment needs>" *.wav`. Keep the one it calls *strong* and whose "sounds most like" reading fits. Episode 1 found that my synth pop "sounds like a kick drum" and my click was "no match" for a correct-answer chime.
- Current set (in `sfx/`, placed by `scripts/add_sfx.py`, with each effect's **peak** on its moment, every effect peak-normalised to -6 dBFS before its role volume):
  - whoosh `whoosh_fast/tight` (rendered dur 0.6, apex 0.30) into each section cut
  - pop `pop/0` when the ONLINE/REAL LIFE panel appears
  - typewriter ding on the price tag
  - REAL `mallet/up4` ("success chime", peak at 0.335 s)
  - HYPE: **ElevenLabs-generated buzzer** `sfx/buzz_el.wav` ("Quiz show incorrect answer buzzer, short", ranked strong by earshot against my weak synth buzz; peak at 0.345 s)
  - ElevenLabs sound generation (`POST /v1/sound-generation`) is worth trying for specific real-world sounds, but always rank the result with earshot: its whoosh and cash-register tries lost to the bank and the typewriter ding
- **Final QA**: `earshot timeline final.mp4 --video final.mp4` (gaps, loudness, sync of hits to cuts) and `earshot measure final.mp4`. Targets: about -15 LUFS integrated, **true peak ≤ -1 dBTP** (the final limiter is `alimiter=limit=0.84`), and no dead-air gap over ~0.5 s unless music will fill it.
- Its limits (README): genre and mood are "hints only"; it can't judge taste, speech content or licences, and it can't find music.
- Openverse (`api.openverse.org`, no key) is fine for CC0 effects. **Not for music**: almost all its music is Jamendo CC BY-NC-ND (non-commercial, no derivatives). Freesound blocks automated downloads (403), so don't try to get around that. Wikimedia needs a descriptive User-Agent.
- **Music**: the creator adds a trending sound in Instagram at about 10–15%, or sends a licensed track (Epidemic, Artlist or Pixabay) for me to bake in after the sting and cut to its beat. Top Shanghai travel TikToks (Nov 2026) most often used "No Reason" by Ryan.B. Episode 1's timeline showed 0.6–1.05 s dead-air gaps, which music fills.

## 5c. Trial-reel variants (`scripts/variants.py`, `scripts/vr_render.py`, `scripts/vr_all.sh`)

Make 3 versions that change **only the hook/angle**, and post them as Instagram Trial Reels with the same music:
- **A, claim hook**: reaction card + claim VO.
- **B, price shock**: open 1.5 s on the steadiest price-tag shot with his "$20,000" and the yellow punch, then the card with "This bike is in a mall in Shanghai with a thousand trees on it." The bike/price leaves the inside section (replaced by another shop shot).
- **C, how-to guide**: "Everyone's posting this mall in Shanghai. Here's how to get there." → "Take line 3 or 4 to Zhongtan Road, exit 3." → bike → his "Because you can get the best pictures from this park right here." with a BEST PHOTO SPOT label → the rest, with less shopping.

`variants.py` holds each segment list and its overlays; `vr_all.sh <dir> A B C` renders, cut-checks, subtitles, adds SFX and runs earshot `measure`, stopping on the first error. **Never move or replace source files while a render is running.** Open with a steady shot: scan the hook shot at 0.1 s for motion and start on the stillest window.

## 5d. Editable CapCut / JianYing projects (experimental)

`scripts/draft_media.py <dir> <VAR> <media_dir>` collects the variant's shots (rendered segments, colour already converted), graphics PNGs, narration, sound effects (gain baked in), the sting and a phrase-level SRT, plus `manifest.json`. `scripts/build_draft.py <jianying|capcut> <media_dir> <manifest> <out> <name>` (venv with `pip install pyJianYingDraft pycapcut`; pyJianYingDraft 0.3.1 uses `append_track(TrackSpec)`, pycapcut 0.0.4 uses `add_track`) writes the draft. Drafts store **absolute media paths**, so make Windows (`C:/RealOrHype/<name>_media`) and Mac (`/Users/Shared/RealOrHype/<name>_media`) copies by rewriting the paths, and ship each with its media folder and a README.
Gotchas: shot files can be a few ms shorter than their slot (stretch with `speed=mat.duration/slot`); audio lengths must come from the library's own material (ms precision); cap each audio clip before the next one on its track; SRT phrases must not overlap. Newer app versions encrypt drafts and may refuse generated ones, so ask the creator for the app version if a draft won't open. **Not yet confirmed to open in the creator's apps.**

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
| Two effects were wrong for their moment and I couldn't hear it | Rank effects with earshot before using them |
| B opened on a motion-blurred price tag | Scan the opening shot for motion and start on the stillest window |
| 9 of 17 clips were soft Alipan previews without anyone noticing | Download originals with the `aliyunpan-login` skill and check every file's size against the drive listing |
| True peak -0.2 dBTP | Final limiter ≤ -1 dBTP; check with `earshot measure` |
| Verdict ticks looked the same for REAL and HYPE | Green ✓ for REAL, red ✗ for HYPE, different sounds |
| His real lines ~19 dB quieter than the narration | loudnorm real-voice segments to -16 LUFS |
