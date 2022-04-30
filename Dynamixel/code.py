
import os
import sys
import board
import busio
from digitalio import DigitalInOut, Direction, Pull
import time
from dynamixel_sdk import *                 # Uses Dynamixel SDK library

# Protocol version
PROTOCOL_VERSION        = 1.0               # See which protocol version is used in the Dynamixel

# Default setting
DXL_ID                  = [19, 3, 5, 2, 4, 6, 7, 9, 11, 8, 10, 12, 13, 15, 17, 14, 16, 18]                 # Dynamixel ID : 1
BAUDRATE                = 1000000             # Dynamixel default baudrate : 57600
#DEVICENAME              = '/dev/ttyUSB0'    # Check which port is being used on your controller
                                            # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"
if (sys.platform == "RP2040"):
    dir_pin = board.D25
    enable_pin = board.D6
    test_pin = board.D9
    debug_pin = None
else:
    dir_pin = board.D2
    enable_pin = board.D3
    test_pin = board.D4
    debug_pin = board.D5

timetest = DigitalInOut(test_pin)
timetest.direction = Direction.OUTPUT
timetest.value = 0
for dtime in [0.005, 0.010, 0.025, 0.050, 0.1, 0.5]:
    ms = time.monotonic()
    msns = time.monotonic_ns()
    timetest.value = 1
    time.sleep(dtime)
    timetest.value = 0
    me = time.monotonic()
    mens = time.monotonic_ns()
    print("SL: ", dtime, " MT: ", ms," ", me, " ", me-ms,
        " MTNS: ", msns, " ", mens, " ", mens-msns, " ", int((mens-msns)/1000000))
#quit()
timetest.deinit()


dxl_enable = DigitalInOut(enable_pin)
dxl_enable.direction = Direction.OUTPUT
dxl_enable.value = 1

if debug_pin != None:
    uart_debug_pin = DigitalInOut(debug_pin)
    uart_debug_pin.direction = Direction.OUTPUT
    uart_debug_pin.value = 1

# Initialize PortHandler instance
# Set the port path
# Get methods and members of PortHandlerLinux or PortHandlerWindows
portHandler = PortHandler(board.TX, board.RX, dir_pin)

# Initialize PacketHandler instance
# Set the protocol version
# Get methods and members of Protocol1PacketHandler or Protocol2PacketHandler
packetHandler = PacketHandler(PROTOCOL_VERSION)

# Open port
if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    print("Press any key to terminate...")
    getch()
    quit()


# Set port baudrate
if portHandler.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    print("Press any key to terminate...")
    getch()
    quit()

# lets play with setting the return delay
if True:
    return_delay = [100]
    for id in DXL_ID:
        # try to set the return delay...
        print("Set return delay: ", id)
        dxl_comm_result, dxl_error = packetHandler.writeTxRx(portHandler, id, 5, 1, return_delay)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))




# Try to ping the Dynamixel
# Get Dynamixel model number
for id in DXL_ID:
    print("Ping: ", id)
    dxl_model_number, dxl_comm_result, dxl_error = packetHandler.ping(portHandler, id)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    else:
        print("[ID:%03d] ping Succeeded. Dynamixel model number : %d" % (id, dxl_model_number))

# Close port
portHandler.closePort()
