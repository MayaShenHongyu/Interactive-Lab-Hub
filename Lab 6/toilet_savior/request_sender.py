import paho.mqtt.client as mqtt
import uuid
import subprocess
import qwiic_button 
import time

DEVICE_ID = 1

requested_toilet_paper = False

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

#connect to the broker
client.connect(
    'farlab.infosci.cornell.edu',
    port=8883)


request_topic = 'IDD/toilet_savior/request/' + str(DEVICE_ID)
respond_topic = 'IDD/toilet_savior/respond'

#this is the callback that gets called once we connect to the broker. 
#we should add our subscribe functions here as well
def on_connect(client, userdata, flags, rc):
	print(f"connected with result code {rc}")
	client.subscribe(respond_topic)
	# you can subsribe to as many topics as you'd like
	# client.subscribe('some/other/topic')


# this is the callback that gets called each time a message is recived
def on_message(cleint, userdata, msg):
	# you can filter by topics
	# if msg.topic == 'IDD/some/other/topic': do thing
    if msg.payload.decode('UTF-8') == str(DEVICE_ID) and requested_toilet_paper:
        speak("Confirm! Someone is on their way to save you!")
    
    print(f"topic: {msg.topic} msg: {msg.payload.decode('UTF-8')}")

# attach out callbacks to the client
client.on_connect = on_connect
client.on_message = on_message

client.loop_start()

red_button.clear_event_bits()
red_button.LED_off()
while True:
    if red_button.has_button_been_clicked():
        red_button.clear_event_bits()
        if requested_toilet_paper == False:
            client.publish(request_topic, "Need toilet paper!")
            requested_toilet_paper = True
            red_button.LED_on(100)
        else:
            client.publish(request_topic, "No longer need toilet paper!")
            requested_toilet_paper = False
            red_button.LED_off()
    time.sleep(0.2)


