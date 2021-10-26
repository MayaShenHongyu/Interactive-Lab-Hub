import time
import board
import busio

import adafruit_mpr121

import subprocess  
import board
import busio
from i2c_button import I2C_Button

import qwiic_button 


i2c = busio.I2C(board.SCL, board.SDA)

mpr121 = adafruit_mpr121.MPR121(i2c)

# scan the I2C bus for devices
while not i2c.try_lock():
	pass
devices = i2c.scan()
i2c.unlock()
print('I2C devices found:', [hex(n) for n in devices])
default_addr = 0x6f
if default_addr not in devices:
	print('warning: no device at the default button address', default_addr)

my_button = qwiic_button.QwiicButton()
my_button2 = qwiic_button.QwiicButton(0x5B)

if my_button.begin() == False:
    print("The Qwiic Button isn't connected to the system. Please check your connection")

if my_button2.begin() == False:
    print("The Qwiic Button isn't connected to the system. Please check your connection")

print("Button ready!")
print(my_button.get_I2C_address(), my_button2.get_I2C_address())

while True:   
        
    if my_button.is_button_pressed() == True:
        print("\nThe first button is pressed!")

    if my_button.is_button_pressed() == True:
        print("\nThe second button is pressed!")
        
    time.sleep(0.02)


# button = I2C_Button(i2c)
# button.clear()
# button.led_bright = 0
# button.led_gran = 1
# button.led_cycle_ms = 0
# button.led_off_ms = 100

# while True:
#     button.clear() # status must be cleared manually
#     time.sleep(0.1)
#     print('status', button.status)
#     # print('last click ms', button.last_click_ms)
#     # print('last press ms', button.last_press_ms)

yellow = 9
green = 11
red = 5
white = 2


while True:
    for i in range(12):
        if mpr121[i].value:
            print(f"Twizzler {i} touched!")
    if mpr121[yellow].value: 
        subprocess.Popen(['aplay', 'llama.wav'], start_new_session=True)
    if mpr121[green].value: 
        subprocess.Popen(['aplay', 'bear.wav'], start_new_session=True)
    if mpr121[red].value: 
        subprocess.Popen(['aplay', 'fox.wav'], start_new_session=True)
    if mpr121[white].value: 
        subprocess.Popen(['aplay', 'hello.wav'], start_new_session=True)
    time.sleep(0.1)  # Small delay to keep from spamming output messages.
