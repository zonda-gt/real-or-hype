# Honor store: Robot Phone + gadgets (Nov 2026)

This episode is **not** in the Real or Hype? format: there's no sting, no verdict bar and no ticks. It's a "cool stuff in a store" reel in the style of @jennaisblonde (Heytea × Cup Noodle, Suzhou qipao reels):
- serif hook title with an emoji (DM Serif Display, white, soft shadow)
- one-word captions in chunky caps (Montserrat ExtraBold 108, centred at y 1180)
- fast cuts of ~1.5 s
- first-person, upbeat voice-over ("of course I had to try it", "let me tell you right now", "Honestly?")
- a price card
- the CTA "Hit that follow button…"

Two variants differ in the narration angle:

| | A: Robot Phone hook (34.5 s) | B: Top-3 countdown (31.7 s) |
| --- | --- | --- |
| Hook title | "Honor's ROBOT phone?! 🤖" | "3 crazy gadgets in a phone store 🤯" (until 2.2 s, off before the HONOR sign shot) |
| Order | Robot Phone → price → telescope lens → cat massage gun | #3 cat massage gun → #2 telescope lens → #1 Robot Phone → price |

**A script:** Honor made a phone with a robot camera, and of course I had to try it. / If you don't know Honor, it's one of China's biggest phone brands. / *(his line)* Guys, check out this phone. I'm going to turn the camera on now. / The camera pops out on a tiny robot arm, and it moves on its own. / It's about fourteen hundred dollars. *(card: ¥9,999 ≈ $1,400)* / And let me tell you right now, that's not even the craziest thing in here. / They have a telescope lens for your phone. You can zoom across the whole building. / And this is a cat massage gun. It literally punches you in the face. / Honestly? It felt kind of nice. / Hit that follow button for more cool stuff in China.

**B script:** These are the three craziest things I found in a phone store in China. / Number three: a cat massage gun. / It punches you in the face with its little paws, and I don't hate it. / Number two: a telescope lens for your phone. / Clip it on, and you can zoom across the whole building. / And number one: the Honor Robot Phone. / *(his line)* / The camera pops out on a tiny robot arm, and it moves on its own. / It's about fourteen hundred dollars. Honestly? I'd get one. / Hit that follow button, because I'm showing you more things to do in China.

## Facts used (checked Nov 2026)
- Honor Robot Phone: launched in China on Aug 12 2026 at **9,999 yuan** (12/512 GB). Its 200MP main camera sits on a motorised gimbal arm.
- The "telescope" is Honor's **2.35× teleconverter kit** for the Magic8 Pro / RSR (about 200 mm equivalent).
- The cat massage gun's brand and price weren't found, so neither is stated.

## Footage
OneDrive folder "Honor shop" (20 × Samsung 1080p, rotated portrait). They were shot in HDR but arrived as 8-bit SDR BT.709 conversions, so there's nothing to tone-map. They look flat (YLOW ~60, SATAVG ~10), so `render.py` applies `GRADE` (contrast curve + saturation 1.1), which brings them to YLOW ~45 and SAT ~15, in line with her reels. A public `1drv.ms` folder link resolves anonymously:
POST `https://api-badgerp.svc.ms/v1.0/token` `{"appId":"5cbed6ac-a083-4e14-b191-b4ba07653de2"}`, then GET `https://my.microsoftpersonalcontent.com/_api/v2.0/shares/u!<base64url(link)>/driveitem?$expand=children` with `Authorization: Badger <token>` and `Prefer: autoredeem`. Each child has `@content.downloadUrl`. All sizes were checked.
Only `214352` has usable speech (his line, 0–3.35 s; cut at 3.5 s into silence, played at 1.2×). Whisper invents "Thanks for watching" on the other, quiet clips.

## Pipeline (work dir `/home/user/honor`: `src/`, `vo/`, `music/`, `out/`)
1. `wtx.py`: word stamps → `words.json`
2. `tts.py`: generates each line in the creator clone `KdPzirZUC0HY6WhfwyeE` (v2; stability 0.45, sim 0.9, **style 0.3** for a livelier read; trim; atempo 1.2) with a Whisper check.
   "the mall" became "them all" again, so the lines say "the whole building"; "Honor's Robot Phone" became "on his", so the line says "the Honor Robot Phone".
3. `overlays.py`: title, number and price PNGs. DM Serif Display came as a woff from the fontsource CDN, which PIL reads directly; the GitHub raw link returns 403.
4. `render.py A|B`: renders the shots, places narration per beat with a fit check (each line must end ≥0.1 s before its beat ends), adds captions and overlays, and mixes in **numpy**.
   The mix: shot ambience 0.35, narration loudnormed to -16, music (ElevenLabs Music, upbeat pop at 118 BPM) at -6 dB and ducked 9 dB under the narration and his line, effects peak-normalised, and `alimiter 0.84`. That gives **-15.4 LUFS** and a -1.4 dB peak.
   An ffmpeg `asplit`/`sidechaincompress` graph had produced a 0.075 s file, which is why the mix is done in numpy.

## Real-voice versions RA / RB (Nov 17)
He recorded the Honor clone script (`rec/read.wav`: 119 s, 48 kHz/24-bit mono, -34.5 LUFS, SNR ~26 dB) and ad-libbed much of it.
`cutrec.py` cuts it into narration lines and jump-cuts the inner pauses:
- every edge must be ≤10 dB over the noise floor (fine envelope at 10 ms); "phone" ran to 44.24, past Whisper's word end
- then highpass 80, `afftdn nf=-45` (for the video only, never for cloning), atempo 1.1
- each cut is Whisper-checked
He skipped the "Number three/two/one" lines, so RB carries the countdown with on-screen badges only.
`variants.py` `RA` (46.7 s) / `RB` (39.5 s); `render.py RA|RB`. Both measure about -15 LUFS and a -1.4 dB peak, and per-beat loudness stays within ±1.5 LU.
Captions follow what he actually says ("It's literally, look at me", "I have to try it").

**Clone v3** `Y8yZ6Nt4TKaEQy0ASAFX` ("Real or Hype - creator voice v3 (Honor read)"): IVC trained on this read (highpass 60, long pauses shortened, loudnorm -18, 97 s mp3 192k, `remove_background_noise=false`).
With stability 0.45, sim 0.9, style 0.3, Whisper passed 5/5 test lines, including "This mall…" and "The mall is hype". v2 still exists; the creator picks between them by ear (`exports/honor-store/clone_*_test.mp3`).

## New-clone versions A3 / B3 (Nov 17)
He chose generated narration over his own read. `VID=Y8yZ6Nt4TKaEQy0ASAFX VODIR=vo3 python3 tts.py <keys>` regenerates the A/B lines with clone v3 (same settings as v2).
v3 reads A about 10% faster than v2, so every line fits.
B3 is a copy of B with two shots lengthened (b2 → 214202 8.0–10.0, b6 → 213203 3.0–4.4), because v3 reads "Number three…" and "And number one…" slightly slower.
`render.py A3|B3` gives 34.5 s and 32.2 s at about -15.5 LUFS, and the final-mix Whisper check is clean.
`exports/honor-store/COMPARE_{A,B}_old-vs-new-clone.mp4` plays the v2 version and then the v3 version, labelled, so he can pick the narrator by ear.

## Excited versions AX / BX (Nov 17): FINAL
- The creator rejected both his own read and clone v3. **v3 was deleted** from ElevenLabs. The old clone `KdPzirZUC0HY6WhfwyeE` stays the narrator.
- **Why the clones sounded flat:** the model and settings, not his delivery. A livelier sample (v3) changed nothing under the same settings, because an instant clone copies timbre more than energy.
- **Measurement:** praat-parselmouth pitch range (5–95th percentile, in semitones), via `f0.py`.
  - his real excited read: 10–12 st
  - old clone on multilingual_v2 at 0.45/0.9/0.3: 8.7–9 st
  - multilingual_v2 with stability 0.2–0.3 and style 0.6–0.85: no better (7–11 st)
  - **`eleven_v3`, stability 0.5 ("natural"), sim 0.85, with tags** (`[excited]`, `[amazed]`, `[laughs]`, `[amused]`, `[impressed]`): 10.6–16 st
  - v3 creative (stability 0) went to 21 st and misread "cat" as "cap".
- `tts_x.py` makes 3 takes per line, trims, squeezes pauses and applies atempo 1.12, then Whisper-matches each take (ratio ≥0.93).
  It keeps the passing take whose range is closest to about 15 st. Takes over 20 st (usually laugh tags) read as overacted, and a1's take with "robot's camera" was rejected.
- v3 talks about 20% longer, so `render.py`'s **autofit** (AX/BX) lengthens the beat's shots from the end backwards within each source, or pulls in-points earlier.
  Watch for repeats: BX's b6 autofit ran into b8's 213203 footage, so BX extends the poster shot instead.
- Results: AX 39.8 s and BX 41.2 s, both about -15 LUFS with a -1.4 dB peak, and the final-mix Whisper check is clean.

## Variant C + posting (Nov 17)
- **CX** is the cat-punch hook with a comedy / bait-and-switch angle: "I let a cat punch me in the face… in a phone store in China" → "But that's not why I came here" → Robot Phone → price → telescope → "Which one would you try first? The cat, or the robot? Tell me in the comments!"
  - The title is "Punched by a cat in a phone store?! 😹". The lines `c1`–`c9` are in `tags_c.json`.
  - "the Honor store" came out as "honest store" in all 3 takes, so that line became "…why I came here".
  - Autofit had stretched shots into footage the next beat reuses, so CX sets those shots by hand. Always check for repeats after autofit.
  - 37.1 s, -14.6 LUFS.
- **Posted as trial reels (MANUAL graduation), same caption on all three:**
  - A: https://www.instagram.com/reel/Df2DfsBlMDI/
  - B: https://www.instagram.com/reel/Df2DopaD68P/
  - C: https://www.instagram.com/reel/Df2DuulD_q2/
