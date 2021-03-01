import digitalio
import board
import time
from time import strftime, sleep
import subprocess
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display.rgb import color565
import adafruit_rgb_display.st7789 as st7789
import webcolors
from datetime import datetime, timedelta

# The display uses a communication protocol called SPI.
# SPI will not be covered in depth in this course. 
# you can read more https://www.circuitbasics.com/basics-of-the-spi-communication-protocol/

# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000  # the rate  the screen talks to the pi

# Create the ST7789 display:
display = st7789.ST7789(
    board.SPI(),
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)


# these setup the code for our buttons and the backlight and tell the pi to treat the GPIO pins as digitalIO vs analogIO
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = display.width  # we swap height/width to rotate it to landscape!
width = display.height
image = Image.new("RGB", (width, height))
rotation = 90

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
display.image(image, rotation)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
font1 = ImageFont.truetype("/home/pi/Interactive-Lab-Hub/Lab 2/babyblocks/baby blocks.ttf", 25)
font2 = ImageFont.truetype("/home/pi/Interactive-Lab-Hub/Lab 2/advanced_pixel_lcd_7/advanced_pixel_lcd-7.ttf", 25)


# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True


# Main loop:
while True:

    now = datetime.now()

    clockdate = strftime("Date: %m/%d/%Y")
    clocktime = strftime("Time: %H:%M:%S")
    digital = strftime("%A \n\n%H:%M:%S")

    t = timedelta(hours = now.hour, minutes = now.minute , seconds = now.second)
    totalsec = t.total_seconds()
    percent = "{:.2%}".format(totalsec/86400)+"percent\nof the day has passed"

    if buttonA.value and buttonB.value:
        # Draw a black filled box to clear the image.
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
        y = top+50
        draw.text((x+45, y), clockdate, font=font, fill="#FF00FF") 
        y += font.getsize(clockdate)[1]
        draw.text((x+45, y), clocktime, font=font, fill="#FFFF00") 
        display.image(image, rotation)
        time.sleep(0.7)
    elif buttonB.value and not buttonA.value:
        y=top+40
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
        draw.text((x+15, y), percent, font=font1, fill="#FFFFFF")
        display.image(image, rotation)
        time.sleep(0.7)
    elif buttonA.value and not buttonB.value:
        y = top+40
        draw.rectangle((0, 0, width, height), outline=0, fill="#535AC2")
        draw.text((x+2, y), digital, font=font2,fill="#FFFFFF")
        display.image(image, rotation)
        time.sleep(0.7)
        
        


