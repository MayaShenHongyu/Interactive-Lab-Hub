import time
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789

HEALTHY_DAYS = 0
TOTAL_DAYS = 0

#### Set-up

# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True


### Buttons
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()


### Display text

# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)

def clear_screen():
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)



### Display / interaction

while True:
    clear_screen()

    SUMMARY_1 = 'You have eaten healthy '
    SUMMARY_2 = 'on %d days out of %d days' % (HEALTHY_DAYS, TOTAL_DAYS)
    SUMMARY_3 = 'this year!'
    x = 0
    y = top
    draw.text((x, y), SUMMARY_1, font=font, fill="#FFFFFF")
    y += font.getsize(SUMMARY_1)[1]
    draw.text((x, y), SUMMARY_2, font=font, fill="#FFFFFF")
    y += font.getsize(SUMMARY_2)[1]
    draw.text((x, y), SUMMARY_3, font=font, fill="#FFFFFF")

    # Display image.
    disp.image(image, rotation)

    button_pressed = None

    while button_pressed == None:
        if buttonA.value and not buttonB.value:
            button_pressed = "A"
        if not buttonA.value and buttonB.value:
            button_pressed = "B"


    ATE_HEALTHY = None

    while ATE_HEALTHY == None:
        draw.rectangle((0, 0, width, height), outline=0, fill=0)

        # QUESTION = 'Did you eat healthy today?'
        # x = width - font.getsize(QUESTION)[0]
        # y = top + height / 2 - font.getsize(QUESTION)[1] / 2
        # draw.text((x, y), QUESTION, font=font, fill="#FFFFFF")

        YES = 'Yes :)'
        x = 0
        y = top
        print(str(height), str(y), str(top))
        draw.text((x, y), YES, font=font, fill="#FFFFFF")

        NO = 'Sadly no :('
        x = 0
        y = bottom - font.getsize(NO)[1]
        draw.text((x, y), NO, font=font, fill="#FFFFFF")

        # Display image.
        disp.image(image, rotation)

        time.sleep(0.5)
        
        if buttonA.value and not buttonB.value:
            ATE_HEALTHY = False
        if not buttonA.value and buttonB.value:
            ATE_HEALTHY = True

    
    clear_screen()
    
    if ATE_HEALTHY:
        CONGRATS = 'Good job! Keep it up tomorrow!'
        x = 0
        y = top
        draw.text((x, y), CONGRATS, font=font, fill="#FFFFFF")
        HEALTHY_DAYS += 1
    else:
        TRY = 'Try to eat healthy tomorrow!'
        x = 0
        y = top
        draw.text((x, y), TRY, font=font, fill="#FFFFFF")
    
    TOTAL_DAYS += 1


    # Display image.
    disp.image(image, rotation)
    time.sleep(2)


        

            


            

