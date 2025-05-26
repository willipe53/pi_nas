#!/usr/bin/python3

# NOTE THIS IS JUST A SCRATCH PAD.
# FILE NOT USED.

import board
import digitalio
import time
import psutil
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

WIDTH = 128
HEIGHT = 32
BORDER = 5

i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C)

# Clear display, set to 1 bit color.
oled.fill(0)
oled.show()
image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)

# Draw a white background
draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)

# Draw a smaller inner rectangle
draw.rectangle(
    (BORDER, BORDER, oled.width - BORDER - 1, oled.height - BORDER - 1),
    outline=0,
    fill=0,
)

# Load default font.
font = ImageFont.load_default()

# Draw Some Text
text = "Hello World!"
bbox = font.getbbox(text)
(font_width, font_height) = bbox[2] - bbox[0], bbox[3] - bbox[1]
draw.text(
    (oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2),
    text,
    font=font,
    fill=255,
)

# Display image
oled.image(image)
oled.show()

btn_right = digitalio.DigitalInOut(board.D17)
btn_right.direction = digitalio.Direction.INPUT
btn_right.pull = digitalio.Pull.UP  # Internal pull-up
btn_left = digitalio.DigitalInOut(board.D4)  # GPIO4
btn_left.direction = digitalio.Direction.INPUT
btn_left.pull = digitalio.Pull.UP  # Internal pull-up
prev = psutil.disk_io_counters(perdisk=True)["sda"]
last_print = 0

while True:
    now = time.monotonic()
    if not btn_right.value:  # Active low (pressed = GND)
        print("btn_right was pressed")
        time.sleep(0.2)  # debounce
    time.sleep(0.01)
    if not btn_left.value:  # Active low (pressed = GND)
        print("btn_left was pressed")
        time.sleep(0.2)  # debounce
    time.sleep(0.01)
    if now - last_print >= 5.0:
        curr = psutil.disk_io_counters(perdisk=True)["sda"]
        read_bytes = curr.read_bytes - prev.read_bytes
        write_bytes = curr.write_bytes - prev.write_bytes
        if read_bytes or write_bytes:
            print(f"sda R={read_bytes} B/s, W={write_bytes} B/s")
            # you could update your I2C display here
    prev = curr
