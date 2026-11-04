#!/usr/bin/env bash
# usage: vr_all.sh <workdir> A B C   — render, subtitle, add SFX, QA. Stops on the first failure.
set -euo pipefail
cd "$1"; shift
for v in "$@"; do
  mkdir -p vr/$v/seg
  python3 -I scripts/vr_render.py "$PWD" $v > vr/$v/render.log
  tail -1 vr/$v/render.log > vr/$v/starts.txt
  python3 -c "import ast;ast.literal_eval(open('vr/$v/starts.txt').read())" || { echo "render $v failed:"; cat vr/$v/render.log; exit 1; }
  python3 -I scripts/cutcheck.py "$PWD" scripts/variants.py $v | tail -1
  python3 -I scripts/subs.py "$PWD" vr/$v/starts.txt vr/$v/subs.ass v11/vo vr/$v/lines.json vr/$v/seg 2>/dev/null | tail -1
  ffmpeg -loglevel error -y -i vr/$v/base.mp4 -vf "ass=vr/$v/subs.ass:fontsdir=vr/fontsdir" -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -c:a copy vr/$v/subbed.mp4
  python3 -I scripts/add_sfx.py "$PWD" vr/$v/subbed.mp4 vr/$v/starts.txt vr/$v/final_$v.mp4
  earshot/.venv/bin/python -m earshot measure vr/$v/final_$v.mp4 2>/dev/null | cut -c1-90
done
echo ALL_RENDERED
