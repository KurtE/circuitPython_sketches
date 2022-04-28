import time
import board
import busio
import supervisor
from digitalio import DigitalInOut, Direction, Pull

initial_baud = 115200

if hasattr(board, 'NEOPIXEL'): 
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
    led = neopixel.NeoPixel(board.NEOPIXEL, 1)
    led.brightness = 0.3

else:
    led = DigitalInOut(board.LED)
    led.direction = Direction.OUTPUT
    led_colors = None

if hasattr(board, 'TX2'): 
    dir1_pin = board.D2
    dir2_pin = board.D3
    tx2 = board.TX2
    rx2 = board.RX2
else:
    #ESP32-S3
    dir1_pin = board.IO1
    dir2_pin = board.IO16
    tx2 = board.IO17
    rx2 = board.IO18

uart1 = board.UART()
uart2 = None

#def setup_uarts(baud):
if True:
    baud = initial_baud
    print("*** initialize the uarts baud: ", baud, " ***")
    # we have not yet tried to iniatialize the uarts
    if (uart1 != None):
        uart1.deinit()
    uart1 = busio.UART(board.TX, board.RX, rs485_dir=dir1_pin, baudrate=baud)
    print("After Uart1")

    # on second one roll our own direction pin
    if (uart2 != None):
        uart2.deinit()
    uart2 = busio.UART(tx2, rx2, baudrate=baud)
    print("After Uart2")

#setup_uarts(initial_baud)

uart2_dir = DigitalInOut(dir2_pin)
uart2_dir.direction = Direction.OUTPUT
uart2_dir.value = 0
times_1 = 0
times_2 = 0
loop_count = 0
print("Start loop")

while True:
    start_time = time.monotonic_ns()
    uart1.write(b"abcdefghijklmnopqrstuvwxyz")
    after1 = time.monotonic_ns()
    times_1 += int(after1 - start_time)
    uart2_dir.value = 1
    uart2.write(b"abcdefghijklmnopqrstuvwxyz")
    uart2_dir.value = 0
    after2 = time.monotonic_ns()
    times_2 += int(after2 - after1)
    loop_count += 1
    if (loop_count == 10):
        print(int(times_1/10), " ", int(times_2/10))
        times_1 = 0
        times_2 = 0
        loop_count = 0
        if led_colors != None:
            led[0] = led_colors[color_index]
            color_index += 1
            if color_index >= len(led_colors):
                color_index = 0
        else:
            if led.value:
                led.value = False
            else:    
                led.value = True
    time.sleep(0.025)
