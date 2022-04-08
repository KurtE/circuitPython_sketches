import time
import board
import busio
import supervisor
from digitalio import DigitalInOut, Direction, Pull

led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT

check_pin = DigitalInOut(board.D2)
check_pin.direction = Direction.INPUT
check_pin.pull = Pull.DOWN
uart1 = None

last_check_value = check_pin.value

def CheckAndEchoUart(index, uart):
    waiting_count = uart.in_waiting
    if waiting_count:
        print("*** Uart", index, " input(", waiting_count, ") ***")
        data = uart.read(waiting_count)

        if (index == 1):
            print("Echoed back len:",len(data), "data:", data.decode())
        else:
            print(index,">>", data.decode())
            uart.write(data)

while True:
    if check_pin.value:
        if uart1 == None:
            # we have not yet tried to iniatialize the uarts
            print("Initialize Uarts")
            uart1 = busio.UART(board.TX, board.RX, baudrate=500000)
            uart2 = busio.UART(board.D8, board.D7, baudrate=500000)
            uart3 = busio.UART(board.D14, board.D15, baudrate=500000)
            uart4 = busio.UART(board.D17, board.D16, baudrate=500000)
            uart5 = busio.UART(board.D20, board.D21, baudrate=500000)
            uart6 = busio.UART(board.D24, board.D25, baudrate=500000)
            uart7 = busio.UART(board.D29, board.D28, baudrate=500000)
            uart8 = busio.UART(board.D35, board.D34, baudrate=500000)

        if supervisor.runtime.serial_bytes_available:
            text = input()
            print("*** Serial input ***", text)
            b = bytearray()
            b.extend(text)
            uart1.write(b)

        CheckAndEchoUart(1, uart1)
        CheckAndEchoUart(2, uart2)
        CheckAndEchoUart(3, uart3)
        CheckAndEchoUart(4, uart4)
        CheckAndEchoUart(5, uart5)
        CheckAndEchoUart(6, uart6)
        CheckAndEchoUart(7, uart7)
        CheckAndEchoUart(8, uart8)
    # cycle colors
    if led.value:
        led.value = False
    else:
        led.value = True
    time.sleep(0.5)