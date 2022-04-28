#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
# Copyright 2017 ROBOTIS CO., LTD.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
################################################################################

# Author: Ryu Woon Jung (Leon)

import time
#import serial
import sys
#import platform
import board
import busio

LATENCY_TIMER = 16
DEFAULT_BAUDRATE = 1000000


class PortHandler(object):
    def __init__(self, tx_pin, rx_pin, dir_pin):
        self.is_open = False
        self.baudrate = DEFAULT_BAUDRATE
        self.packet_start_time = 0.0
        self.packet_timeout = 0.0
        self.tx_time_per_byte = 0.0

        self.is_using = False
        self.tx_pin = tx_pin
        self.rx_pin = rx_pin
        self.dir_pin = dir_pin
        self.ser = None

    def openPort(self):
        return self.setBaudRate(self.baudrate)

    def closePort(self):
        self.ser.deinit()
        self.is_open = False

    def clearPort(self):
        #self.ser.flush()
        pass

    def setPortName(self, port_name):
        self.port_name = port_name

    def getPortName(self):
        return self.port_name

    def setBaudRate(self, baudrate):
        baud = self.getCFlagBaud(baudrate)

        if baud <= 0:
            # self.setupPort(38400)
            # self.baudrate = baudrate
            return False  # TODO: setCustomBaudrate(baudrate)
        else:
            self.baudrate = baudrate
            return self.setupPort(baud)

    def getBaudRate(self):
        return self.baudrate

    def getBytesAvailable(self):
        return self.ser.in_waiting

    def readPort(self, length):
        if (sys.version_info > (3, 0)):
            rval = self.ser.read(length)
            print(rval)
            return rval
        else:
            return [ord(ch) for ch in self.ser.read(length)]

    def writePort(self, packet):
        #print("Write Port")
        #print(packet)
        bpacket = bytearray(packet)
        return self.ser.write(bpacket)

    def setPacketTimeout(self, packet_length):
        self.packet_timeout = int((self.tx_time_per_byte * packet_length) + (LATENCY_TIMER * 2.0) + 2.0)
        print("setPacketTimeout: ", self.packet_timeout )
        self.packet_start_time = time.monotonic_ns() # self.getCurrentTime()

    def setPacketTimeoutMillis(self, msec):
        self.packet_timeout = msec
        print("setPacketTimeoutMillis: ", self.packet_timeout )
        self.packet_start_time = time.monotonic_ns() #self.getCurrentTime()

    def isPacketTimeout(self):
        delta_time = int((time.monotonic_ns() - self.packet_start_time) / 1000000) #self.getTimeSinceStart()
        print("dt: ", delta_time)
        if delta_time > self.packet_timeout:
            self.packet_timeout = 0
            return True

        return False

    def getCurrentTime(self):
        return round(time.time() * 1000000000) / 1000000.0

    def getTimeSinceStart(self):
        time_since = self.getCurrentTime() - self.packet_start_time
        if time_since < 0.0:
            self.packet_start_time = self.getCurrentTime()

        return time_since

    def setupPort(self, cflag_baud):
        print("$$$Setup Port: Baud", self.baudrate)
        if self.is_open:
            self.closePort()
        self.ser = busio.UART(self.tx_pin,
            self.rx_pin,
            rs485_dir=self.dir_pin,
            baudrate=self.baudrate)

        self.is_open = True
        self.ser.timeout = 0.01

        self.ser.reset_input_buffer()

        self.tx_time_per_byte = (1000.0 / self.baudrate) * 10.0

        return True

    def getCFlagBaud(self, baudrate):
        if baudrate in [9600, 19200, 38400, 57600, 115200, 230400, 460800, 500000, 576000, 921600, 1000000, 1152000,
                        2000000, 2500000, 3000000, 3500000, 4000000]:
            return baudrate
        else:
            return -1
