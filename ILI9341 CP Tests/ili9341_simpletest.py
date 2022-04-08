# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This test will initialize the display using displayio and draw a solid green
background, a smaller purple rectangle, and some yellow text. All drawing is done
using native displayio modules.

Pinouts are for the 2.4" TFT FeatherWing or Breakout with a Feather M4 or M0.
"""
import board
import terminalio
import busio
import displayio
from adafruit_display_text import label
import adafruit_ili9341

# Release any resources currently in use for the displays
displayio.release_displays()

# For Mimxrt10xx boards
spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI, MISO=board.MISO)
# For ESP32S3
# spi = busio.SPI(clock=board.IO36, MOSI=board.IO35, MISO=board.IO37)

while not spi.try_lock():
    pass
spi.configure(baudrate=32000000)
spi.unlock()
print("SPI Clock changed to: ", spi.frequency)

# For the MIMXRT10xx
#tft_cs = digitalio.DigitalInOut(board.D10)
#tft_dc = digitalio.DigitalInOut(board.D9)
#tft_rst = digitalio.DigitalInOut(board.D8)
# For ESP32S3
# tft_cs = digitalio.DigitalInOut(board.IO10)
# tft_dc = digitalio.DigitalInOut(board.IO9)
# tft_rst = digitalio.DigitalInOut(board.IO8)

display_bus = displayio.FourWire(
    spi, command=board.D9, chip_select=board.D10
)
display = adafruit_ili9341.ILI9341(display_bus, width=320, height=240)

# Make the display context
splash = displayio.Group()
display.show(splash)

# Draw a green background
color_bitmap = displayio.Bitmap(320, 240, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0x00FF00  # Bright Green

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)

splash.append(bg_sprite)

# Draw a smaller inner rectangle
inner_bitmap = displayio.Bitmap(280, 200, 1)
inner_palette = displayio.Palette(1)
inner_palette[0] = 0xAA0088  # Purple
inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=20, y=20)
splash.append(inner_sprite)

# Draw a label
text_group = displayio.Group(scale=3, x=57, y=120)
text = "Hello World!"
text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00)
text_group.append(text_area)  # Subgroup for text scaling
splash.append(text_group)

while True:
    pass
