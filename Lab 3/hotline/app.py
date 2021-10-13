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

speak("Is this 911? Hi, I need help, please! Can you help me?")
while True:
    record_user_input()
    result = recognize("yes")
    if "yes" in result:
        break
    dont_understand()
    speak("Can you help me?")

speak("I lost my memory and I’m now trapped in a room! There’s no one with me, and I don’t remember anything!")
while True:
    record_user_input()
    result = recognize("room see what")
    if result != "":
        break
    dont_understand()

speak("Ok, ok, I’m in a study I guess, there’s a door, let me see … it’s locked, there are many books on a bookshelf, there’s a painting on the wall… and it’s just like a regular study...")
while True:
    record_user_input()
    result = recognize("door painting bookshelf")
    if "door" in result:
        speak("It’s still locked!")
    elif "painting" in result:
        speak("There is nothing special")
    elif "bookshelf" in result:
        speak("Ok, I’ll check the book …… oh! There’s a book that looks strange, let me check… " + 
        "Oh my god, the book is carved hollow inside and there’s a key in it!")
        break
    else:
        dont_understand()
    what_should_I_do()

speak("What do you want me to do with the key?")
while True:
    record_user_input()
    result = recognize("door")
    if "door" in result:
        break
    else:
        dont_understand()
    what_should_I_do()

speak("Ok, now I’m out, I’m in a … hallway I think, quite a simple house, there’s no window though, let me see …… are you still there? I see three rooms, other than the study, one to my left, it says, bathroom, one to my right, I think is the kitchen, and one ahead, should be the bedroom?")
while True:
    record_user_input()
    result = recognize("bathroom kitchen study left right ahead")
    if "bathroom" in result or "left" in result:
        speak("The door is open, god bless, it seems to be… a normal bathroom, quite small.")
        break
    elif "kitchen" in result or "right" in result:
        speak("I can smell something, it smells so good in it, the door is locked, I can’t go in, my god, I’m so hungry, how long has it been! Maybe I should try somewhere else?")
    elif "bedroom" in result or "ahead" in result:
        speak("it’s weird, there’s not even a grip on the door, wait a minute, there’s something written on the door … What’s in the soup today? what? What does that mean? Maybe I should try somewhere else?")
    else:
        dont_understand()
    what_should_I_do()

speak("Now I’m in the bathroom, there’s the bathtub, nothing unusual, the toilet, and a mirror ...")
while True:
    record_user_input()
    result = recognize("bathtub mirror toilet")
    if "bathtub" in result:
        speak("It’s … just a regular bathtub I think...")
    elif "mirror" in result:
        speak("Ok, you are right, I should probably see what I look like, maybe I could remember something? Let me see … Oh My God!! Who am I, what’s wrong with this terrible face! I’m not looking at it anymore!")
    elif "toilet" in result:
        speak("Ok, It’s really dirty, but got to do whatever gets me out of this shithole .... Wait, it’s not flushing, maybe something is clogged, let me check... who would have thought that! Are you like a detective or something? It’s a key! Probably opens the door to the kitchen!")
        break
    else:
        dont_understand()
    what_should_I_do()


speak("Now that I have the key, where should I go? Bedroom, Kitchen, or study?")
while True:
    record_user_input()
    result = recognize("bedroom study kitchen")
    if "bedroom" in result:
        speak("Ok, let me see, there’s no key hole on the door, really weird, just something written on the door … What’s in the soup today? What does that mean?")
    elif "study" in result:
        speak("Just like before, I don’t see anything useful, maybe I should do something with the key?")
    elif "kitchen" in result:
        speak("Ahh, there’s a keyhole, let me try… Ok, the door’s open, let me see what’s inside, man, it smells so good!")
        break
    else:
        dont_understand()
    what_should_I_do()

