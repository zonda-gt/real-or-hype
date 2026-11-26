# Hotel savings v3: couples (source 20261126_164554.mp4)

Final: `hotel_3_couples_howwedo.mp4` (How We Do bed) and `hotel_3_couples_for_app_audio.mp4` (no music), 31.7 s, -14 LUFS.

## Takes (source seconds)
| Seg | In-out | Line |
| --- | --- | --- |
| A | 10.66-13.00 | Planning a China trip with your partner? (2nd take; 1st take at 1.87 also clean) |
| B | 40.19-45.08 | We can help you get better hotel prices by directly working with local hotels. (31.48 take says "directing") |
| C | 61.24-64.45 | Imagine a trip designed around what you both love. (3rd take; Whisper hears "ship", verbatim + full mix hear "trip") |
| D | 68.92-70.79 | Discovering hidden places, |
| E | 83.91-87.00 | getting reservations at incredible local restaurants, (4th take) |
| F+G | 93.32-96.87 + 97.27-98.66 | and enjoy unique experiences without spending hours / researching them. |
| H | 103.48-107.68 | You will have us as a local concierge to help you throughout your trip. |
| I | 113.88-117.54 | Your hotel savings can cover our concierge fee alone. |
| J | 119.46-122.92 | Comment hotel to find out more. (+1.2 s room tone hold, stops before "OK" at 123.8) |

## Hiccups removed
- F: "spending hours research- researching them": cut 96.87 -> 97.27 (both cut points at near-floor dips; spliced audio re-transcribed clean).
- I: "And- and your hotel savings": started at 113.88 on "Your" (113.46 left a soft "and" + 0.36 s air; keeping the first "And" still read "and, and").
- H: a 0.1 s lip smack at 102.88 and 0.6 s of air before the line dropped (start 103.48).
- Whisper invents a leading "And" on segment I (envelope: silence then "Your" at +0.08 s): dropped from words.json by hand.
- Full-track Whisper skipped "help you throughout ... fee alone": words.json comes from `segwords.py` (per-segment transcription).

## B-roll (Douyin aweme ids)
couple 7642580991148451007 @0.95 s (Fenghuang couple by the river, center crop) · waterfall 7616465800123416566 @2.0 s (crop x 210-720 of the 720x1280 source, clear of the creator watermark "雨果小妖") · dinner 7657142967366832994 @7.4 s · hanfu 7642580991148451007 @4.2 s · reused from v1: jhotel, ritz, bund.
Rejected: 7709498897294845290 (DJI OSMO overlay bottom-centre, couple too wide for 9:16), 7236371025624173828 (burned-in titles), 7660335482949111046 (no download URL).

## Mix
`mix_music_ep3.py` = shared mix_music.py + an extra -8 dB music dip (0.3 s ramps) under segment H: with the plain mix Whisper heard "as a local concierge to" as "at the local conchchd" (the line is fast; no vocals in the bed, voice level same as other lines). With the dip every word is heard; only "Comment" -> "Common" (known mishear).
