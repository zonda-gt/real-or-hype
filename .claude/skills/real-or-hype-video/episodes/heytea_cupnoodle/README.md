# Heytea × Cup Noodle "Fresh Coconut Ramen" (生打椰拉面), Instagram reel, Nov 2026

Not a Real or Hype episode: a straight product-review reel modelled on @jennaisblonde's Heytea × Cup Noodle reel
(hook with the cup + big title → storefront/menu → ordering → unboxing → tasting → verdict → follow CTA, ~31 s).

- Footage: 18 clips, OneDrive folder from the creator (20261115_HHMMSS.mp4, HLG → tone-mapped to BT.709).
- Narration (v2, creator's pick): ElevenLabs library voice **John, "Passionate Founder"** (`PXo7njgt8slUVdtKa3La`),
  `eleven_multilingual_v2`, stability 0.35 / similarity 0.8 / style 0.45 / speaker boost; trimmed, inner pauses squeezed
  to 0.18 s, `atempo=1.12`. John says "Nissin" like "Nissan" and "yuan" like "UN": use "official collab" and
  "22 yuan, about $3" (passes). v1 used Dev (`5J8HNhWkTAhN2YWsd9Ta`, atempo 1.1). Also auditioned: John `PXo7njgt8slUVdtKa3La`, Jeongki `fwH9jZjJVWYg6qwyWr01`,
  Minho `LoXeQQJXcdhPF6vk2Phy`, The student `Ih5c9jfzl0g5jmK1Z2Nq`, Minzy (female) `y3J9lm4KG5NLFtSFEB5A`.
  Shared-library voices work directly by id with this key. Write "Hey Tea" in TTS text (subtitles say "Heytea").
- Facts used: launched 13 Nov 2026, coconut base + mango "noodles" + corn, ¥22, some shops sold out in minutes (21jingji, Sohu).

Opening (v2, creator asked for "aesthetic shots, take the viewer on a journey" + an aesthetic text hook):
hero push-in on the cup on the steel counter (hook text) → neon sign at night → walking in the door → lamp-lit
"new style tea" wall (zoom 1.25 to hide an LED ticker) → tilt up to the animated noodle-cup screen → his line.
Hook text (`hook.py`): small tracked caps "HEYTEA × CUP NOODLES" (Inter Display Medium) over a large Instrument Serif
"a cup noodle" / italic warm-cream "you drink?", soft shadow, no outline, soft top gradient; lines rise in one by one
(0.15 / 0.55 / 0.95 s) and fade out at the end of the hero shot. Narration subtitles start only after the hook.
The v1 meme-style title (`title.py`, yellow Montserrat with outline) was judged not aesthetic enough.

Pipeline (workdir has raw/, vo/L*.wav):
1. `python3 hook.py <wd>/hook 150`
2. `python3 render.py <wd>`  shots from `segs.py`, gap check against his measured speech spans
3. `python3 finish.py <wd>`  subtitles, title card, narration, whoosh/pop, loudnorm -15 LUFS, limiter

## v3 (creator notes: open on him + cup, "make the colour normal", re-pick aesthetic shots, write narration TO the clips)
- **Colour**: the zscale+`tonemap=hable` chain tone-maps R, G, B separately, which pushed bright areas yellow/orange
  ("looks a bit off"). Now: ITU-R BT.2446-1 Method A (luma-based, hue-preserving) baked into a 65³ LUT
  (`hlg2sdr_lut.py out.cube 65 1.5` → `hlg2sdr_bt2446a_exp1.5.cube`, exposure 1.5), applied with
  `scale=in_color_matrix=bt2020…,lut3d,scale=out_color_matrix=bt709`. White cups, natural skin. libplacebo bt.2390 was
  tried via lavapipe (software Vulkan) but renders stripe artefacts in this container.
- **Picture first**: all 18 clips re-reviewed at 0.5 s in the new colour; shots picked for looks and ordered as a journey
  (`segs.py`), then one short narration line written per shot it describes (`vo_lines_v3.json`, N1–N13) and anchored
  to that shot's start. `fitcheck.py <vo_dir>` checks fit without rendering; shot lengths were nudged to lines, not the
  other way round. Detail found on review: staff wear "CUP HEYTEA" chef hats (N4 "Even the chef hats!").
- Hook shot: 173008 9.2–10.96 s at 0.8× (his steadiest pose; the creator picked it).
- Subtitles: events are made non-overlapping (two Whisper word times out of order had stacked a line twice).

## v4: two variants, script first (creator: v3 narration "too dry"; write narration as good as the reference, THEN match clips)
Lesson: "write the narration to the clips" meant a lively, story-driven script like the reference (setup, disbelief,
reveal, question, reaction, verdict, CTA), with each line then matched to the shot that fits it best. Not
caption-style descriptions of each shot. Lines are short and punchy and carry opinion and personality.
- `segs_A.py` + `vo_lines_A.json`: "I had to try this" story (hook "a cup noodle / you drink?" on him + cup).
- `segs_B.py` + `vo_lines_B.json`: "3 things to know before you order": opens on the overhead noodles ("these noodles /
  are a drink."), numbered tip labels (`tips.py`: Instrument Serif italic "No. 1" + tracked caps) via `OVL`, ends "Save this
  for your China trip!" (save-driven).
- Run: `render.py <wd> A` / `finish.py <wd> A` (segs_A, vo_A/, hook_A/, out_A/); `fitcheck.py <vo_dir> A`.
- John (stability 0.3, style 0.55, atempo 1.1). Mishearings fixed by rewording: "Soup, or drink?" → "Is it soup... or a drink?",
  "22 yuan" → "about $3" (B), "Pour" retaken.
