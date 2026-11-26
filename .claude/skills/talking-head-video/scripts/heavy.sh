#!/bin/bash
# heavy.sh <cmd...>: run a memory-heavy command (Whisper, demucs, HyperFrames render/snapshot/check) in one of 2 slots
while true; do
  for L in 1 2; do
    exec 9>/tmp/claude-0/-home-user-real-or-hype/d19943c7-4785-5b96-ac45-70ac94e4bbed/scratchpad/.heavy$L.lock
    if flock -n 9; then "$@"; rc=$?; flock -u 9; exit $rc; fi
  done
  sleep 3
done
