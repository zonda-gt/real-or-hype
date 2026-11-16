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
