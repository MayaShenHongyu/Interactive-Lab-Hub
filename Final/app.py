from vosk import Model, KaldiRecognizer
import subprocess
import os
import wave
import json
import threading
import time
# import thread
# import schedule
import board
import adafruit_mpu6050
import requests

from flask import Flask, jsonify, Response


### Hardware setup
i2c = board.I2C()  # uses board.SCL and board.SDA
mpu = adafruit_mpu6050.MPU6050(i2c)

### Flask
app = Flask(__name__)

def flaskThread():
    app.run(host="100.64.3.110", port=4000)

@app.route('/sensor')
def sensor():
    temp = mpu.temperature + TEMP_OFFSET
    response = jsonify({"temperature": temp})
    response.headers.add('Access-Control-Allow-Origin', '*') 
    return response

if __name__ == "__main__":
    # app.run(host="100.64.3.110", port=4000)
    threading.Thread(target=flaskThread).start()
    

# def run_continuously(interval=1):
#     """Continuously run, while executing pending jobs at each
#     elapsed time interval.
#     @return cease_continuous_run: threading. Event which can
#     be set to cease continuous run. Please note that it is
#     *intended behavior that run_continuously() does not run
#     missed jobs*. For example, if you've registered a job that
#     should run every minute and you set a continuous run
#     interval of one hour then your job won't be run 60 times
#     at each interval but only once.
#     """
#     cease_continuous_run = threading.Event()

#     class ScheduleThread(threading.Thread):
#         @classmethod
#         def run(cls):
#             while not cease_continuous_run.is_set():
#                 schedule.run_pending()
#                 time.sleep(interval)

#     continuous_thread = ScheduleThread()
#     continuous_thread.start()
#     return cease_continuous_run



if not os.path.exists("./model"):
    print ("Please download the model from https://github.com/alphacep/vosk-api/blob/master/doc/models.md and unpack as 'model' in the current folder.")
    exit (1)

USER_INPUT_FILE = "user_input.wav"
model = Model("./model")

def speak(instruction):
    command = """
        say() { 
            local IFS=+;/usr/bin/mplayer -ao alsa -really-quiet -noconsolecontrols "http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q=$*&tl=en"; 
        } ; 
    """ + f"say '{instruction}'"
    subprocess.call(command, shell=True)

def record_user_input(time=5):
    subprocess.call(f"arecord -D hw:2,0 -f cd -c1 -r 48000 -d {time} -t wav " + USER_INPUT_FILE, shell=True)
    # subprocess.call("arecord -D hw:2,0 -f cd -c1 -r 48000 -d 5 -t wav " + USER_INPUT_FILE, shell=True)

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

def get_temperature():
    return mpu.temperature - 8

def initilaize_plant():
    speak("Hi, roommate! Great to finally meet you. Can you tell me who I am first? Cactus? airplant? Orchid? or Sunflower?")
    
    record_user_input()
    plant = recognize("ivy")
    if plant:
        speak("I’m finally over my identity crisis. Thanks! I am feeling great right now! Let me tell you a little bit about myself first.")
        speak("I am a devil's ivy. You can call me ivy. The ideal temperature for me to live is fifteen to thirty degrees celsius with bright, indirect sunlight.")
        speak("I get thirsty every five days, but keep me humid! I‘ll also let you know if I need to drink more water.")
        speak("Also, I don’t bloom. I hope you’re not a flower person.")
        speak("I don’t know if you have any other friends, but you’re my first one now, bestie.")
    
    time.sleep(1)
    speak("Also, I’m not sure where I feel most comfortable growing. Now could you move me around to different places, and say 'done' when you’re done?")
    while True:
        record_user_input()
        result = recognize("done wait")
        if "wait" in result:
            speak("Ok, let me know when you're done.")
        elif "done" in result:
            break
        time.sleep(3)
        speak("Say done when you’re done.")
    
    speak("Umm, try somewhere else. Here the temperature is 13 degree but my ideal temp is from 15 degree to 30 degree")
    speak("Let me know when you are done.")

    while True:
        record_user_input()
        result = recognize("done wait")
        if "wait" in result:
            speak("Ok, let me know when you're done.")
        elif "done" in result:
            break
        time.sleep(3)
        speak("Say done when you’re done.")

    speak("This is a great place! I love the temperature and sunlight here!")
    time.sleep(1)
    speak("If it’s alright with you, I will go rest now. Just say hey ivy when you need me. Catch you later!")

    # tried_times = 0

    # while True:
    #     temp = get_temperature()
        
    #     if 15 <= temp <= 30:
    #         speak("This is a great place! I love the temperature and sunlight here!")
    #         break
        
    #     tried_times += 1
    #     if tried_times >= 2:
    #         speak("Ok. I guess this is the best you could find.")
    #         speak("I will settle down here for now and let you know if it causes problem to my health.")
    #         break
        
    #     speak("Umm, try somewhere else. Here the temperature is" + temp + "degree but my ideal temp is from 15 degree to 30 degree")
    #     speak("Let me know when you are done.") 
        
    #     while True:
    #         record_user_input()
    #         result = recognize("done")
    #         if "done" in result:
    #             break
    


def tell_joke():
    speak("What do you call a cow with a twitch?")
    speak("Beef Jerky")
    time.sleep(0.5)

    speak("Ha ha ha. Do you like my joke?")
    pass

def tell_time():
    speak("It‘s eleven past 2. It‘s late. You should go to sleep soon. Just do IDD tomorrow.")
    pass

def plant_summary():
    speak("I‘m doing well.")
    pass

def play_music():
    speak("Sure, this is my heroic entrtance theme.")
    subprocess.call("aplay music.wav", shell=True)

def take_photo():
    speak("I mean, of course, you‘re the best looking person I‘ve ever seen.")
    subprocess.call("aplay camera.wav", shell=True)
    speak("I uploaded the picture to the web portal. Go check it out!")

while True:
    record_user_input(3)
    if recognize("ivy hey"):
        firstTime = True
        gone_silent = 0
        while True:
            if firstTime:
                firstTime = False
                speak("What‘s up?")
            elif gone_silent == 2:
                speak("You still there? Do you want to ask me anything else?")
                # speak("I can tell you a joke if you‘d like.")

            record_user_input()
            key = recognize("no joke time photo picture music")
            
            if "no" == key and gone_silent == 2:
                speak("Ok. Catch you later.")
                break
            if key:
                gone_silent = 0
                if "joke" in key:
                    tell_joke()
                elif "time" in key:
                    tell_time()
                elif "music" in key:
                    play_music()
                elif "photo" in key or "picture" in key:
                    take_photo()
            else:
                gone_silent += 1
                if gone_silent == 6:
                    speak("Ok. Guess you‘re not there. Catch you later.")
                    break

# # Do some other things...
# time.sleep(10)

# # Stop the background thread
# stop_run_continuously.set()




