import board
import time
import busio
import digitalio

from adafruit_rgb_display import ili9341, color565

# for the teensy
spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI, MISO=board.MISO)
# for ESP32S3
# spi = busio.SPI(clock=board.IO36, MOSI=board.IO35, MISO=board.IO37)

while not spi.try_lock():
    pass
spi.configure(baudrate=32000000)
spi.unlock()
print("spi.frequency: {}".format(spi.frequency))

# For the Teensy
tft_cs = digitalio.DigitalInOut(board.D10)
tft_dc = digitalio.DigitalInOut(board.D9)
# For ESP32S3
# tft_cs = digitalio.DigitalInOut(board.IO10)
# tft_dc = digitalio.DigitalInOut(board.IO9)
# tft_rst = digitalio.DigitalInOut(board.IO8)

display = ili9341.ILI9341(spi, cs=tft_cs, dc=tft_dc, width=240, height=320)

display.fill(color565(255, 0, 0))
# time.sleep(2)
display.fill(0)
display.fill_rectangle(0, 0, 120, 170, color565(0, 0, 255))
# time.sleep(10)

while True:
    pass
