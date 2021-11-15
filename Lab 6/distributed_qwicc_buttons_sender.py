import qwiic_button 
import paho.mqtt.client as mqtt
import uuid

client = mqtt.Client(str(uuid.uuid1()))
client.tls_set()
client.username_pw_set('idd', 'device@theFarm')

client.connect(
    'farlab.infosci.cornell.edu',
    port=8883)

topic = 'IDD/maya/qwicc_buttons'

### Initialize Buttons

red_button = qwiic_button.QwiicButton()
green_button = qwiic_button.QwiicButton(0x6E)

if red_button.begin() == False:
    print("The Red Qwiic Button isn't connected to the system. Please check your connection")

if green_button.begin() == False:
    print("The Green Qwiic Button isn't connected to the system. Please check your connection")

while True:
    if red_button.has_button_been_clicked():
        val = f"Red button pressed!"
        print(val)
        client.publish(topic, val)
        red_button.clear_event_bits()
    if green_button.has_button_been_clicked():
        val = f"Green button pressed!"
        print(val)
        client.publish(topic, val)
        green_button.clear_event_bits()