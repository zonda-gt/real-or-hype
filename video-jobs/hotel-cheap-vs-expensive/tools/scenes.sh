#!/bin/bash
ffmpeg -v info -i "$1" -vf "select='gt(scene,${2:-0.3})',showinfo" -f null - 2>&1 | grep -o 'pts_time:[0-9.]*' | cut -d: -f2 | tr '\n' ' '
