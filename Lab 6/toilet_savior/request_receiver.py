import paho.mqtt.client as mqtt
import uuid
import subprocess
import qwiic_button 
import time

requested_toilet_id = None

red_button = qwiic_button.QwiicButton()

if red_button.begin() == False:
    print("The Red Qwiic Button isn't connected to the system. Please check your connection")


def speak(instruction):
    command = """
        say() { 
            local IFS=+;/usr/bin/mplayer -ao alsa -really-quiet -noconsolecontrols "http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q=$*&tl=en"; 
        } ; 
    """ + f"say '{instruction}'"
    subprocess.call(command, shell=True)


# Every client needs a random ID
client = mqtt.Client(str(uuid.uuid1()))
# configure network encryption etc
client.tls_set()
# this is the username and pw we have setup for the class
client.username_pw_set('idd', 'device@theFarm')


request_topic = 'IDD/toilet_savior/request'
respond_topic = 'IDD/toilet_savior/respond'

#this is the callback that gets called once we connect to the broker. 
#we should add our subscribe functions here as well
def on_connect(client, userdata, flags, rc):
	print(f"connected with result code {rc}")
	client.subscribe(request_topic)
	# you can subsribe to as many topics as you'd like
	# client.subscribe('some/other/topic')


# this is the callback that gets called each time a message is recived
def on_message(cleint, userdata, msg):
	# you can filter by topics
	# if msg.topic == 'IDD/some/other/topic': do thing
    request_toilet_id = msg.topic.split("/")[-1]
    if msg.payload.decode('UTF-8') == "Need toilet paper!":
        speak("Toilet " + request_toilet_id + " needs paper!")
        global requested_toilet_id
        requested_toilet_id = request_toilet_id
        red_button.LED_config(100, 500, 100)
    else:
        red_button.LED_off()
    print(f"topic: {msg.topic} msg: {msg.payload.decode('UTF-8')}")

# attach out callbacks to the client
client.on_connect = on_connect
client.on_message = on_message

#connect to the broker
client.connect(
    'farlab.infosci.cornell.edu',
    port=8883)

client.loop_start()

while True:
    if red_button.has_button_been_clicked():
        red_button.clear_event_bits()
        client.publish(respond_topic, requested_toilet_id)
        red_button.LED_on(100)


