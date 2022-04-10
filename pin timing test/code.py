import time
import board
import busio
import supervisor
from digitalio import DigitalInOut, Direction, Pull

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

if hasattr(board,'D0'):
    pin_name_list = ['D0','D1', 'D2','D3']
else: 
    pin_name_list = ['IO0','IO1', 'IO2','IO3']
    
pin_list = []

for pin_name in pin_name_list:
    pin_actual_name = getattr(board, pin_name)
    pin = DigitalInOut(pin_actual_name)
    pin.direction = Direction.OUTPUT
    pin.value = False;
    pin_list.append(pin)

times_high = 0
times_low = 0
loop_count = 0

while True:
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
    for i in range(10):
        start_time = time.monotonic_ns()    
        for pin in pin_list:
            pin.value = True
        high_time = time.monotonic_ns()    
        for pin in pin_list:
            pin.value = False
        low_time = time.monotonic_ns()
        dt = int(high_time - start_time)
        times_high += dt
        dt = int(low_time - high_time)
        times_low += dt
    print("High: ", times_high/10, " Low: ", times_low/10)
    loop_count = 0
    times_high = 0
    times_low = 0
    if supervisor.runtime.serial_bytes_available:
        foo
    time.sleep(0.25)
