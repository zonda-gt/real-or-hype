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
OneDrive folder "Honor shop" (20 × Samsung 1080p SDR, rotated portrait, so no tone-map is needed). A public `1drv.ms` folder link resolves anonymously:
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
