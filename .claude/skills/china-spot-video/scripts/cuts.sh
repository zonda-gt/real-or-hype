#!/bin/bash
# Print a source's own shot boundaries (scene changes), so in/out points never cross a cut. usage: cuts.sh <video> [threshold 0.25]
ffmpeg -hide_banner -i "$1" -vf "scale=320:-2,select='gt(scene,${2:-0.25})',showinfo" -an -f null - 2>&1 | grep -o 'pts_time:[0-9.]*' | cut -d: -f2 | awk '{printf "%.2f ", $1} END {print ""}'
