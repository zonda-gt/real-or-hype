---
name: talking-head-video
description: Edit the creator's own talking-head recordings (ChinaPal concierge pitches, e.g. the "hotel savings" series) into short vertical reels in the style of the reference reel @iamaayushswamy DfVTpW_OE_j - best take of each line, jump cuts with punch-ins, zoom-blur whips, mid-frame captions with red serif accents, stacked italic titles, cream/navy word cards, B-roll on the nouns, and an Instagram comment pill CTA. Built with HyperFrames. Not for "Real or Hype?" (real-or-hype-video) or narrated B-roll reels (china-spot-video).
---

# Talking-head reels (HyperFrames)

## Source footage
- Phone takes, 1080x1920 portrait (stored 1920x1080 + rotation), 60 fps, one long take per script with many retakes and long pauses.
- OneDrive "1drv.ms/f/c/..." folder links: the old `api.onedrive.com/v1.0/shares` call returns 401. Get an anonymous token: `POST https://api-badgerp.svc.ms/v1.0/token {"appId":"5cbed6ac-a083-4e14-b191-b4ba07653de2"}`, then `GET https://my.microsoftpersonalcontent.com/_api/v2.0/shares/u!<base64url(link)>/driveitem?$expand=children` with `Authorization: Badger <token>` and `Prefer: autoredeem`; each child has `@content.downloadUrl`.

## 1. Find every take
- Whisper over the whole file **skips repeated takes** (20 s of retakes vanished). `scripts/islands.py <wav> medium` splits on relative-energy speech islands and transcribes each island alone, so every take is listed with times.
- Pick the best complete take of each line; write `cuts.json` `[[key, in, out, text], ...]` (rough island times).

## 2. Cut the A-roll (audio first)
- `scripts/refine.py <wav> segs.json cuts.json` snaps in/out to silence with a sensitive threshold and reports the clear space either side. Then look at the 20 ms envelope (`scripts/env.py <wav> a:b`) at any cut with < 0.1 s clear: breaths before a line stay out, word tails decay to the noise floor before the out point.
- `scripts/cut_aroll.py <src.mp4> cuts.json <dir>`: one accurate-seek encode per segment (several `trim`s of one 1080p60 input in one filter graph got OOM-killed), 12 ms audio fades, each segment's audio padded/trimmed to its video length (no drift), `voice.wav` processed with highpass, afftdn, compressor, loudnorm. **afftdn delays audio 25 ms**: the script trims it back (checked by cross-correlation: 0 ms).
- `scripts/verify.py voice.wav timeline.json words.json voice_raw.wav`: Whisper the cut voice (every scripted word present, in order) and check each join lands in silence on the **unprocessed** audio (thresholds on the compressed track are meaningless).

## 3. Build in HyperFrames
- `hyperframes init <dir> --non-interactive --resolution portrait --skip-transcribe` (telemetry: `hyperframes telemetry disable`). Copy segments (re-encoded `-g 30`), B-roll (cut to 1080x1920 cover, `-g 30`), fonts, voice, music, sfx into `assets/`.
- Episode `make_plan.py` turns words.json + timeline.json into `plan.json` (caption groups by word index, accent words, B-roll windows, cards, sfx); `scripts/build_hf.py <project> plan.json` writes `index.html` + `compositions/{aroll,broll,cards,captions}.html`.
- Then `hyperframes check --json --safe-zone reels`, `hyperframes snapshot --at ...`, look, fix, `hyperframes render -o out.mp4 --fps 30` (~2.5 min for 25 s on CPU).

## Style (measured from the reference)
- Captions: 1-3 words, Inter Display Bold 76 px, -0.05em tracking, warm off-white `#f5efe6`, soft shadow, centred, top 1060 px (on the chest; at 930 they sat on his chin/mouth after punch-ins). Words appear on their onsets; the group blurs in 0.1 s.
- Accent words: Instrument Serif Italic 104 px, red `#c8161d` over the black T-shirt; **white serif over B-roll** (red vanished on the skyline and hotel room).
- Titles: Inter Display Black Italic uppercase lines + a red Playfair Bold Italic line, built word by word with a 0.13 s blur-in; keep lines <= ~1000 px wide and the block above y 1248 (Reels safe area).
- Full-screen word cards: cream `#efe6d8` with red text, navy `#101a20` with off-white text, ~0.8 s.
- Cuts: alternate punch-in 1.0 / 1.1-1.15 (origin 50% 30%); zoom-blur whip (scale x1.16-1.2, blur 14-16 px -> 0 in 0.22 s expo.out) into B-roll and back to the face.
- CTA: white pill with the keyword in quotes and a red send button, back.out pop on the keyword, held ~1 s after the last word (extend the last take into room tone; never freeze a frame).
- Mix: voice -15 LUFS, music bed (china-spot-video `sfx/music_marimba_el.mp3`) at volume 0.25 (~11 dB under), whoosh into B-roll, pop on cards; final two-pass loudnorm to -14 LUFS, TP -1.5, video stream copied.

## Before delivery
- Rendered file: no black frames, freezes only on the cards (`freezedetect`), audio offset vs voice.wav 0 ms, -14 LUFS, Whisper of the final mix hears every word, a frame either side of every cut.

## Episodes
- `episodes/hotel-savings/` (Nov 2026, 6 scripts): v1 general (done), family, couples, solo, "without a tour group, $89", "before you spend thousands". Keyword: HOTEL.
