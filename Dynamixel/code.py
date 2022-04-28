
import os
import sys
import board
import busio
from digitalio import DigitalInOut, Direction, Pull
from dynamixel_sdk import *                 # Uses Dynamixel SDK library

# Protocol version
PROTOCOL_VERSION        = 1.0               # See which protocol version is used in the Dynamixel

# Default setting
DXL_ID                  = [17, 3, 5, 2, 4, 6, 7, 9, 11, 8, 10, 12]                 # Dynamixel ID : 1
BAUDRATE                = 1000000             # Dynamixel default baudrate : 57600
#DEVICENAME              = '/dev/ttyUSB0'    # Check which port is being used on your controller
                                            # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"

dxl_enable = DigitalInOut(board.D3)
dxl_enable.direction = Direction.OUTPUT
dxl_enable.value = 1

# Initialize PortHandler instance
# Set the port path
# Get methods and members of PortHandlerLinux or PortHandlerWindows
portHandler = PortHandler(board.TX1, board.RX1, board.D2)

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
