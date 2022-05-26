import time
import board
import busio
import supervisor
from digitalio import DigitalInOut, Direction, Pull

uart1 = board.UART()
uart1.deinit()
uart1 = busio.UART(board.TX, board.RX, baudrate=115200)
uart2 = busio.UART(board.IO17, board.IO18, baudrate=115200)

#led = DigitalInOut(board.LED)
#led.direction = Direction.OUTPUT
#led_colors = None

import adafruit_dotstar as dotstar
led = dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1, brightness=0.2)
led_colors = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 0, 255),
    (0, 255, 255),
    (255, 255, 255),
    (0, 0, 0),
]
color_index = 0


while True:
    if supervisor.runtime.serial_bytes_available:
        text = input()
        text1_encoded = text.encode();
        ba = bytearray(text1_encoded)
        print("\tBA: ", ba)
        uart1.write(ba);
        text1 = uart2.read();
        uart2.write(text1)
        print("\tText1: ", text1)
        text2 = uart1.read();
        print("\ttext2: ", text2)

    led[0] = led_colors[color_index]
    color_index += 1
    if color_index >= len(led_colors):
        color_index = 0

    time.sleep(0.5)
#    if led.value:
#        led.value = False
#    else:
#        led.value = True

