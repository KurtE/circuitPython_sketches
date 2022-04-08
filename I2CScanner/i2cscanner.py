# SPDX-FileCopyrightText: 2017 Limor Fried for Adafruit Industries
# SPDX-FileCopyrightText: 2017 Limor Fried for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""CircuitPython I2C Device Address Scan"""
# If you run this and it seems to hang, try manually unlocking
# your I2C bus from the REPL with
#  >>> import board
#  >>> board.I2C().unlock()

import time
import board
import busio

# To use default I2C bus (most boards)
i2c = busio.I2C(board.SCL, board.SDA)
i2c1 = busio.I2C(board.SCL1, board.SDA1)
#i2c2 = busio.I2C(board.SCL2, board.SDA2)
# To use default I2C bus (most boards) scl/sda use for ESP32s3
#i2c = busio.I2C(board.IO10, board.IO11)
#i2c1 = busio.I2C(board.IO1, board.IO2)
# use bitbangio for BNO080 to be recognized
#i2c1 = bitbangio.I2C(board.I2C_SCL1, board.I2C_SDA1, timeout = 500)
#i2c1 = busio.I2C(board.I2C_SCL1, board.I2C_SDA1)


def i2cportscan():
    print("Wire")
    # Lock the I2C device before we try to scan
    while not i2c.try_lock():
        pass
    # Print the addresses found once
    # print(
    #    "I2C addresses found:", [hex(device_address) for device_address in i2c.scan()]
    # )
    for device_address in i2c.scan():
        print("Device found at address", end=" ")
        print(hex(device_address), end=" (")
        printKnownChips(hex(device_address))
        print(end=")")
        print()
    # Unlock I2C now that we're done scanning.
    i2c.unlock()

def i2cport1scan():
    print("Wire1")
    # Lock the I2C device before we try to scan
    while not i2c1.try_lock():
        pass
    # Print the addresses found once
    for device_address in i2c1.scan():
        print("Device found at address", end=" ")
        print(hex(device_address), end=" (")
        printKnownChips(hex(device_address))
        print(end=")")
        print()
    # Unlock I2C now that we're done scanning.
    i2c1.unlock()


def i2cport2scan():
    print("Wire2")
    # Lock the I2C device before we try to scan
    while not i2c2.try_lock():
        pass
    # Print the addresses found once
    for device_address in i2c2.scan():
        print("Device found at address", end=" ")
        print(hex(device_address), end=" (")
        printKnownChips(hex(device_address))
        print(end=")")
        print()
    # Unlock I2C now that we're done scanning.
    i2c2.unlock()


def printKnownChips(address):
    # print("passed address:", address)
    if address == "0x00":
        print("AS3935", end=" ")
        return
    if address == "0x01":
        print("AS3935", end=" ")
        return
    if address == "0x02":
        print("AS3935", end=" ")
        return
    if address == "0x03":
        print("AS3935", end=" ")
        return
    if address == "0x04":
        print("ADAU1966", end=" ")
        return
    if address == "0x0a":
        print("SGTL5000", end=" ")
        return
    if address == "0x0b":
        print("SMBusBattery?", end=" ")
        return
    if address == "0x0c":
        print("AK8963", end=" ")
        return
    if address == "0x10":
        print("CS4272", end=" ")
        return
    if address == "0x11":
        print("Si4713", end=" ")
        return
    if address == "0x13":
        print("VCNL4000,AK4558", end=" ")
        return
    if address == "0x18":
        print("LIS331DLH", end=" ")
        return
    if address == "0x19":
        print("LSM303,LIS331DLH", end=" ")
        return
    if address == "0x1a":
        print("WM8731", end=" ")
        return
    if address == "0x1c":
        print("LIS3MDL", end=" ")
        return
    if address == "0x1d":
        print("LSM303D,LSM9DS0,ADXL345,MMA7455L,LSM9DS1,LIS3DSH", end=" ")
        return
    if address == "0x1e":
        print("LSM303D,HMC5883L,FXOS8700,LIS3DSH", end=" ")
        return
    if address == "0x20":
        print("MCP23017,MCP23008,PCF8574,FXAS21002,SoilMoisture", end=" ")
        return
    if address == "0x21":
        print("MCP23017,MCP23008,PCF8574", end=" ")
        return
    if address == "0x22":
        print("MCP23017,MCP23008,PCF8574", end=" ")
        return
    if address == "0x23":
        print("MCP23017,MCP23008,PCF8574", end=" ")
        return
    if address == "0x24":
        print("MCP23017,MCP23008,PCF8574,ADAU1966,HM01B0", end=" ")
        return
    if address == "0x25":
        print("MCP23017,MCP23008,PCF8574", end=" ")
        return
    if address == "0x26":
        print("MCP23017,MCP23008,PCF8574", end=" ")
        return
    if address == "0x27":
        print("MCP23017,MCP23008,PCF8574,LCD16x2,DigoleDisplay", end=" ")
        return
    if address == "0x28":
        print("BNO055,EM7180,CAP1188", end=" ")
        return
    if address == "0x29":
        print("TSL2561,VL6180,TSL2561,TSL2591,BNO055,CAP1188", end=" ")
        return
    if address == "0x2a":
        print("SGTL5000,CAP1188", end=" ")
        return
    if address == "0x2b":
        print("CAP1188", end=" ")
        return
    if address == "0x2c":
        print("MCP44XX ePot", end=" ")
        return
    if address == "0x2d":
        print("MCP44XX ePot", end=" ")
        return
    if address == "0x2e":
        print("MCP44XX ePot", end=" ")
        return
    if address == "0x2f":
        print("MCP44XX ePot", end=" ")
        return
    if address == "0x30":
        print("Si7210", end=" ")
        return
    if address == "0x31":
        print("Si7210", end=" ")
        return
    if address == "0x32":
        print("Si7210", end=" ")
        return
    if address == "0x33":
        print("MAX11614,MAX11615,Si7210", end=" ")
        return
    if address == "0x34":
        print("MAX11612,MAX11613", end=" ")
        return
    if address == "0x35":
        print("MAX11616,MAX11617", end=" ")
        return
    if address == "0x38":
        print("RA8875,FT6206,MAX98390", end=" ")
        return
    if address == "0x39":
        print("TSL2561, APDS9960", end=" ")
        return
    if address == "0x3c":
        print("SSD1306,DigisparkOLED", end=" ")
        return
    if address == "0x3d":
        print("SSD1306", end=" ")
        return
    if address == "0x40":
        print("PCA9685,Si7021,MS8607", end=" ")
        return
    if address == "0x41":
        print("STMPE610,PCA9685", end=" ")
        return
    if address == "0x42":
        print("PCA9685", end=" ")
        return
    if address == "0x43":
        print("PCA9685", end=" ")
        return
    if address == "0x44":
        print("PCA9685, SHT3X, ADAU1966", end=" ")
        return
    if address == "0x45":
        print("PCA9685, SHT3X", end=" ")
        return
    if address == "0x46":
        print("PCA9685", end=" ")
        return
    if address == "0x47":
        print("PCA9685", end=" ")
        return
    if address == "0x48":
        print("ADS1115,PN532,TMP102,LM75,PCF8591,CS42448", end=" ")
        return
    if address == "0x49":
        print("ADS1115,TSL2561,PCF8591,CS42448", end=" ")
        return
    if address == "0x4a":
        print("ADS1115,Qwiic Keypad,CS42448", end=" ")
        return
    if address == "0x4b":
        print("ADS1115,TMP102,BNO080,Qwiic Keypad,CS42448", end=" ")
        return
    if address == "0x50":
        print("EEPROM,FRAM", end=" ")
        return
    if address == "0x51":
        print("EEPROM", end=" ")
        return
    if address == "0x52":
        print("Nunchuk,EEPROM", end=" ")
        return
    if address == "0x53":
        print("ADXL345,EEPROM", end=" ")
        return
    if address == "0x54":
        print("EEPROM", end=" ")
        return
    if address == "0x55":
        print("EEPROM", end=" ")
        return
    if address == "0x56":
        print("EEPROM", end=" ")
        return
    if address == "0x57":
        print("EEPROM", end=" ")
        return
    if address == "0x58":
        print("TPA2016,MAX21100", end=" ")
        return
    if address == "0x5a":
        print("MPR121", end=" ")
        return
    if address == "0x60":
        print("MPL3115,MCP4725,MCP4728,TEA5767,Si5351", end=" ")
        return
    if address == "0x61":
        print("MCP4725,AtlasEzoDO", end=" ")
        return
    if address == "0x62":
        print("LidarLite,MCP4725,AtlasEzoORP", end=" ")
        return
    if address == "0x63":
        print("MCP4725,AtlasEzoPH", end=" ")
        return
    if address == "0x64":
        print("AtlasEzoEC, ADAU1966", end=" ")
        return
    if address == "0x66":
        print("AtlasEzoRTD", end=" ")
        return
    if address == "0x68":
        print("DS1307/3231,MPU6050/9050,MPU9250,ITG3200/3701,LSM9DS0,L3G4200D", end=" ")
        return
    if address == "0x69":
        print("MPU6050,MPU9050,MPU9250,ITG3701,L3G4200D", end=" ")
        return
    if address == "0x6a":
        print("LSM9DS1", end=" ")
        return
    if address == "0x6b":
        print("LSM9DS0", end=" ")
        return
    if address == "0x6f":
        print("Qwiic Button", end=" ")
        return
    if address == "0x70":
        print("HT16K33,TCA9548A", end=" ")
        return
    if address == "0x71":
        print("SFE7SEG,HT16K33", end=" ")
        return
    if address == "0x72":
        print("HT16K33", end=" ")
        return
    if address == "0x73":
        print("HT16K33", end=" ")
        return
    if address == "0x76":
        print("MS5607,MS5611,MS5637,BMP280", end=" ")
        return
    if address == "0x77":
        print("BMP085,BMA180,BMP280,MS5611", end=" ")
        return
    if address == "0x7c":
        print("FRAM_ID", end=" ")
        return
    print("UNKNOWN DEVICE", end=" ")
    return


i2cportscan()
i2cport1scan()
i2cport2scan()
sys.exit()


