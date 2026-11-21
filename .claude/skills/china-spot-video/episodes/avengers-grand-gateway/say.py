import sys,soundfile as sf
from kokoro_onnx import Kokoro
k=Kokoro('/home/user/real-or-hype/work/tts/kokoro-v1.0.onnx','/home/user/real-or-hype/work/tts/voices-v1.0.bin')
text=open(sys.argv[1]).read().strip(); voice=sys.argv[2]; out=sys.argv[3]; sp=float(sys.argv[4]) if len(sys.argv)>4 else 1.0
s,sr=k.create(text,voice=voice,speed=sp,lang='en-us'); sf.write(out,s,sr)
