# Pipeline scripts for this reel

These were run from `video-jobs/hotel-cheap-vs-expensive/` as the working directory (`JOB=$PWD`). Keys are read only from the environment variables `TIKHUB_API_KEY`, `ELEVENLABS_API_KEY` and `OPENAI_API_KEY`; none are stored here.

| Step | Script |
|---|---|
| TikHub client (sends User-Agent `chinapal-video/1.0`, logs every call to `search/calls.log`) | `th.py` |
| Douyin search v2/v3, harvests candidates into `search/candidates.json` | `harvest.py v2 "<kw>" ...` (`PAGES=1` to limit pages) |
| Fresh detail per video (`app/v3/fetch_one_video`) | `one.py <aweme_id> ...` |
| Download the best decodable no-watermark stream (H.264 from `aweme/v1/play/?video_id=<play_addr.uri>&ratio=1080p`, or ByteVC1/HEVC `bit_rate` entries; ByteVC2 can't be decoded by ffmpeg) | `dl3.py` |
| Whisper transcription / translation | `whisper.py`, `translate.py <aweme_id>` |
| Contact sheets, scene cuts, OCR text bands, crop preview | `sheet.sh`, `scenes.sh`, `ocrband.py`, `tx.py` |
| ElevenLabs TTS with timestamps + gap tightening and tempo 1.12 | `el.py <name> "<text>"`, `tighten.py <name> 0.32` |
| Procedural (licence-free) music bed | `musicbed.py out.wav 32` |
| Edit / render | `render.py A`, `render.py B`, `render.py A music` |
| Watermark + quality QA | `OMP_THREAD_LIMIT=1 qa.py`, then `corners.py` |

Note: the scripts contain absolute paths from the cloud session (`/home/user/real-or-hype/...`, the sfx folder in `.claude/skills/real-or-hype-video/sfx`). Adjust them before reusing.
