# Baixiangju (白象居, Chongqing): straight recreation (Nov 2026)

This episode is a straight recreation of 于锡明's Douyin vlog 7633751862790313829 ("重庆这小区建的也太梦幻了", 4 min), cut to 61 s.
It is not in the Real or Hype? format: there's no sting and no verdict, and his own on-camera lines tell the story (10F → 15F → 14F → 12F → "ground floor again").

- Footage: Alipan 资源库 `/chongqing、/重庆系列/白象居（惊讶）` (19 files, 3.4 GB). Douyin drone B-roll: 7416732680286489856 (F11, needs `play_addr_h264`; the default stream is ByteVC2, which ffmpeg can't decode).
- Work dir layout: `src/` (the Alipan folder), `broll/<aweme_id>_hq.mp4`, `ov/`, and `words.json` (faster-whisper medium word stamps).
- `python3 bxj_check.py` runs the noise-relative energy check on every in/out point of his voice (must print ALL OK).
- `python3 bxj_render.py` writes `out/bxj_1080.mp4` (HLG tone-map, his lines at 1.3× with loudnorm -16, elevator floor badge 2 frames before each floor word, hook title, end card, word subtitles).
- `python3 bxj_sfx.py sfx/ding_el.wav sfx/whoosh_tonal.wav 0.30 0.35` writes `out/bxj_final_1080.mp4`.
  The ding is ElevenLabs "Hotel lift arrival chime" (earshot: strong as a bell ding, top match for a lift chime). Its **peak sits 0.30 s before the floor word at 0.35 volume**: on the word itself it masked "14th floor" (Whisper heard "424").
- `python3 bxj_mix.py music/quirky_pizzicato_el.mp3 -5` is the final mix and replaces `bxj_sfx.py`. It includes the effects, plus:
  - Background music: an ElevenLabs Music track (prompt: quirky sneaky mystery, 110 BPM, pizzicato, bassoon/clarinet, snaps). Earshot heard it as "playful and quirky music" (strong); the other two candidates read as "corporate pop" and "lo-fi".
    It is loudnormed to -16, then -5 dB, sidechain-ducked under his voice (more than 10 dB below speech, about -22 LUFS in the gaps), and faded over the end card.
  - On "Wait, what?" a record scratch (ElevenLabs, earshot "record scratch" strong; edges faded to stop clicks) cuts the music until after the second "what?".
  - The master adds +1.5 dB, then alimiter 0.84, giving -16.0 LUFS and a true peak of -1.1 dBTP. Every line was Whisper-checked over the music.
  - Earshot flags 0.4–0.7 s drops at 15.7, 17.0, 36.7 and 46.5 s. These are the track's own staccato rests, not dead air.
- `vruns.py <file> <a> <b>` prints voiced runs, to pick cut points that land in silence.
