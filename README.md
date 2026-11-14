# Real or Hype?

Claude Code skill for making "Real or Hype?" short videos: react to a viral clip of a place, go there, test the claim, give a verdict (Instagram Reels / TikTok, under 40 s).

The skill lives in `.claude/skills/real-or-hype-video/`. It contains the workflow, a pre-delivery checklist, scripts, the sung sting, sound effects and fonts.

## Starting a new video

1. Start a new Claude Code session with this repo (`zonda-gt/real-or-hype`) selected.
2. Type `/real-or-hype-video`, or paste:

```
Make a Real or Hype video using the real-or-hype-video skill.
Place: <name, city>
Viral reaction clip: <Instagram/TikTok link>
My reaction video + raw footage: <Google Drive folder link, "anyone with the link">
Claim to test: <e.g. "thousands of trees on a mall">
Keep it under 40 s.
```

## Keys (set in the cloud environment's settings, never in this repo)

- `OPENAI_API_KEY`: narration voice (OpenAI `gpt-4o-mini-tts`, voice `cedar`)
- `BRIGHTDATA_API_TOKEN`: finding viral clips and scraping reels

Footage is best shared as a Google Drive folder set to "anyone with the link".

## Aliyun Drive (阿里云盘) footage

`.claude/skills/aliyunpan-login/` logs in to Aliyun Drive with a QR code and downloads original files of any size. The environment's network must allow `alipan.com`, `aliyundrive.com`, `aliyundrive.net` and `api.tickstep.com`.

## mall-reel skill

`.claude/skills/mall-reel/` makes 60-75 s intro reels of many-spot places (malls, districts, streets) from Douyin b-roll and an AI narration, in the style of @wynnejael: research with Douyin search + Doubao, per-spot footage search, script rules, ElevenLabs v3 voice, renderer with the exact text styles, and QA. Example episode: GATE M West Bund Dream Center (`work/gatem2/`). Keys: `TIKHUB_API_KEY`, `ARK_API_KEY` (Doubao), `ELEVENLABS_API_KEY`.
