"""
Example IMU Control
Robo HAT MM1
https://github.com/wallarug/circuitpython_mpu9250
"""
import time
import board
import busio
from robohat_mpu9250.mpu9250 import MPU9250
from robohat_mpu9250.mpu6500 import MPU6500
from robohat_mpu9250.ak8963 import AK8963
import mahony
from time import sleep

i2c = busio.I2C(board.SCL, board.SDA)

mpu = MPU6500(i2c, address=0x68)
ak = AK8963(i2c)

sensor = MPU9250(mpu, ak)

MAG_MIN = [-28.06, 11.6279, -83.3449]
MAG_MAX = [45.2994, 88.7783, -4.42383]

## Used to calibrate the magenetic sensor
def map_range(x, in_min, in_max, out_min, out_max):
    """
    Maps a number from one range to another.
    :return: Returns value mapped to new range
    :rtype: float
    """
    mapped = (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    if out_min <= out_max:
        return max(min(mapped, out_max), out_min)

    return min(max(mapped, out_max), out_min)


## create the ahrs_filter
ahrs_filter = mahony.Mahony(50, 5, 100)

count = 0  # used to count how often we are feeding the ahrs_filter
lastPrint = time.monotonic()  # last time we printed the yaw/pitch/roll values
timestamp = time.monotonic_ns()  # used to tune the frequency to approx 100 Hz

print("Reading in data from IMU.")
print("MPU9250 id: " + hex(sensor.read_whoami()))

while True:
    # print('Acceleration (m/s^2): ({0:0.3f},{1:0.3f},{2:0.3f})'.format(*sensor.read_acceleration()))
    # print('Magnetometer (gauss): ({0:0.3f},{1:0.3f},{2:0.3f})'.format(*sensor.read_magnetic()))
    # print('Gyroscope (degrees/sec): ({0:0.3f},{1:0.3f},{2:0.3f})'.format(*sensor.read_gyro()))
    # print('Temperature: {0:0.3f}C'.format(sensor.read_temperature()))
    
            # read the magenetic sensor
    if (time.monotonic_ns() - timestamp) > 6500000:

        # read the magenetic sensor
        mx, my, mz = sensor.read_magnetic()

        # adjust for magnetic calibration - hardiron only
        # calibration varies per device and physical location
        mx = map_range(mx, MAG_MIN[0], MAG_MAX[0], -1, 1)
        my = map_range(my, MAG_MIN[1], MAG_MAX[1], -1, 1)
        mz = map_range(mz, MAG_MIN[2], MAG_MAX[2], -1, 1)

        # read the gyroscope
        gx, gy, gz = sensor.read_gyro()
        # adjust for my gyro calibration values
        # calibration varies per device and physical location
        gx -= 0.0122643
        gy -= 0.00239408
        gz -= 0.0228527

        # read the accelerometer
        ax, ay, az = sensor.read_acceleration()

        # update the ahrs_filter with the values
        # gz and my are negative based on my installation
        ahrs_filter.update(gx, gy, -gz, ax, ay, az, mx, -my, mz)

        count += 1
        timestamp = time.monotonic_ns()

    # every 0.1 seconds print the ahrs_filter values
    if time.monotonic() > lastPrint + 0.1:
        # ahrs_filter values are in radians/sec multiply by 57.20578 to get degrees/sec
        yaw = ahrs_filter.yaw * 57.20578
        if yaw < 0:  # adjust yaw to be between 0 and 360
            yaw += 360
        print(
            "Orientation: ",
            yaw,
            ", ",
            ahrs_filter.pitch * 57.29578,
            ", ",
            ahrs_filter.roll * 57.29578,
        )
        print(
            "Quaternion: ",
            ahrs_filter.q0,
            ", ",
            ahrs_filter.q1,
            ", ",
            ahrs_filter.q2,
            ", ",
            ahrs_filter.q3,
        )

        # print("Count: ", count)    # optionally print out frequency
        count = 0  # reset count
        lastPrint = time.monotonic()