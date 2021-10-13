from vosk import Model, KaldiRecognizer
import subprocess
import os
import wave
import json

if not os.path.exists("../model"):
    print ("Please download the model from https://github.com/alphacep/vosk-api/blob/master/doc/models.md and unpack as 'model' in the current folder.")
    exit (1)

USER_INPUT_FILE = "user_input.wav"
model = Model("../model")

def speak(instruction):
    command = """
        say() { 
            local IFS=+;/usr/bin/mplayer -ao alsa -really-quiet -noconsolecontrols "http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q=$*&tl=en"; 
        } ; 
    """ + f"say '{instruction}'"
    subprocess.call(command, shell=True)

def dont_understand():
    speak("What, what are you saying? I don’t understand.")

def what_should_I_do():
    speak("What should I do?")

def record_user_input():
    subprocess.call("arecord -D hw:2,0 -f cd -c1 -r 48000 -d 5 -t wav " + USER_INPUT_FILE, shell=True)


def recognize(pattern):
    
    wf = wave.open(USER_INPUT_FILE, "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        print ("Audio file must be WAV format mono PCM.")
        exit (1)

    rec = KaldiRecognizer(model, wf.getframerate(), pattern)

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            res = json.loads(rec.Result())
            print("Result:", res['text'])
            return res['text']
        # else:
        #     print(rec.PartialResult())
    print("Failed to recognize")
    return ""

# speak("say hello!")
# record_user_input()
# result = recognize("hello")
# if result != None:
#     print("RESULT IS: " + result)
speak("Ahh, there’s a keyhole, let me try… Ok, the door's open, let me see what’s inside, man, it smells so good!")
speak("Now that I have the key, where should I go? Bedroom, Kitchen, or study?")
while True:
    record_user_input()
    result = recognize("bedroom study kitchen")
    if "bedroom" in result:
        speak("Ok, let me see, there’s no key hole on the door, really weird, just something written on the door … What’s in the soup today? What does that mean?")
    elif "study" in result:
        speak("Just like before, I don’t see anything useful, maybe I should do something with the key?")
    elif "kitchen" in result:
        speak("Ahh, there’s a keyhole, let me try… Ok, the door's open, let me see what’s inside, man, it smells so good!")
        passed = True
        break
    else:
        dont_understand()
    what_should_I_do()

