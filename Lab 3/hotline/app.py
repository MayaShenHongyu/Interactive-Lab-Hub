from vosk import Model, KaldiRecognizer
import subprocess
import os
import wave
import json
import board
from adafruit_seesaw import seesaw, rotaryio, digitalio
from playsound import playsound

# For use with the STEMMA connector on QT Py RP2040
# import busio
# i2c = busio.I2C(board.SCL1, board.SDA1)
# seesaw = seesaw.Seesaw(i2c, 0x36)

seesaw = seesaw.Seesaw(board.I2C(), addr=0x36)

seesaw_product = (seesaw.get_version() >> 16) & 0xFFFF
print("Found product {}".format(seesaw_product))
if seesaw_product != 4991:
    print("Wrong firmware loaded?  Expected 4991")

seesaw.pin_mode(24, seesaw.INPUT_PULLUP)
button = digitalio.DigitalIO(seesaw, 24)
button_held = False

encoder = rotaryio.IncrementalEncoder(seesaw)
last_position = None

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

pickedUp = False
while not pickedUp:
    subprocess.call("aplay ring.wav", shell=True)
    if not button.value and not button_held:
        button_held = True
        pickedUp = True
    if button.value and button_held:
        button_held = False
        pickedUp = True

speak("Is this 911? Hi, I need help, please! Can you help me?")
while True:
    record_user_input()
    result = recognize("yes sure")
    if result != "":
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
# fix this

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
    speak("Should I check the door, the painting, or the bookshelf?")

speak("What do you want me to do with the key?")
while True:
    record_user_input()
    result = recognize("door")
    if "door" in result:
        break
    else:
        dont_understand()
    speak("What do you want me to do with the key?")

speak("Ok, now I’m out, I’m in a hallway I think, quite a simple house, there’s no window though, let me see …… ")
speak("Are you still there? I see three rooms, other than the study, one to my left, it says, bathroom, one to my right, I think is the kitchen, and one ahead, should be the bedroom?")
speak("Where should I go?")
while True:
    record_user_input()
    result = recognize("bathroom kitchen study")
    if "bathroom" in result:
        speak("The door is open, god bless, it seems to be… a normal bathroom, quite small.")
        break
    elif "kitchen" in result:
        speak("I can smell something, it smells so good in it, the door is locked, I can’t go in, my god, I’m so hungry, how long has it been! Maybe I should try somewhere else?")
    elif "bedroom" in result:
        speak("it’s weird, there’s not even a grip on the door, wait a minute, there’s something written on the door … What’s in the soup today? what? What does that mean? Maybe I should try somewhere else?")
    else:
        dont_understand()
    speak("Where should I go? Bathroom, kitchen, or bedroom?")

while True:

    # negate the position to make clockwise rotation positive
    position = -encoder.position

    if position != last_position:
        last_position = position
        print("Position: {}".format(position))


speak("Now I’m in the bathroom, there’s the bathtub, nothing unusual, the toilet, and a mirror ...")
speak("Which one should I check first?")
while True:
    record_user_input()
    result = recognize("bathtub mirror toilet")
    if "bathtub" in result:
        speak("It’s … just a regular bathtub I think...")
    elif "mirror" in result:
        speak("Ok, you are right, I should probably see what I look like, maybe I could remember something? Let me see … Oh My God!! Who am I, what’s wrong with this terrible face! I’m not looking at it anymore!")
    elif "toilet" in result:
        speak("Ok, It’s really dirty, but got to do whatever gets me out of this shithole .... Wait, it’s not flushing, maybe something is clogged, let me check... who would have thought that!")
        speak("Are you like a detective or something? It’s a key! Probably opens the door to the kitchen!")
        break
    else:
        dont_understand()
    speak("Should I check the bathtub, mirror, or toilet?")


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
    speak("Should I go to the bedroom, kitchen, or study?")

speak("So… Here’s the kitchen, some bowls … some bread, the stove is still on, and something is boiling in the pot, dang, that smells so good.") 
speak("I wonder what’s in it… should I go check the pot?")
record_user_input()
result = recognize("yes pot check why not what inside")
if result == "":
    speak("Oh I’m too hungry, I need to know what smells that good")
speak("It’s soup! I need to have some…")
speak("Ok, it tastes like heaven, my lord, I think there’s tomatoes, chicken, onions, and chilies, I wish you could be here to taste it.")

speak("Ok, enough soup, what should I do now? Should I go Bathroom, study, or bedroom?")
while True:
    record_user_input()
    result = recognize("bedroom study bathroom")
    if "bedroom" in result:
        speak("Yes! The soup! Maybe that will solve the puzzle!")
        break
    elif "study" in result:
        speak("Still the same old study, maybe I should check out other rooms?")
    elif "bathroom" in result:
        speak("eww, it’s dirty, not going back again")
    else:
        dont_understand()
    speak("Should I go to the bathroom, study, or bedroom?")

speak("Ok, now I’m at the bedroom door, it’s hardly a door, no grip or anything, a question on it though...")
speak("What’s in the soup today? Oh man, I shouldn’t have finished it all, do you still remember what’s in it?")
record_user_input()
result = recognize("tomato chicken onion chilli")
if result == "":
    speak("Hmmm I think there’s tomato in it...")
    result = "tomato"
else:
    speak("Yes, yes, I still remember that taste! You are right!")

speak("So… should I just say the word?" + result + result)
speak("Holy shit, it’s opening! The door opened automatically, is someone listening to me?")
speak("Ok, there’s the bed, of course, queen size I guess, looking cozy, a computer on the desk, and a book on the nightstand… What should I do?")
while True:
    record_user_input()
    result = recognize("bed desk computer book nightstand")
    if "bed" in result:
        speak("I’m not going to sleep at this time, maybe something else?")
    elif "desk" in result or "computer" in result:
        speak("You are right, maybe I can connect to the internet … ok it’s totally dead, just a decoration I guess…, maybe something else?")
    elif "book" in result or "nightstand" in result:
        speak("Sure, it’s never late to read, here’s a bookmarked page...")
        speak("Painting is always a good place for many private people to hide their secrets in their home")
        speak("many indoor designs leave a secret space on the wall that is covered by paintings and decorations … wait, that sounds real familiar... ")
        break
    else:
        dont_understand()
    speak("Should I check the bed, desk, or the nightstand?")

speak("I think that’s it for the bedroom, where should I go next, I don’t see another new door")
speak("Should I go back to the kitchen, or bathroom, or study?")
while True:
    record_user_input()
    result = recognize("study bathroom kitchen")
    if "study" in result:
        speak("Wait, you are right, there’s a painting there! Maybe something hidden!")
        break
    elif "bathroom" in result:
        speak("eww, it’s dirty, not going back again!")
    elif "kitchen" in result:
        speak("No soup there anymore, maybe somewhere else?")
    else:
        dont_understand()
    speak("Should I go to the kitchen, or bathroom, or study?")

speak("Ok, study, the painting, let’s see what’s behind it… My god, there is actually something!")
speak("Can you imagine that? There’s a half-full vile of some greenish fluid … and a note … Drink it and you will be free.")
speak("What does that mean? Should I drink it? Shoot… the phone is going to die … hey, hey can you still hear me... should I drink …")

speak("The connection has been lost. After an hour or so, you received another call suddenly")
speak("Is this 911, hi, I need help, please! Can you help me?")
speak("I lost my memory and I’m now trapped in a room! There’s no one with me, and I don’t remember anything!")