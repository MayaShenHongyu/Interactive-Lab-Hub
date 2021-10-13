from vosk import Model, KaldiRecognizer
import subprocess
import os
import wave
import json

cmd = "arecord -D hw:2,0 -f cd -c1 -r 48000 -d 5 -t wav user_input.wav"
subprocess.call(cmd, shell=True)

if not os.path.exists("../model"):
    print ("Please download the model from https://github.com/alphacep/vosk-api/blob/master/doc/models.md and unpack as 'model' in the current folder.")
    exit (1)

wf = wave.open("user_input.wav", "rb")
if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
    print ("Audio file must be WAV format mono PCM.")
    exit (1)

model = Model("../model")

rec = KaldiRecognizer(model, wf.getframerate(), "hello [unk]")

while True:
    data = wf.readframes(4000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        res = json.loads(rec.Result())
        print("Result:", res['text'])


