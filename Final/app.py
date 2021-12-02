from vosk import Model, KaldiRecognizer
import subprocess
import os
import wave
import json
import threading
import time
import schedule
import board
import adafruit_mpu6050
import requests


def run_continuously(interval=1):
    """Continuously run, while executing pending jobs at each
    elapsed time interval.
    @return cease_continuous_run: threading. Event which can
    be set to cease continuous run. Please note that it is
    *intended behavior that run_continuously() does not run
    missed jobs*. For example, if you've registered a job that
    should run every minute and you set a continuous run
    interval of one hour then your job won't be run 60 times
    at each interval but only once.
    """
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run


i2c = board.I2C()  # uses board.SCL and board.SDA
mpu = adafruit_mpu6050.MPU6050(i2c)


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
    subprocess.call("arecord -D hw:2,0 -f cd -c1 -r 48000 -d " + str(time) + " -t wav " + USER_INPUT_FILE, shell=True)

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


def initilaize_plant():
    pass

def tell_joke():
    speak("Tells joke")
    pass

def tell_time():
    speak("Tells time")
    pass

def plant_summary():
    speak("Tells plant summary")
    pass


def measure_temp():
    print('Hello from the background thread')
    temp = mpu.temperature
    print(f"Temperature: ${temp}")
    payload = {'temperature': temp, 'time': time.strftime("%H:%M:%S\n")}
    # requests.put('https://httpbin.org/put', data=payload)
    # requests.get('https://httpbin.org/get', params=payload) # https://httpbin.org/get?key2=value2&key1=value1


schedule.every(5).seconds.do(measure_temp)

# Start the background thread
stop_run_continuously = run_continuously(5)


while True:
    record_user_input(2)
    if recognize("cactus hey"):
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
            key = recognize("no joke time how doing water temperature")
            
            if "no" in key and gone_silent == 2:
                speak("Ok. Catch you later.")
                break
            
            if key:
                gone_silent = 0
                if "joke" in key:
                    tell_joke()
                elif "time" in key:
                    tell_time()
                elif "how" in key or "doing" in key:
                    plant_summary()
                elif "water" in key:
                    pass
                elif "temperature" in key:
                    pass
            else:
                gone_silent += 1
                if gone_silent == 6:
                    speak("Ok. Guess you‘re not there. Catch you later.")
                    break

# Do some other things...
time.sleep(10)

# Stop the background thread
stop_run_continuously.set()