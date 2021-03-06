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
uarts = None

last_check_value = check_pin.value

def CheckAndEchoUart(index, uart):
    waiting_count = uart.in_waiting
    if waiting_count:
        print("*** Uart", index, " input(", waiting_count, ") ***")
        data = uart.read(waiting_count)

        if (index == 0):
            print("Echoed back len:",len(data), "data:", data.decode())
        else:
            print(index,">>", data.decode())
            uart.write(data)

while True:
    if check_pin.value:
        if uarts == None:
            print("Initialize Uarts")
            uarts = []
            for index in range(9):
                tx_name = "TX"+str(index)
                rx_name = "RX"+str(index)
                if hasattr(board, tx_name):
                    tx_pin = getattr(board, tx_name)
                    rx_pin = getattr(board, rx_name)
                    uart = busio.UART(tx_pin, rx_pin, baudrate=5000000)
                    uarts.append(uart)
                    print("\tAdded: ",index, " TX:",tx_pin, " RX:", rx_pin)

            # we have not yet tried to iniatialize the uarts
        if supervisor.runtime.serial_bytes_available:
            text = input()
            print("*** Serial input ***", text)
            b = bytearray()
            b.extend(text)
            #uart1.write(b)
            uarts[0].write(b)

        for index in range(len(uarts)):
            CheckAndEchoUart(index, uarts[index])
    # cycle colors
    if led.value:
        led.value = False
    else:
        led.value = True
    time.sleep(0.5)
