# Shanghai budget reel: AI room + "words behind my head" captions (Nov 2026)

This is a talking-head reel ("Would you fly to China just to see a panda? … 5 days in Shanghai for $906 … DM us"), filmed at a desk against a plain white wall. It's edited in the style of @viashaan's reel `DfMiYjYRbMI`. It's not in the Real or Hype? format.

## What the reference does (frame-by-frame review)
- **The fake room is a full AI video-to-video restyle, not a key.** At 30.0 s it reveals his real white flat. In the AI room his black hoodie is brown and his face is lit by the room's lamps: the whole frame was regenerated shot by shot, with a different room for each section.
- **Words behind the head:** a per-frame person matte, with the caption layer drawn between the room and him. The head covers only the lower part of the big word.
- **The caption style changes every phrase:**
  - a small sans lead-in plus a big serif-italic word
  - 3D extruded caps
  - glowing text
  - a gold 3D call to action
  - outline caps
  - a mono HUD
- Words blur in and blur out.
- **Also in the edit:** punch-in jump cuts, a face-tracking HUD, text kept clear of Instagram's buttons, and a wireframe → iris reveal of the real room.

## Why this episode uses a cut-out, not a restyle
- **Seedance 2.0 / 2.5 (Ark) rejects real faces** in a reference video unless the person is a verified "private real-person asset" (liveness check in the Ark console, then `asset://` IDs). It also only takes a reference video as a web URL. The creator chose not to verify, so we used the cut-out.
- Measured restyle prices, video input, 720p:
  - 2.0 mini: about ¥0.6 per second
  - 2.0: about ¥1.2 per second
  - 2.5: about ¥1.8 per second; it isn't activated on the account.
- **The session proxy cuts any request at about 30 s.** Seedream image edits with a photo usually took longer and failed with 502 "upstream request failed". A short text-only prompt sometimes fits: `room_plate_shanghai_night.jpg` came back in 32 s.
- **RobustVideoMatting (cloned repo + .pth) was blocked by the auto-mode classifier** as code from outside. MediaPipe's `selfie_multiclass_256x256` segmenter from pip (needs `apt-get install libegl1`) plus an OpenCV guided filter works well enough.

## Pipeline (work dir layout: `src/`, `work/`, `rs/`, `broll/`, `fonts/`, `models/`, `tools/`)
1. **Rough cut:** `edl.json` (source in/out) is cut from the HLG iPhone clip with the skill's tone-map, one segment at a time. A single filtergraph with 10 trims of a 60 fps HEVC was OOM-killed. Every join was checked with the noise-relative energy runs, then Whisper large-v3 on the cut.
2. **Matte:** `mpmatte.py roughcut.mp4 alpha.mkv` runs at ~8 fps on CPU. Bugs fixed:
   - The guided filter needs a **float** guide; a uint8 guide gives NaN.
   - The raw matte spreads 15–20 px past the body. Remap with `(a-0.45)/0.35` (the best of three tested).
3. **Faces + wall:** MediaPipe face detection on every frame. The clean wall is estimated from pixels outside the matte and filled with a normalised blur. It is used to **decontaminate** edge colours: `F = (I-(1-a)·wall)/a`.
4. **Room:** a Seedream text-to-image plate (no person, no desk), blurred with σ = 6 for depth of field.
5. **`render.py <work_dir> <out> [t0 t1]`:**
   - Layers per frame: room → behind-head words → him, graded warmer and darker with a lamp gradient from the left → the real table, kept with a static mask below y≈1521 and regraded to walnut (hands on the table keep the person grade) → front captions.
   - Also adds a faint cool rim light, vignette and grain.
   - `ZOOMS` sets the hard punch-ins; `BR` sets the b-roll windows and the crops that hide burned-in text.
   - `PH` sets the phrases: style, size and word onset. Captions show 2 frames before each word.
   - Every sprite is built at start-up, so a bad style fails fast. An outline-mask size bug once killed a render at 26 s, silently.
6. **`mix.py`:** places sound effects by their peak (whoosh into each b-roll cut, pop on each price, ding on the total), then `loudnorm I=-15:TP=-2` and `alimiter 0.79`. Result: −15.6 LUFS, true peak −1.8 dB.

## Rules learned
- **A big price behind the head must stay readable.** Put the last line's bottom at the hair top + 30% of its own height; the first try hid "$6" completely.
- Hold a caption long enough to read (SHANGHAI was on screen for 0.3 s and the Chengdu strike for 0.2 s).
- B-roll (TikHub Douyin search, `fetch_one_video`, h264 `bit_rate` entry):
  - Use curl, because Python urllib gets a Cloudflare 1010.
  - Check each window at 0.5 s steps for burned-in text, then crop with `zoom` / anchor.
- **Facts to flag to the creator:**
  - "600 miles" (London–Shanghai is about 5,700).
  - Most "Shanghai panda" clips are the Wild Animal Park; the $6 ticket is Shanghai Zoo.
