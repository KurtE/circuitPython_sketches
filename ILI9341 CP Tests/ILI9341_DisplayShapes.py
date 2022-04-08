import board
import time
import busio
import digitalio
from adafruit_rgb_display import ili9341, color565

import displayio
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.circle import Circle
from adafruit_display_shapes.roundrect import RoundRect
from adafruit_display_shapes.triangle import Triangle
from adafruit_display_shapes.line import Line

# For the MIMXRT10xx
tft_cs = digitalio.DigitalInOut(board.D10)
tft_dc = digitalio.DigitalInOut(board.D9)
tft_rst = digitalio.DigitalInOut(board.D8)
# For ESP32S3
# tft_cs = digitalio.DigitalInOut(board.IO10)
# tft_dc = digitalio.DigitalInOut(board.IO9)
# tft_rst = digitalio.DigitalInOut(board.IO8)

# For Mimxrt10xx boards
spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI, MISO=board.MISO)
# For ESP32S3
# spi = busio.SPI(clock=board.IO36, MOSI=board.IO35, MISO=board.IO37)

while not spi.try_lock():
    pass
spi.configure(baudrate=32000000)
spi.unlock()
print("SPI Clock changed to: ", spi.frequency)

display = ili9341.ILI9341(spi, cs=tft_cs, dc=tft_dc, width=240, height=320)

display.fill(color565(255, 0, 0))
display.fill(0)
display.fill_rectangle(0, 0, 120, 170, color565(0, 0, 255))

# Make the display context
splash = displayio.Group()
board.DISPLAY.show(splash)

# Now loop forever drawing different primitives.
while True:
    # Clear screen and draw a red line.
    display.fill(0)
    splash.append(Line(0, 0, 239, 319, color565(255, 0, 0)))
    time.sleep(2)
    # Clear screen and draw a green rectangle.
    display.fill(0)
    rect = Rect(0, 0, 120, 160, outline=color565(0, 255, 0))
    splash.append(rect)
    time.sleep(2)
    # Clear screen and draw a filled green rectangle.
    display.fill(0)
    display.fill_rectangle(0, 0, 120, 160, color565(0, 255, 0))
    time.sleep(2)
    # Clear screen and draw a blue circle.
    display.fill(0)
    circle = Circle(120, 160, 60, outline=color565(0, 0, 255))
    splash.append(circle)
    time.sleep(2)
    # Clear screen and draw a filled blue circle.
    display.fill(0)
    f_circ = Circle(120, 160, 60, fill=color565(0, 0, 255))
    splash.append(f_circ)
    time.sleep(2)
    # Clear screen and draw a pink triangle.
    # display.fill(0)
    # tri = Triangle(120, 100, 180, 160, 60, 160, outline = color565(255, 0, 255))
    # splash.append(tri)
    # time.sleep(2)
    # Clear screen and draw a filled pink triangle.
    display.fill(0)
    fill_tri = Triangle(120, 100, 180, 160, 60, 160, fill=color565(255, 0, 255))
    splash.append(fill_tri)
    time.sleep(2)
    # Rounded Rect
    roundrect = RoundRect(10, 10, 61, 81, 10, fill=0x0, outline=0xFF00FF, stroke=6)
    splash.append(roundrect)
    
