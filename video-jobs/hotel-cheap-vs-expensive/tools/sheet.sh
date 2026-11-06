#!/bin/bash
# usage: sheet.sh in.mp4 out.jpg [fps] [tilew]
in=$1; out=$2; fps=${3:-1}; w=${4:-240}
d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$in")
n=$(python3 -c "import math;print(max(1,math.ceil($d*$fps)))")
cols=8; rows=$(( (n+cols-1)/cols ))
ffmpeg -v error -y -i "$in" -vf "fps=$fps,scale=$w:-2,drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='%{pts\:hms}':x=4:y=4:fontsize=16:fontcolor=yellow:box=1:boxcolor=black@0.6,tile=${cols}x${rows}:padding=2" -frames:v 1 -q:v 3 "$out"
