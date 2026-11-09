# Split-screen lyric reel with Chinese cities on top

This format comes from @eks.learnchinese, "Illusionary Daytime (幻昼) – TrackMaker", 17.3 s.
- **Top half:** the creator, with the caption "speak 🇨🇳: 1%".
- **Bottom half:** a lyrics-app recording (pinyin, red current word, English) with "sing 🇨🇳: 99%".

This edit keeps the bottom half and the audio exactly as they are, and replaces the top with Douyin city clips cut on the drum hits.

Run everything in a work dir containing `reel.mp4`, `song.wav` (its audio) and `dy/` (city clips from `../character-beat-edit/dysearch.py` and `dydl.py`).

1. **Beat**: the song is 102.4 BPM. essentia's confidence is 3.83 and earshot calls it "clear". Fit the grid to the kick and snare onsets (`grid.json`). `pickcuts_s2.py` then picks cuts on the strongest hits with shots of 2–4 beats (`cuts.json`).
   - The bottom card flips follow the vocals, not the drums: only 2 of the 9 flips land on a hit. So don't cut the top on the flips.
2. **Split line**: y = 633 until ~14.4 s, then y = 675, because the original's top panel grows. It's measured per frame from the strongest row edge outside the caption (`split.json`).
   - A first detector mistook the lyric card's edge for the split at 5.6–7.8 s. Always look at crops before trusting it.
3. **Captions**: `capov.py x y w h out.png` lifts a static caption from the original. It takes the per-pixel temporal median, keeps only text-coloured pixels that stay stable over time, and fills the flag from its largest red blob.
   - "speak" is at (190, 505, 340, 80) and is redrawn over the cities.
   - "sing" is at (190, 625, 340, 80) and is redrawn once the split moves above it.
4. **Render**: `s2_render.py out.mp4`.
   - City clip cover-cropped into the top panel, with a 7% zoom punch on each cut.
   - City label pill.
   - Both captions.
   - Output 1080×1920, audio copied unchanged.
5. **Verify**: `verify_s2.py out.mp4`. It detects the cuts in the top band of the rendered video and scores them against the drum onsets.
   - v1: all 11 cuts found, median 12 ms from the beat, every cut on a clear hit.
   - The one extra detection is neon flashing inside a clip.
