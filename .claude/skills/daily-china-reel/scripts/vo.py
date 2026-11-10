#!/usr/bin/env python3
"""Narration in the creator's ElevenLabs clone (eleven_v3), several takes per line, Whisper-checked.

  vo.py EPISODE_DIR [--takes 3] [--tempo 1.3] [--voice ID]

Reads EPISODE_DIR/episode.json ("lines": [{"id", "say", "check"}]), where "say" is the text sent to
ElevenLabs (Chinese characters for place names, so v3 says them in Mandarin) and "check" is the
English part Whisper must hear (the place name is left out, Whisper can't spell it). Writes
EPISODE_DIR/vo/<id>.wav (trimmed, inner pauses squeezed, sped up) and vo/lines.json with each
line's duration and "cut": the time "go to" starts, where the edit cuts to the second shot.
Takes are cached in vo/takes/, so a re-run only pays for what is missing.
"""
import argparse, difflib, json, os, re, subprocess, sys, time
import requests

VOICE = "KdPzirZUC0HY6WhfwyeE"  # "Real or Hype - creator voice v2" (Instant Voice Clone)
SETTINGS = {"stability": 0.5, "similarity_boost": 0.9, "style": 0.15, "use_speaker_boost": True}
_model = None


def whisper():
    global _model
    if _model is None:
        from faster_whisper import WhisperModel
        _model = WhisperModel("small", device="cpu", compute_type="int8")
    return _model


def words(path):
    import numpy as np  # decode with ffmpeg: some PyAV builds break faster-whisper's own decoder
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "s16le", "-ac", "1", "-ar", "16000", "-"],
                         capture_output=True, check=True).stdout
    audio = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
    segs, _ = whisper().transcribe(audio, language="en", word_timestamps=True, beam_size=5)
    return [w for s in segs for w in s.words]


def norm(t):
    return re.sub(r"[^a-z' ]", " ", t.lower()).split()


def tts(text, out, voice):
    body = {"text": text, "model_id": "eleven_v3", "voice_settings": SETTINGS}
    for i in range(4):
        r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{voice}?output_format=mp3_44100_128",
                          json=body, headers={"xi-api-key": os.environ["ELEVENLABS_API_KEY"]}, timeout=180)
        if r.status_code == 200:
            open(out, "wb").write(r.content); return
        print("elevenlabs", r.status_code, r.text[:200], file=sys.stderr)
        if r.status_code in (401, 403, 422):
            sys.exit(1)
        time.sleep(2 ** (i + 1))
    sys.exit("elevenlabs failed")


def process(src, out, tempo):
    # trim both ends, squeeze inner pauses to ~0.12 s, speed up, 48 kHz mono
    af = ("silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.02,areverse,"
          "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,areverse,"
          "silenceremove=stop_periods=-1:stop_duration=0.14:stop_threshold=-45dB:stop_silence=0.12,"
          f"atempo={tempo},aresample=48000")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-af", af, "-ac", "1", out], check=True)


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                                capture_output=True, text=True).stdout)


def score(ws, check):
    heard = norm(" ".join(w.word for w in ws))
    want = norm(check)
    # every expected word must be heard, in order, before the place name
    m = difflib.SequenceMatcher(a=want, b=heard[:len(want) + 2])
    return sum(b.size for b in m.get_matching_blocks()) / max(1, len(want)), " ".join(heard)


def cut_time(ws):
    t = [norm(w.word) for w in ws]
    for i in range(len(ws) - 1):
        if t[i] == ["go"] and t[i + 1] and t[i + 1][0] in ("to", "too", "two"):
            return ws[i].start
    return None


def main():
    p = argparse.ArgumentParser()
    p.add_argument("ep"); p.add_argument("--takes", type=int, default=3)
    p.add_argument("--tempo", type=float, default=None); p.add_argument("--voice", default=VOICE)
    p.add_argument("--only", default="")
    x = p.parse_args()
    ep = json.load(open(f"{x.ep}/episode.json"))
    tempo = x.tempo or ep.get("vo_tempo", 1.3)
    os.makedirs(f"{x.ep}/vo/takes", exist_ok=True)
    res_path = f"{x.ep}/vo/lines.json"
    res = json.load(open(res_path)) if os.path.exists(res_path) else {}
    for ln in ep["lines"]:
        lid = ln["id"]
        if x.only and lid not in x.only.split(","):
            continue
        best = None
        for k in range(x.takes):
            raw = f"{x.ep}/vo/takes/{lid}_{k}.mp3"
            if not os.path.exists(raw):
                tts(ln["say"], raw, x.voice)
            proc = f"{x.ep}/vo/takes/{lid}_{k}.wav"
            process(raw, proc, tempo)
            ws = words(proc)
            s, heard = score(ws, ln["check"])
            d = dur(proc)
            c = cut_time(ws) if ln.get("split", True) else None
            ok = s >= 0.95 and (c is not None or not ln.get("split", True))
            print(f"{lid} take {k}: {d:.2f}s score {s:.2f} cut {c} {'OK' if ok else '--'} | {heard}")
            if ok and (best is None or d < best[1]):
                best = (proc, d, c, heard)
        if best is None:
            print(f"{lid}: NO TAKE PASSED. Rewrite the line or add takes (--takes 6 --only {lid})")
            continue
        out = f"{x.ep}/vo/{lid}.wav"
        subprocess.run(["cp", best[0], out], check=True)
        res[lid] = {"wav": out, "dur": round(best[1], 3), "cut": None if best[2] is None else round(best[2], 3),
                    "heard": best[3], "tempo": tempo}
    json.dump(res, open(res_path, "w"), indent=1)
    missing = [l["id"] for l in ep["lines"] if l["id"] not in res]
    print("total voice", round(sum(r["dur"] for r in res.values()), 2), "s; missing:", missing or "none")


if __name__ == "__main__":
    main()
