import time
import board
import busio

import adafruit_mpr121

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
    time.sleep(0.25)  # Small delay to keep from spamming output messages.
