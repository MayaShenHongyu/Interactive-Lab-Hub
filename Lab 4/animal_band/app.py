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


# while True:
#     for i in range(12):
#         if mpr121[i].value:
#             print(f"Twizzler {i} touched!")
#     if mpr121[yellow].value: 
#         subprocess.call("aplay llama.wav", shell=True)
#         # subprocess.Popen(['aplay', 'llama.wav'])
#     elif mpr121[green].value: 
#         subprocess.call("aplay bear.wav", shell=True)
#         # subprocess.Popen(['aplay', 'bear.wav'])
#     elif mpr121[red].value: 
#         subprocess.call("aplay fox.wav", shell=True)
#         # subprocess.Popen(['aplay', 'fox.wav'])
#     elif mpr121[white].value: 
#         subprocess.call("aplay hello.wav", shell=True)
#         # subprocess.Popen(['aplay', 'hello.wav'])
#     # time.sleep(0.25)  # Small delay to keep from spamming output messages.


while True:
    for i in range(12):
        if mpr121[i].value:
            print(f"Twizzler {i} touched!")
    if mpr121[yellow].value: 
        subprocess.Popen(['aplay', 'llama.wav'], start_new_session=True)
    elif mpr121[green].value: 
        subprocess.Popen(['aplay', 'bear.wav'], start_new_session=True)
    elif mpr121[red].value: 
        subprocess.Popen(['aplay', 'fox.wav'], start_new_session=True)
    elif mpr121[white].value: 
        subprocess.Popen(['aplay', 'hello.wav'], start_new_session=True)
    # time.sleep(0.25)  # Small delay to keep from spamming output messages.
