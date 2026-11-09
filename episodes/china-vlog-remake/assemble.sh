#!/bin/bash
# Concatenate graded shots + title shot and lay the reference's original sound underneath.
set -e
cd "$(dirname "$0")"
{ echo "file 'segs/seg00_title.mp4'"; for k in $(seq -w 1 14); do echo "file 'segs/seg$k.mp4'"; done; } > concat.txt
ffmpeg -v error -y -f concat -safe 0 -i concat.txt -c copy video_only.mp4
ffmpeg -v error -y -i ../ref/ref1080.mp4 -vn -c:a aac -b:a 256k sound.m4a
ffmpeg -v error -y -i video_only.mp4 -i sound.m4a -map 0:v -map 1:a -c:v copy -c:a copy -shortest -movflags +faststart china_vlog_1080p.mp4
ffmpeg -v error -y -i china_vlog_1080p.mp4 -vf scale=960:540 -c:v libx264 -crf 23 -preset medium -c:a aac -b:a 160k -movflags +faststart china_vlog_preview_540p.mp4
ffprobe -v error -show_entries stream=codec_type,width,height,nb_frames:format=duration -of compact china_vlog_1080p.mp4
