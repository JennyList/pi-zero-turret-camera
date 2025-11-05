#!/usr/bin/env python3

#
# World's worst Raspberry Pi camera script
# Jenny List, January 2023
#
# For a Pi Zero with a camera module and a Pimoroni Display HAT Mini.
#
# It's horribly inefficient, there's no pretence of optimisation, you could certainly do better than this.
#

from picamera2 import Picamera2, Preview
import time
from displayhatmini import DisplayHATMini
from libcamera import controls
from PIL import Image
import os
from os.path import exists
import ST7789 as ST7789

# set up parameters for display library
disp = ST7789.ST7789(
    height=240,
    width=320,
    rotation=180,
    port=0,
    cs=1,
    dc=9,
    backlight=13,
    spi_speed_hz=60 * 1000 * 1000,
    offset_left=0,
    offset_top=0
)
disp.begin()

# Set up display hat
width = DisplayHATMini.WIDTH
height = DisplayHATMini.HEIGHT
buffer = Image.new("RGB", (width, height))
displayhatmini = DisplayHATMini(buffer)

# Find most recent file name
i = 0
while exists("./Pictures/test" + str(i) + ".jpg"):
    i += 1

# Set up camera
picam2 = Picamera2()
preview_config = picam2.create_preview_configuration()
capture_config = picam2.create_still_configuration()
picam2.configure(preview_config)
picam2.start()
# Following line for cameras with autofocus only.
# picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous})

# Main loop
while True:
    image = picam2.capture_image("main") # Display viewfinder image
    image = image.resize((width, height))
    disp.display(image)
    if displayhatmini.read_button(displayhatmini.BUTTON_X): # Detect shutter press
        picam2.switch_mode(capture_config)
        picam2.capture_file("./Pictures/test" + str(i) + ".jpg") # Capture in hi res mode
        picam2.switch_mode(preview_config)
        displayhatmini.set_led(0.1, 0.1, 0.1) # Flash the LED white
        time.sleep (0.02)
        displayhatmini.set_led(0, 0, 0)
        i += 1
    if displayhatmini.read_button(displayhatmini.BUTTON_A): # Detect leave script button
        displayhatmini.set_led(0, 0.1, 0) # Flash the LED green
        time.sleep (0.02)
        displayhatmini.set_led(0, 0, 0)
        break
    if displayhatmini.read_button(displayhatmini.BUTTON_B): # Detect shutdown button
        displayhatmini.set_led(0.1, 0, 0) # Flash the LED red
        time.sleep (0.02)
        os.system ('sudo shutdown -h now')
        displayhatmini.set_led(0, 0, 0)
