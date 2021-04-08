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
import adafruit_ssd1306

i2c = busio.I2C(board.SCL, board.SDA)
mpr121 = adafruit_mpr121.MPR121(i2c)
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)


# Helper function to draw a circle from a given position with a given radius
# This is an implementation of the midpoint circle algorithm,
# see https://en.wikipedia.org/wiki/Midpoint_circle_algorithm#C_example for details
def draw_circle(xpos0, ypos0, rad, col=1):
    x = rad - 1
    y = 0
    dx = 1
    dy = 1
    err = dx - (rad << 1)
    while x >= y:
        oled.pixel(xpos0 + x, ypos0 + y, col)
        oled.pixel(xpos0 + y, ypos0 + x, col)
        oled.pixel(xpos0 - y, ypos0 + x, col)
        oled.pixel(xpos0 - x, ypos0 + y, col)
        oled.pixel(xpos0 - x, ypos0 - y, col)
        oled.pixel(xpos0 - y, ypos0 - x, col)
        oled.pixel(xpos0 + y, ypos0 - x, col)
        oled.pixel(xpos0 + x, ypos0 - y, col)
        if err <= 0:
            y += 1
            err += dy
            dy += 2
        if err > 0:
            x -= 1
            dx += 2
            err += dx - (rad << 1)


# initial center of the circle
center_x = 63
center_y = 15
# how fast does it move in each direction
x_inc = 1
y_inc = 1
# what is the starting radius of the circle
radius = 2

# start with a blank screen
oled.fill(0)
# we just blanked the framebuffer. to push the framebuffer onto the display, we call show()
oled.show()


# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = digitalio.DigitalInOut(board.D24)

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 24000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

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


red_button = qwiic_button.QwiicButton(0x6f)
green_button = qwiic_button.QwiicButton(0x60)
red_button.begin()
green_button.begin()

red_button.LED_off()
green_button.LED_off()

if not red_button.begin():
    print("Red Button is not connected.")
if not green_button.begin():
    print("Red Button is not connected.")

# musical_notation = ['7', '6#', '6', '5#', '5', '4#', '4', '3', '2#', '2', '1#', '1'] # Test

user_input = 0
while user_input==0:
    user_input = input("Enter the selection of the music: ")
    if user_input == '1':
        musical_notation = []
    elif user_input == '2':
        musical_notation = ['1', '2', '2', '3', '3', '4', '4', '5', '6', '6', '5', '5', '1', '1']
    elif user_input == '3':
        musical_notation = ['1', '2', '3', '2', '2', '3', '3', '3', '3', '2', '1', '2', '3', '5', '5', '3', '2', '2', '2', '3', '3', '3', '2', '1', '2', '3']

    else:
        user_input = '4'
        print("Error!")
        musical_notation = []
    green_button.LED_on(200)
    sleep(1)
    green_button.LED_off()
    sleep(0.5)
    green_button.LED_on(200)
    sleep(1)
    green_button.LED_off()
    sleep(0.5)
    green_button.LED_on(200)
    sleep(1)
    green_button.LED_off()

def check_playing_note(musical_notation_queue, playing_note, r):
    correct_note = musical_notation_queue.pop()    
    print("Correct: "+str(correct_note)+" Playing: "+str(playing_note))
    print(correct_note==playing_note)
    if correct_note == playing_note:
        r += 1
        green_button.LED_on(200)
        sleep(1)
        green_button.LED_off()
    else:
        red_button.LED_on(200)
        sleep(1)
        red_button.LED_off()
    return musical_notation_queue, r

sound = ''

while True:

    # undraw the previous circle
    draw_circle(center_x, center_y, radius, col=0)

    note_playing = ''
    if mpr121[0].value:
        sound = './keyboard_notes/C.mp3'
        sound_to_play = AudioPlayer(sound)
        sound_to_play.play()
        if len(musical_notation) != 0:
            note_playing = '1'
            musical_notation, radius = check_playing_note(musical_notation, note_playing, radius)
    
    elif mpr121[1].value:
        sound = './keyboard_notes/C_sharp.mp3'
        sound_to_play = AudioPlayer(sound)
        sound_to_play.play()
        if len(musical_notation) != 0:
            note_playing = '1#'
            musical_notation, radius = check_playing_note(musical_notation, note_playing, radius)

    elif mpr121[2].value:
        sound = './keyboard_notes/D.mp3'
        sound_to_play = AudioPlayer(sound)
        sound_to_play.play()
        if len(musical_notation) != 0:
            note_playing = '2'
            musical_notation, radius = check_playing_note(musical_notation, note_playing, radius)

    elif mpr121[3].value:
        sound = './keyboard_notes/D_sharp.mp3'
        sound_to_play = AudioPlayer(sound)
        sound_to_play.play()
        if len(musical_notation) != 0:
            note_playing = '2#'
            musical_notation, radius = check_playing_note(musical_notation, note_playing, radius)

    elif mpr121[4].value:
        sound = './keyboard_notes/E.mp3'
        sound_to_play = AudioPlayer(sound)
        sound_to_play.play()
        if len(musical_notation) != 0:
            note_playing = '3'
            musical_notation, radius = check_playing_note(musical_notation, note_playing, radius)

    elif mpr121[5].value:
        sound = './keyboard_notes/F.mp3'
        sound_to_play = AudioPlayer(sound)
        sound_to_play.play()
        if len(musical_notation) != 0:
            note_playing = '4'
            musical_notation, radius = check_playing_note(musical_notation, note_playing, radius)

    elif mpr121[6].value:
        sound = './keyboard_notes/F_sharp.mp3'
        sound_to_play = AudioPlayer(sound)
        sound_to_play.play()
        if len(musical_notation) != 0:
            note_playing = '4#'
            musical_notation, radius = check_playing_note(musical_notation, note_playing, radius)

    elif mpr121[7].value:
        sound = './keyboard_notes/G.mp3'
        sound_to_play = AudioPlayer(sound)
        sound_to_play.play()
        if len(musical_notation) != 0:
            note_playing = '5'
            musical_notation, radius = check_playing_note(musical_notation, note_playing, radius)

    elif mpr121[8].value:
        sound = './keyboard_notes/G_sharp.mp3'
        sound_to_play = AudioPlayer(sound)
        sound_to_play.play()
        if len(musical_notation) != 0:
            note_playing = '5#'
            musical_notation, radius = check_playing_note(musical_notation, note_playing, radius)

    elif mpr121[9].value:
        sound = './keyboard_notes/A.mp3'
        sound_to_play = AudioPlayer(sound)
        sound_to_play.play()
        if len(musical_notation) != 0:
            note_playing = '6'
            musical_notation, radius = check_playing_note(musical_notation, note_playing, radius)

    elif mpr121[10].value:
        sound = './keyboard_notes/A_sharp.mp3'
        sound_to_play = AudioPlayer(sound)
        sound_to_play.play()
        if len(musical_notation) != 0:
            note_playing = '6#'
            musical_notation, radius = check_playing_note(musical_notation, note_playing, radius)

    elif mpr121[11].value:
        sound = './keyboard_notes/B.mp3'
        sound_to_play = AudioPlayer(sound)
        sound_to_play.play()
        if len(musical_notation) != 0:
            note_playing = '7'
            musical_notation, radius = check_playing_note(musical_notation, note_playing, radius)

    # if bouncing off right
    if center_x + radius >= oled.width:
        # start moving to the left
        x_inc = -1
    # if bouncing off left
    elif center_x - radius < 0:
        # start moving to the right
        x_inc = 1

    # if bouncing off top
    if center_y + radius >= oled.height:
        # start moving down
        y_inc = -1
    # if bouncing off bottom
    elif center_y - radius < 0:
        # start moving up
        y_inc = 1

    # go more in the current direction
    center_x += x_inc
    center_y += y_inc

    # draw the new circle
    draw_circle(center_x, center_y, radius)
    # show all the changes we just made
    oled.show()

    time.sleep(0.1)  # Small delay to keep from spamming output messages.


