---
name: chinapal-promo
description: Plan, storyboard, generate (AI demo) and edit ChinaPal product promo Reels — "DM us your saved reels, we build your itinerary" — using a menu of motion-graphics effects (couch wall, orbit, vertigo, UI world, checklist, pull-back reveal, route grow, zoom-through, cover story, frame break). Use for ChinaPal promo scripts, storyboards, Seedance demo shots, Remotion edits and re-cuts.
---

# ChinaPal promo videos

Product: **ChinaPal**. Instagram: **@steven_chinapal** (Steven, the founder, is the on-camera presenter).
Pitch: send your saved Instagram reels of places to @steven_chinapal in a DM → ChinaPal builds a personalised day-by-day itinerary around those reels.
CTA in use: "Comment TRIP and I'll send you the link" (needs a comment auto-DM; otherwise "DM us your saved reels").

## Status (Nov 2026)
- v1 (Python/PIL renderer, `scripts/render.py`) and v2 (Remotion, `remotion/`) of a ~37 s AI demo exist. Same cut, same audio.
- Creator feedback on v1: **too slow**. Next versions: **faster pace and a new script that sells the service harder**. Also wanted: a 15–17 s cut.
- App screens are HTML mock-ups (`scripts/screens.py`), placeholders until Steven sends the real DM thread, itinerary and reel links.

## Script 2 / Script 3 cuts (~18–19 s, Nov 2026)
- Script 2 "result first": PhoneHold (overview screen) → Checklist → Orbit → RouteGrow + tip bubble → StopScreen zoom → CoverStory "YOUR REELS/TRIP" → FrameBreak "Comment TRIP".
- Script 3 "offer": FrameBreak hook "Send me your saved reels. I'll plan your whole China trip." → CouchWall → UIWorld (DM) → PullBackReveal (facecam tile + Day-1 itinerary phone) → StopScreen with chip/map/tip highlights on "hours, routes, tips" → CommentCTA (IG comment sheet, TRIP typed, "Sent you a DM").
- Build: `scripts/sd_batch2.py shots.json outdir` (Seedance, prompt asks for "upbeat and quick") → Whisper `wtx.py` → `scripts/prep2.py plan.json rm/public rm/edl.json` (trim, speed 1.15×, cut-out, voice loudnorm, word frames, merges "-by -day", fixes Whisper "roots"→"routes") → `remotion/src/Fx.tsx` (reusable effect components incl. word-synced captions, per-segment voice and SFX) + `Scripts.tsx` (step lists) → `node render2.mjs Script2|Script3 [stills f…]`.
- CTA advice given: one spoken CTA "Comment TRIP" only with an instant auto-DM (ManyChat) asking them to share reels into that chat; caption backup "share your saved reels to @steven_chinapal"; without automation say "Share your saved reels to my DMs". A/B by completed trips, not comments.

## Presenter = Steven's real face (Nov 2026)
- Verified Ark portrait asset: **`asset-20261108173149-2kjzb`** (group `group-20261108172400-zgsn2`, created in Ark Experience Center → 我的 → 真人人像). Use as `{"type":"image_url","image_url":{"url":"asset://asset-…"},"role":"reference_image"}`; the group id is NOT accepted, direct photo uploads are always rejected. `scripts/sd_batch3.py shots.json outdir asset_id`.
- Prompt "starts speaking at the very first frame and says only this exact line" — short lines still make it pad with filler/stutters; give lines of 6+ words, trim on Whisper word times, regenerate with another seed if garbled (~1 in 4 shots needed it).
- Creator wants it FAST: speech at **1.3×** (prep2 speed), cuts on word boundaries; v1 ≈ 24 s, Script 2 ≈ 16 s, Script 3 ≈ 15 s. CTA keyword is now **REEL** ("Comment REEL"); Whisper hears it as "real", prep2/edl fix maps it to REEL.
- Instagram posting: use the **instagram-trial-reel** skill (trial reels only, uploads local files directly). Old manifest script `scripts/post_trial_reels.py` is superseded.
- Instagram posting (history): the user's "AI Chat generation env" holds INSTAGRAM_ACCESS_TOKEN / INSTAGRAM_USER_ID / INSTAGRAM_FB_TOKEN (not this "Video editing" env). Post only after explicit confirmation of video, caption and trial/normal reel.

## Real-footage edits: choosing takes (lessons, Nov 9)
- Never pick takes from the transcript alone. For every line, build a sheet of ALL its takes (`scripts/take_sheets.py`: one row per take, a frame every 0.4 s labelled with the word being said) and choose on picture AND sound: eye contact, a gesture that fits the effect, not reading the phone, not looking down, not leaning out of frame.
- Check Whisper's segmentation: a "take" can contain an aborted start ("But you've been … and you've been to none of them"); re-transcribe the chosen range alone before trusting it.
- Pointing shots: grab grid frames (1080×1920 coords) at each place word, read the fingertip position, and put that word's pin there (`RouteGrow pts/pins/at`); the route must follow the order he points (Real 1 goes right→left). Mirror the shot or flip the graphic if needed; never let a graphic contradict the hand.
- Floating UI must not cover his face: measure the head box and place the phone (`UIWorld px/py/pw`, `PhoneHold x/y/w`) beside it; flying cards arc above the head.
- If a take opens with him settling into frame and the first word starts too soon to trim, hide those frames with a short zoom-blur-in (`Orbit blurIn`).
- Final check: 3 fps sheets of each render plus close 5–8 fps strips of every effect moment, before sending.

## Effects menu (from @tenfoldmarc's "17 video effects Claude can create" reel)
Used: 01 couch wall (reels pinned on the wall *behind* him), 02 orbit (reels circle him in 3D), 03 vertigo (dolly zoom on a clean plate), 04 UI world (floating DM, reels fly in), 05 checklist (glass panel ticks), 06 pull-back reveal (shot shrinks into "building your trip" window, % counter), 07 route grow (Day-1 route draws on the wall behind him, pins pop on spoken words), 08 zoom-through cut (into the café reel → café shot), 09 cover story (Playfair title behind his head), 10 frame break (he reaches out of an IG reel frame).
Not used: headline wall (dup of couch wall), green screen, paper cut, doodle boil, glass type (pick one of cover story / glass type), phone mockup (UI world covers it), digital zoom (use sparingly).
Rule: one effect per story beat, never two big effects at once, one text style at a time.

## Pipeline
0. **Polished app screens (itinerary etc.)**: OpenAI **`gpt-image-2.6-sunburst`**, size **`1152x2496`** (true iPhone shape), quality high, via `scripts/gen2.py`. It beat `gpt-image-2.6-flare` (garbled a label) and `gpt-image-2` at 1024x1536 (creator: "not like mobile, not polished"). Give it a full design system in the prompt (colours, SF Pro hierarchy, 8 pt grid, 20 pt cards, exact copy for every element). Frame in an iPhone with `scripts/phone_frame.py`. The "Steven's tip" avatar is AI: swap in his real photo.
1. **Stills / storyboard**: `scripts/gen.py` (OpenAI `gpt-image-2` generations), `scripts/edit.py` (likeness edits from a photo), `scripts/screens.py` + `scripts/shot.js` (HTML → PNG via Playwright), `scripts/frames.py`, `scripts/sheets.py`.
2. **AI shots: Seedance 2.0 Mini on Volcano Engine Ark** (`ark.cn-beijing.volces.com`, key is a proxy-injected environment credential: send `Authorization: Bearer proxy-injected`). Model `doubao-seedance-2-0-mini-260615` (must be activated in the Ark console). `scripts/sd_batch.py`.
   - **Any realistic face in an input image is rejected** (`InputImageSensitiveContentDetected.PrivacyInformation`): Steven's photo, a gpt-image presenter, even a frame of Seedance's own output. Only text-to-video works unless he completes Volcano's real-person verification (asset id).
   - Consistency: one fixed presenter + room description and `seed: 77911` for every shot. Worked well enough.
   - Measured cost: 480p ≈ 10,100 tokens/s ≈ **0.23 yuan/s** (0.023 yuan / 1k tokens); 720p ≈ 0.5 yuan/s. 4–6 s per shot.
   - It speaks the quoted line (generate_audio). Watch for extras (it said "one two three" aloud when told to count) and for props it invents (paper notes on the wall: say "the wall is completely bare").
3. **Cut-outs**: `scripts/mattes.py` → trimmed `base_XX.mp4` + presenter-only `cut_XX.webm` (VP9 alpha, rembg `u2net_human_seg`, EMA-smoothed) + `plate_03.jpg` (OpenCV inpaint clean plate for vertigo).
4. **Edit (preferred): Remotion** (`remotion/`, remotion@4.0.536, react@18.3.1). Graphics in `src/Demo.tsx`, one component per effect, `SEG` holds segment frame counts. Render with `node render.mjs` (uses `/opt/pw-browsers/chromium`; `node render.mjs stills <frames…>` for checks). Layers: `<OffthreadVideo>` base → graphics behind → `<OffthreadVideo transparent>` cut-out → graphics in front → captions. 1080×1920 @ 24 fps.
   Python/PIL renderer (`scripts/render.py`, `scripts/assets.py`) is the v1 fallback: fine for pixel work, worse for typography and motion.
5. **Audio**: each shot's voice `highpass=f=80,loudnorm=I=-16`, whoosh at every cut, pop/ding/click on graphic hits (sfx from `real-or-hype-video/sfx`), limiter; target ≈ -15/-16 LUFS, peak ≤ -1 dB.
6. Captions: small white line + big yellow keyword (Montserrat ExtraBold, black stroke), keyword timed to the Whisper word onset minus 2 frames.

## Filming brief (for the real version)
4K 30 fps vertical, HDR off, tripod locked, waist-up with space above the head, plain wall 1–2 m behind, face the window, 3 takes per line, 5 s of the empty room. Screen-record: Saved folder scroll, sharing 8–10 reels to @steven_chinapal, the reply, the itinerary, the profile.
