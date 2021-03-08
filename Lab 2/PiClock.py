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
reset_pin = digitalio.DigitalInOut(board.D24)

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 24000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# pylint: disable=line-too-long
# Create the display:
# disp = st7789.ST7789(spi, rotation=90,                            # 2.0" ST7789
# disp = st7789.ST7789(spi, height=240, y_offset=80, rotation=180,  # 1.3", 1.54" ST7789
# disp = st7789.ST7789(spi, rotation=90, width=135, height=240, x_offset=53, y_offset=40, # 1.14" ST7789
# disp = hx8357.HX8357(spi, rotation=180,                           # 3.5" HX8357
# disp = st7735.ST7735R(spi, rotation=90,                           # 1.8" ST7735R
# disp = st7735.ST7735R(spi, rotation=270, height=128, x_offset=2, y_offset=3,   # 1.44" ST7735R
# disp = st7735.ST7735R(spi, rotation=90, bgr=True,                 # 0.96" MiniTFT ST7735R
# disp = ssd1351.SSD1351(spi, rotation=180,                         # 1.5" SSD1351
# disp = ssd1351.SSD1351(spi, height=96, y_offset=32, rotation=180, # 1.27" SSD1351
# disp = ssd1331.SSD1331(spi, rotation=180,                         # 0.96" SSD1331

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

height = display.width
width = display.height

rotation = 90

image = Image.new("RGB", (width, height))

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


# Scale the image to the smaller screen dimension
def scaleAndCrop(image):
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

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
font1 = ImageFont.truetype("/home/pi/Interactive-Lab-Hub/Lab 2/babyblocks/baby blocks.ttf", 25)
font2 = ImageFont.truetype("/home/pi/Interactive-Lab-Hub/Lab 2/advanced_pixel_lcd_7/advanced_pixel_lcd-7.ttf", 20)


# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True


# Main loop:
while True:

    today = datetime.today()
    now = datetime.now()

    digital = strftime("%b%d %Y\n\n%H:%M:%S\n\n%A")
    birthday = datetime(now.year, 12, 18)
    diff = str((birthday-today).days)
    name1 = "Time Percent Calculator"
    name2 = "Birthday Countdown"
    andSymbol = "&"

    t = timedelta(hours = now.hour, minutes = now.minute , seconds = now.second)
    totalsec = t.total_seconds()
    weekday = datetime.weekday(now)
    daypercent = "{:.2%}".format(totalsec/86400)+"percent\nof the day has passed"
    weekpercent = "{:.2%}".format((weekday*86400+totalsec)/604800)+"percent\nof the week has passed"
    diff = str((birthday-today).days) + " days until \n my birthday!!!"

    if buttonA.value and buttonB.value:
        # Draw a black filled box to clear the image.
        home = image
        home = Image.open("/home/pi/Interactive-Lab-Hub/Lab 2/Lab_2_Images/home_background.jpg")
        home = scaleAndCrop(home)
        draw = ImageDraw.Draw(home)
        y = top+40
        draw.text((x+10, y), name1, font=font, fill="#FF00FF") 
        y += font.getsize(name1)[1]
        draw.text((x+115, y), andSymbol, font=font, fill=0) 
        y += font.getsize(andSymbol)[1]
        draw.text((x+30, y), name2, font=font, fill="#003C7B") 
        display.image(home, rotation)
        time.sleep(0.7)
    elif buttonB.value and not buttonA.value:
        b_background = image
        b_background = Image.open("/home/pi/Interactive-Lab-Hub/Lab 2/Lab_2_Images/black_background.jpg")
        b_background = scaleAndCrop(b_background)
        draw = ImageDraw.Draw(b_background)
        y=top+10
        draw.text((x+15, y), daypercent, font=font1, fill="#FC6F03")
        y += font1.getsize(daypercent)[1]
        draw.text((x+15, y+40), weekpercent, font=font1, fill="#0F03FC") 
        display.image(b_background, rotation)
        time.sleep(0.7)
    elif buttonA.value and not buttonB.value:
        c_background = image
        c_background = Image.open("/home/pi/Interactive-Lab-Hub/Lab 2/Lab_2_Images/color_background.jpg")
        c_background = scaleAndCrop(c_background)
        draw = ImageDraw.Draw(c_background)
        y = top+35
        draw.text((x+2, y), digital, font=font2,fill="#FFFFFF")
        display.image(c_background, rotation)
        time.sleep(0.7)
    else:
        birthday_background = image
        birthday_background = Image.open("/home/pi/Interactive-Lab-Hub/Lab 2/Lab_2_Images/birthday_background.jpg")
        birthday_background = scaleAndCrop(birthday_background)
        draw = ImageDraw.Draw(birthday_background)
        y=top+40
        draw.text((x+18, y), diff, font=font1, fill="#FF748C")
        display.image(birthday_background, rotation)
        time.sleep(0.7)

        


