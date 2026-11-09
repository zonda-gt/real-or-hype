import sys
from faster_whisper import WhisperModel
m = WhisperModel(sys.argv[2], device="cpu", compute_type="int8")
import librosa
audio, _ = librosa.load(sys.argv[1], sr=16000)
segs, info = m.transcribe(audio, language="zh", word_timestamps=True, vad_filter=False,
                          initial_prompt=(sys.argv[3] if len(sys.argv) > 3 else None))
for s in segs:
    print(f"{s.start:6.2f} {s.end:6.2f} {s.text}")
    print("      words:", " ".join(f"{w.word}@{w.start:.2f}" for w in s.words))
