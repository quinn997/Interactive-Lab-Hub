import digitalio
import board
import time
from time import strftime, sleep
import subprocess
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display.rgb import color565
import adafruit_rgb_display.st7789 as st7789
import webcolors
import qwiic_joystick
from vosk import Model, KaldiRecognizer


myJoystick = qwiic_joystick.QwiicJoystick()

if myJoystick.is_connected() == False:
    print("The Qwiic Joystick device isn't connected to the system. Please check your connection", \
        file=sys.stderr)

myJoystick.begin()


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

dict = {
  0: "~/Interactive-Lab-Hub/Lab\ 3/muffin_recipe/hello.sh",
  1: "~/Interactive-Lab-Hub/Lab\ 3/muffin_recipe/step1.sh",
  2: "~/Interactive-Lab-Hub/Lab\ 3/muffin_recipe/step2.sh",
  3: "~/Interactive-Lab-Hub/Lab\ 3/muffin_recipe/step3.sh",
  4: "~/Interactive-Lab-Hub/Lab\ 3/muffin_recipe/step4.sh",
  5: "~/Interactive-Lab-Hub/Lab\ 3/muffin_recipe/step5.sh",
  6: "~/Interactive-Lab-Hub/Lab\ 3/muffin_recipe/step6.sh",
  7: "~/Interactive-Lab-Hub/Lab\ 3/muffin_recipe/step7.sh",
  8: "~/Interactive-Lab-Hub/Lab\ 3/muffin_recipe/step8.sh",
  9: "~/Interactive-Lab-Hub/Lab\ 3/muffin_recipe/end.sh",
}


# Main loop:

muffin = image
muffin = Image.open("/home/pi/Interactive-Lab-Hub/Lab 3/muffin.jpeg")
muffin = scaleAndCrop(muffin)
draw = ImageDraw.Draw(muffin)
display.image(muffin, rotation)

subprocess.call(dict[0], shell=True)

i=0
speak = False
while True:
    if myJoystick.get_horizontal() == 1023:
        i+=1
        speak = True
    elif myJoystick.get_horizontal() == 0:
        if i != 0:
            i-=1
            speak = True
        else:
            i+=0
            speak = False
    elif myJoystick.get_button() == 0:
        i+=0
        speak = True
    while speak:
        subprocess.call(dict[i], shell=True)
        speak = False


 
    
    
    



        


