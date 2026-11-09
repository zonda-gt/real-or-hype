---
name: instagram-trial-reel
description: Post videos to Instagram as TRIAL reels (shown to non-followers first) for @steven_chinapal or another account whose token is set up. Use when the user says "post this as a trial reel", "post it on Instagram", "publish these reels", or similar. Trial reels only; never normal posts, stories or feed posts. Works with local video files (desktop app or cloud) and public video URLs.
---

# Post Instagram trial reels

This skill only posts **trial reels**: they go to non-followers first, and the user graduates the winner to their followers later in the Instagram app (or Instagram does it automatically with `SS_PERFORMANCE`). Never post a normal reel, feed post or story with it.

Script: `scripts/post_trial_reel.py` in this skill's folder (Python 3 + `requests`; `ffprobe` optional for the video checks).

## Steps

1. **Collect**: the video file(s) or public URL(s), the caption, the account (default `steven_chinapal`), and graduation (`MANUAL` by default: the user graduates in the app; `SS_PERFORMANCE`: Instagram graduates it if it does well).
   - No caption given: draft one (hook line, what to do, CTA keyword if any, 3–5 hashtags) and treat it as a proposal, not a decision.
   - Several videos for one A/B test: use the **same caption on all of them** unless told otherwise.
   - Save the caption to a text file and pass `--caption-file`, so emoji and line breaks survive.
2. **Dry run** (checks token, account, file format, caption; publishes nothing):
   ```bash
   python3 <skill>/scripts/post_trial_reel.py VIDEO1.mp4 VIDEO2.mp4 --account steven_chinapal --caption-file caption.txt --dry-run
   ```
   Fix any `PROBLEM` (re-encode with `ffmpeg -i in.mp4 -c:v libx264 -crf 18 -pix_fmt yuv420p -c:a aac -ar 48000 -movflags +faststart out.mp4`). Warnings (e.g. not 9:16) are shown to the user.
3. **Confirm with the user before publishing**: show the account, the file names, the exact caption and "trial reel, graduation MANUAL/SS_PERFORMANCE", and ask "Post these?". Publishing is public and can't be undone from here. If the user's request already named the files, the caption and trial settings explicitly ("post X and Y as trial reels with this caption: ..."), that is the confirmation.
4. **Publish**: the same command with `--yes` instead of `--dry-run`. It waits for processing, publishes, and prints each permalink.
   - **@steven_chinapal's token does NOT accept direct file uploads** (Instagram Login API answers "The parameter video_url is required"; the Facebook token lacks `instagram_content_publish`). So for this account pass **public URLs**: commit the final videos to the public `zonda-gt/real-or-hype` repo (e.g. `media/<campaign>/`), push, check `curl -sI` on `https://raw.githubusercontent.com/zonda-gt/real-or-hype/refs/heads/<branch>/<path>` returns 200 with the same size as the local file, then run the script with those URLs. The dry run can't detect this; only the real call can.
   - Other accounts may accept direct upload (resumable); the script tries it for local files and prints this advice if it is refused.
   - It writes `VIDEO.ig.json` next to each local file and skips files already published, so re-running after a partial failure is safe. Never delete those files to "retry" a published video.
   - If one video fails, report Instagram's error; re-run once at most. Don't improvise other ways to post.
5. **Report**: the permalink of each trial reel, plus a reminder that trial reels appear in the Trial reels section of the professional dashboard and are graduated (shared to followers) from there.

## Token setup

The token is never printed or pasted in chat. The script reads, in order:
- `INSTAGRAM_ACCESS_TOKEN` (+ `INSTAGRAM_USER_ID`, optional): Instagram Login token, uses graph.instagram.com
- `INSTAGRAM_FB_TOKEN` + `INSTAGRAM_USER_ID`: Facebook Login token, uses graph.facebook.com (fallback)

Where they come from:
- **Claude Code on the web (cloud)**: the environment's variables (environment "Video editing" or "AI Chat generation env" have them). Variables load when a session starts, so a session that was running before they were added won't see them: start a new chat.
- **Desktop app / local terminal**: put them in `~/.config/instagram-trial-reel/.env`:
  ```
  INSTAGRAM_ACCESS_TOKEN=...
  INSTAGRAM_USER_ID=...
  ```
  (`chmod 600` it), or export them in the shell profile, or pass `--env-file path`.
- The token needs the `instagram_business_content_publish` permission (Instagram Login) or `instagram_content_publish` (Facebook Login), and the account must be a professional account eligible for trial reels.

If no token is found, tell the user where to put it; never ask them to paste it into the chat.

## Using it in other projects

The skill lives in the `zonda-gt/real-or-hype` repo (`.claude/skills/instagram-trial-reel/`), so any session with that repo has it. To have it everywhere on a computer, copy the folder to `~/.claude/skills/instagram-trial-reel/`.

## Notes

- Formats: H.264 (or HEVC) + AAC ≤ 48 kHz, 23–60 fps, 3 s to 15 min, up to 1 GB, 9:16 (1080×1920) recommended. Caption ≤ 2200 characters, ≤ 30 hashtags.
- API calls go to `graph.instagram.com` / `graph.facebook.com` (`/{ig-user-id}/media` with `media_type=REELS`, `upload_type=resumable`, `trial_params={"graduation_strategy": ...}`; upload to `rupload.facebook.com/ig-api-upload/...` with `Authorization: OAuth <token>`; poll `status_code`; `/{ig-user-id}/media_publish`).
- Set `GRAPH_VERSION` to change the Graph API version (default v24.0).
