import board
import time
import busio
import digitalio
import displayio
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.circle import Circle
from adafruit_display_shapes.roundrect import RoundRect
from adafruit_display_shapes.triangle import Triangle
from adafruit_display_shapes.line import Line

import board
import terminalio
import busio
import displayio
import adafruit_ili9341

def color565(r, g=0, b=0):
    try:
        r, g, b = r  # see if the first var is a tuple/list
    except TypeError:
        pass
    return (r & 0xF8) << 8 | (g & 0xFC) << 3 | b >> 3

if "DISPLAY" not in dir(board):
    # Setup the LCD display with driver
    # You may need to change this to match the display driver for the chipset
    # used on your display
    from adafruit_ili9341 import ILI9341

    displayio.release_displays()

    # setup the SPI bus
    spi = board.SPI()
    tft_cs = board.D10  # arbitrary, pin not used
    tft_dc = board.D9
    tft_backlight = board.D12
    tft_reset = board.D8

    while not spi.try_lock():
        spi.configure(baudrate=32000000)

    spi.unlock()

    display_bus = displayio.FourWire(
        spi,
        command=tft_dc,
        chip_select=tft_cs,
        reset=tft_reset,
        baudrate=32000000,
        polarity=1,
        phase=1,
    )

    print("spi.frequency: {}".format(spi.frequency))

    # Number of pixels in the display
    DISPLAY_WIDTH = 320
    DISPLAY_HEIGHT = 240

    # create the display
    display = ILI9341(
        display_bus,
        width=DISPLAY_WIDTH,
        height=DISPLAY_HEIGHT,
        rotation=180,  # The rotation can be adjusted to match your configuration.
        auto_refresh=True,
        native_frames_per_second=90,
    )

    # reset the display to show nothing.
    display.show(None)
else:
    # built-in display
    display = board.DISPLAY
# Make the display context
splash = displayio.Group()
display.show(splash)

# Now loop forever drawing different primitives.
while True:
    # Clear screen and draw a red line.
    # display.show(None)
    splash.append(Line(0, 0, 239, 319, color565(255, 0, 0)))
    time.sleep(0.5)
    # Clear screen and draw a green rectangle.
    # display.fill(0)
    rect = Rect(0, 0, 120, 160, outline=color565(0, 255, 0))
    splash.append(rect)
    time.sleep(0.5)
    # Clear screen and draw a filled green rectangle.
    frect = Rect(0, 0, 120, 160, fill=color565(0, 255, 0))
    time.sleep(0.5)
    splash.append(frect)
    # Clear screen and draw a blue circle.
    # display.fill(0)
    circle = Circle(120, 160, 60, outline=color565(0, 0, 255))
    splash.append(circle)
    time.sleep(0.5)
    # Clear screen and draw a filled blue circle.
    # display.fill(0)
    f_circ = Circle(120, 160, 60, fill=color565(0, 0, 255))
    splash.append(f_circ)
    time.sleep(0.5)
    # Clear screen and draw a pink triangle.
    # display.fill(0)
    tri = Triangle(120, 100, 180, 160, 60, 160, outline = color565(255, 0, 255))
    splash.append(tri)
    time.sleep(0.5)
    # Clear screen and draw a filled pink triangle.
    # display.fill(0)
    fill_tri = Triangle(120, 100, 180, 160, 60, 160, fill=color565(255, 255, 0))
    splash.append(fill_tri)
    time.sleep(0.5)
    # Rounded Rect
    roundrect = RoundRect(10, 10, 61, 81, 10, fill=0x0, outline=0xFF00FF, stroke=6)
    splash.append(roundrect)

