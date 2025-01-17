import time
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789

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
    draw.rectangle((0, 0, width, height), outline=0, fill="#FFFFFF")

def rescale_image(image):
    image_ratio = image.width / image.height
    screen_ratio = width / height
    if screen_ratio < image_ratio:
        scaled_width = image.width * height // image.height
        scaled_height = height
    else:
        scaled_width = width
        scaled_height = image.height * width // image.width
    image = image.resize((scaled_width, scaled_height), Image.BICUBIC)

    # Crop and center the image
    x = scaled_width // 2 - width // 2
    y = scaled_height // 2 - height // 2
    image = image.crop((x, y, x + width, y + height))
    return image



images = [rescale_image(Image.open('image%d.jpg' % i)) for i in range(8)]
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

HEALTHY_DAYS = 0
TOTAL_DAYS = 0

### Display / interaction

while True:
    clear_screen()

    x = 3
    background_image = images[HEALTHY_DAYS].copy()

    draw_background = ImageDraw.Draw(background_image)
    # draw_background.rectangle((0, 0, width, height), outline=0, fill="#FFFFFF")

    if TOTAL_DAYS == 7:
        y = top + 2
        if HEALTHY_DAYS == 7:
            CONG = 'Congrats!!'
            draw_background.text((x, y), CONG, font=font, fill=0)
        else:
            TRY_AGAIN = 'Try again next week!'
            draw_background.text((x, y), TRY_AGAIN, font=font, fill=0)

        disp.image(background_image, rotation)
        time.sleep(3)
        TOTAL_DAYS = 0
        HEALTHY_DAYS = 0
        continue

    DAY = days[TOTAL_DAYS]
    y = top + 3
    draw_background.text((x, y), DAY, font=font, fill=0)
    HINT = 'Press any button to continue.'
    hint_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 15)
    y = bottom - 1.1 * font.getsize(HINT)[1]
    draw_background.text((x, y), HINT, font=hint_font, fill="#FFFF00")

    # Display image.
    disp.image(background_image, rotation)

    button_pressed = None

    while button_pressed == None:
        if buttonA.value and not buttonB.value:
            button_pressed = "A"
        if not buttonA.value and buttonB.value:
            button_pressed = "B"
    
    time.sleep(0.5)


    ATE_HEALTHY = None

    while ATE_HEALTHY == None:
        clear_screen()

        QUESTION_1 = 'Did you'
        QUESTION_2 = 'eat healthy today?'
        x = width - font.getsize(QUESTION_2)[0]
        y = top + height / 2 - font.getsize(QUESTION_1)[1]
        draw.text((x, y), QUESTION_1, font=font, fill=0)
        y = top + height / 2
        draw.text((x, y), QUESTION_2, font=font, fill=0)

        YES = 'Yes!'
        x = 3
        y = top
        draw.text((x, y), YES, font=font, fill=0)

        NO = 'Sadly no :('
        x = 3
        y = bottom - 1.1 * font.getsize(NO)[1]
        draw.text((x, y), NO, font=font, fill=0)

        # Display image.
        disp.image(image, rotation)
        
        if buttonA.value and not buttonB.value:
            ATE_HEALTHY = False
        if not buttonA.value and buttonB.value:
            ATE_HEALTHY = True

    
    clear_screen()
    time.sleep(0.5)
    
    if ATE_HEALTHY:
        CONGRATS_1 = 'Good job!'
        CONGRATS_2 = 'Keep it up!'
        x = 3
        y = top
        draw.text((x, y), CONGRATS_1, font=font, fill=0)
        y += font.getsize(CONGRATS_1)[1]
        draw.text((x, y), CONGRATS_2, font=font, fill=0)
        HEALTHY_DAYS += 1
    else:
        TRY_1 = 'Try to eat healthier'
        TRY_2 = 'next time!'
        x = 3
        y = top
        draw.text((x, y), TRY_1, font=font, fill=0)
        y += font.getsize(TRY_1)[1]
        draw.text((x, y), TRY_2, font=font, fill=0)
    
    TOTAL_DAYS += 1


    # Display image.
    disp.image(image, rotation)
    time.sleep(1)


        

            


            

