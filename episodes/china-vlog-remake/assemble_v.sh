#!/bin/bash
# Concatenate graded shots + title shot and lay the reference's original sound underneath.
set -e
cd "$(dirname "$0")"
{ echo "file '${SEGDIR:-segs_v}/seg00_title.mp4'"; for k in $(seq -w 1 14); do echo "file '${SEGDIR:-segs_v}/seg$k.mp4'"; done; } > concat_${SEGDIR:-segs_v}.txt
ffmpeg -v error -y -f concat -safe 0 -i concat_${SEGDIR:-segs_v}.txt -c copy video_only_${SEGDIR:-segs_v}.mp4
ffmpeg -v error -y -i ../ref/ref1080.mp4 -vn -c:a aac -b:a 256k sound.m4a
ffmpeg -v error -y -i video_only_${SEGDIR:-segs_v}.mp4 -i sound.m4a -map 0:v -map 1:a -c:v copy -c:a copy -shortest -movflags +faststart ${OUTNAME:-china_vlog_9x16_1080x1920}.mp4
ffmpeg -v error -y -i ${OUTNAME:-china_vlog_9x16_1080x1920}.mp4 -vf scale=540:960 -c:v libx264 -crf 23 -preset medium -c:a aac -b:a 160k -movflags +faststart ${OUTNAME:-china_vlog_9x16_1080x1920}_preview.mp4
ffprobe -v error -show_entries stream=codec_type,width,height,nb_frames:format=duration -of compact ${OUTNAME:-china_vlog_9x16_1080x1920}.mp4
