# Character-over-places beat edit

Takes a short clip with one character (e.g. an anime edit), cuts the character out, and puts it over Douyin travel clips cut to the song's beat. Adds bilingual lyric subtitles and place labels.

Run every script from a work dir that contains `reel.mp4` (the source clip), `song.wav`, `dy/` (Douyin clips) and `fonts/` (Noto Sans SC Black as `Noto_San.ttf`, ZCOOL KuaiLe as `ZCOOL_Ku.ttf`, both from Google Fonts). Use a venv with `opencv-python-headless numpy scipy librosa pillow requests`.

1. **Source**: TikHub `GET /api/v1/instagram/v1/fetch_post_by_url?post_url=...` returns `video_url`.
2. **Places**: `dysearch.py "<keyword>" search/<kw>.json` (TikHub video search v2, most-liked, last 6 months, under 1 min). `dydl.py <id,id,...> dy` downloads without the watermark. It prefers `play_addr_h264`, because the ByteVC2 (`bvc2`) streams don't decode in ffmpeg.
   Run `ffmpeg scdet` on each clip and keep every shot window between the source's own cuts. Otherwise you get off-beat cuts.
3. **Beat**: `earshot timeline song.wav --json` plus `beats2.py` (kick/snare band periodicity) and `grid.py` (constant-grid fit). librosa alone locks onto triplet hi-hats (136 vs 90 BPM). Check the phase against the lyric-change times from `lyr.py`.
4. **Cut-out**: `rembg isnet-anime` was unstable frame to frame (a third of frames came out partial). The background was a still image, so we used background subtraction instead:
   - `plate.py`: per-pixel colour mode over all frames
   - `matte.py`: inpaint the always-covered core, then a Lab distance matte
   - `matte3.py`: refill the core from frames where it is visible (behind a 14 px dilated pass-1 matte), drop the floor shadow (ratio test) and the static watermark
   Don't feed a matte's own output back into the plate with a small margin: it erases the hair.
5. **Render**: `render.py out.mp4 [preview_seconds]`. One place per bar, a cut every 2 beats, a 7% zoom punch on each cut, a character bounce on each kick, the place-label pill and the lyric subtitles.
