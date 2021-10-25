import time
import board
import busio

import adafruit_mpr121

import subprocess  


i2c = busio.I2C(board.SCL, board.SDA)

mpr121 = adafruit_mpr121.MPR121(i2c)

yellow = 9
green = 11
red = 5
white = 2


while True:
    for i in range(12):
        if mpr121[i].value:
            print(f"Twizzler {i} touched!")
    if mpr121[yellow].value: 
        subprocess.call("aplay llama.wav", shell=True)
    elif mpr121[green].value: 
        subprocess.call("aplay bear.wav", shell=True)
    elif mpr121[red].value: 
        subprocess.call("aplay fox.wav", shell=True)
    elif mpr121[white].value: 
        subprocess.call("aplay hello.wav", shell=True)
    # time.sleep(0.25)  # Small delay to keep from spamming output messages.
