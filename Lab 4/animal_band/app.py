import time
import board
import busio

import adafruit_mpr121
import asyncio  
from asyncio.subprocess import PIPE, STDOUT  
import subprocess  
import signal



i2c = busio.I2C(board.SCL, board.SDA)

mpr121 = adafruit_mpr121.MPR121(i2c)

yellow = 9
green = 11
red = 5
white = 2


cmd1 = "aplay llama.wav"
process = asyncio.create_subprocess_shell(cmd1, stdin = PIPE, stdout = PIPE, stderr = STDOUT)

time.sleep(1)

process.wait()
print("???")


while True:
    for i in range(12):
        if mpr121[i].value:
            print(f"Twizzler {i} touched!")
    time.sleep(0.25)  # Small delay to keep from spamming output messages.
