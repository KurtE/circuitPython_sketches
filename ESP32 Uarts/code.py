import time
import board
import busio
import supervisor
from digitalio import DigitalInOut, Direction, Pull

import neopixel

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
check_pin = DigitalInOut(board.IO4)
check_pin.direction = Direction.INPUT
check_pin.pull = Pull.DOWN
uart1 = None
uart2 = None

led = neopixel.NeoPixel(board.NEOPIXEL, 1)

led.brightness = 0.3

last_check_value = check_pin.value

def CheckAndEchoUart(index, uart):
    waiting_count = uart.in_waiting
    if waiting_count:
        print("*** Uart", index, " input(", waiting_count, ") ***")
        data = uart.read(waiting_count)

        if (index == 1):
            print("\t len:",len(data), "data:", data.decode())
        else:
            uart2.write(data)

while True:
    if check_pin.value:
        if uart1 == None:
            print("*** initialize the uarts ***")
            # we have not yet tried to iniatialize the uarts
            uart1 = board.UART()
            uart1.deinit()
            uart1 = busio.UART(board.TX, board.RX, baudrate=1000000)
            uart2 = busio.UART(board.IO17, board.IO18, baudrate=1000000)

        if supervisor.runtime.serial_bytes_available:
            text = input()
            print("*** Serial input ***", text)
            b = bytearray()
            b.extend(text)
            uart1.write(b)

        CheckAndEchoUart(1, uart1)
        CheckAndEchoUart(2, uart2)
    # cycle colors
    led[0] = led_colors[color_index]
    color_index += 1
    if color_index >= len(led_colors):
        color_index = 0
    time.sleep(0.5)
