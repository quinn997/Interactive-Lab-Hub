import time
import busio
import digitalio
import board
import time
from time import strftime, sleep
import subprocess
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display.rgb import color565
import adafruit_rgb_display.st7789 as st7789
import adafruit_mpr121
from audioplayer import AudioPlayer

import qwiic_button

green_button = qwiic_button.QwiicButton(0x60)


green_button.begin()


green_button.LED_off()