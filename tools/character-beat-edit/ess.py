import essentia.standard as es, numpy as np, json
a = es.MonoLoader(filename="song.wav", sampleRate=44100)()
bpm, beats, conf, est, intervals = es.RhythmExtractor2013(method="multifeature")(a)
print("multifeature bpm", round(bpm,2), "confidence", round(conf,2), "(0-5.32; >3.5 = very reliable)")
print("beats", np.round(beats,3).tolist())
print("intervals mean/std", np.mean(intervals).round(4), np.std(intervals).round(4))
bpm2, beats2, *_ = es.RhythmExtractor2013(method="degara")(a)
print("degara bpm", round(bpm2,2)); print("beats2", np.round(beats2,3).tolist())
json.dump({"bpm":float(bpm),"conf":float(conf),"beats":beats.tolist(),"beats2":beats2.tolist()}, open("ess_beats.json","w"))
