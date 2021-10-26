import time
import board
import busio

import adafruit_mpr121
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont

import subprocess  
import board
import busio

import qwiic_button 


YELLOW_INDEX = 9
GREEN_INDEX = 11
RED_INDEX = 5
WHITE_INDEX = 2

i2c = busio.I2C(board.SCL, board.SDA)

mpr121 = adafruit_mpr121.MPR121(i2c)
disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)


red_button = qwiic_button.QwiicButton()
green_button = qwiic_button.QwiicButton(0x6E)

if red_button.begin() == False:
    print("The Red Qwiic Button isn't connected to the system. Please check your connection")

if green_button.begin() == False:
    print("The Green Qwiic Button isn't connected to the system. Please check your connection")




# start with a blank screen
disp.fill(0)
# we just blanked the framebuffer. to push the framebuffer onto the display, we call show()
disp.show()

width = disp.width
height = disp.height

image = Image.new("1", (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0


font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
font2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=0)
draw.text((x, top), "Animal Band!", font=font, fill=255)
disp.image(image)
disp.show()

red_button.clear_event_bits()
green_button.clear_event_bits()

while True:   
        
    if red_button.is_button_pressed() == True:
        print("\nThe first button is pressed!")

    if green_button.is_button_pressed() == True:
        print("\nThe second button is pressed!")
        
    time.sleep(0.02)

while True:
    
    while True:
        time.sleep(0.02)
        if red_button.has_button_been_clicked():
            red_button.clear_event_bits()
            break
    
    
    while True:
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
        draw.text((x, top), "Recording...", font=font, fill=255)
        disp.image(image)
        disp.show()
        if red_button.has_button_been_clicked():
            red_button.clear_event_bits()
            break
        for i in range(12):
            if mpr121[i].value:
                print(f"Twizzler {i} touched!")
        if mpr121[YELLOW_INDEX].value: 
            subprocess.Popen(['aplay', 'llama.wav'], start_new_session=True)
        if mpr121[GREEN_INDEX].value: 
            subprocess.Popen(['aplay', 'bear.wav'], start_new_session=True)
        if mpr121[RED_INDEX].value: 
            subprocess.Popen(['aplay', 'fox.wav'], start_new_session=True)
        if mpr121[WHITE_INDEX].value: 
            subprocess.Popen(['aplay', 'hello.wav'], start_new_session=True)
        time.sleep(0.1)  # Small delay to keep from spamming output messages.

    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    draw.text((x, top), "You have a recording to play", font=font2, fill=255)
    disp.image(image)
    disp.show()

    while True:
        time.sleep(0.02)
        if green_button.has_button_been_clicked():
            print("????")
            green_button.clear_event_bits()
            break



    





