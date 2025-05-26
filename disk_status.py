#!/usr/bin/python3

import os
import board
import digitalio
import time
import psutil
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

WIDTH = 128
HEIGHT = 32
BORDER = 5
DISPLAY_TIMEOUT = 10.0

i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C)
dim_display_at = 0
disk_status_index = 0
btn_pins = [board.D4, board.D17]
btns = []

for btn_pin in btn_pins:
    btn = digitalio.DigitalInOut(btn_pin)
    btn.direction = digitalio.Direction.INPUT
    btn.pull = digitalio.Pull.UP
    btns.append(btn)


def reboot():
    oledPrint("Rebooting...3")
    time.sleep(1)
    oledPrint("Rebooting...2")
    time.sleep(1)
    oledPrint("Rebooting...1")
    time.sleep(1)
    oledPrint("Rebooting...")
    os.system("sudo reboot")


def btnPressed(idx):
    if idx == 0:
        showDiskStatus()
    else:
        reboot()


def showDiskStatus():
    global disk_status_index
    usage = psutil.disk_usage('/mnt/backups')
    total_tb = usage.total / (1024 ** 4)
    used_tb = usage.used / (1024 ** 4)
    free_tb = usage.free / (1024 ** 4)
    percent_used = usage.percent
    match disk_status_index:
        case 0:
            oledPrint(f"{total_tb:.2f} TB total")
        case 1:
            oledPrint(f"{used_tb:.2f} TB used")
        case 2:
            oledPrint(f"{free_tb:.2f} TB free")
        case _:
            oledPrint(f"{percent_used:.1f}% used")

    disk_status_index += 1
    if disk_status_index > 3:
        disk_status_index = 0


def oledClear():
    oled.fill(0)
    oled.show()


def oledPrint(text):
    global dim_display_at
    oledClear()
    image = Image.new("1", (oled.width, oled.height))
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    bbox = font.getbbox(text)
    (font_width, font_height) = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(
        (oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2),
        text,
        font=font,
        fill=255,
    )
    oled.image(image)
    oled.show()
    dim_display_at = time.monotonic() + DISPLAY_TIMEOUT


while True:
    now = time.monotonic()
    if now >= dim_display_at:
        oledClear()
    for i in range(2):
        if not btns[i].value:
            btnPressed(i)
            time.sleep(0.2)  # debounce
        time.sleep(0.01)
