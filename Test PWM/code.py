import board
import pwmio
import time
import supervisor

print("setupPWM pin 1")

pwm1 = pwmio.PWMOut(board.D1, frequency=5000, variable_frequency=True, duty_cycle=32767+16384) #1x1
print("setupPWM pin 2")
pwm2 = pwmio.PWMOut(board.D2, frequency=5000, variable_frequency=False, duty_cycle=16384) #4A2
print("setupPWM pin 3")
pwm3 = pwmio.PWMOut(board.D3, frequency=5000, variable_frequency=False, duty_cycle=32767) #4A2
print("setupPWM pin 4")
pwm4 = pwmio.PWMOut(board.D4, frequency=5000, variable_frequency=False, duty_cycle=16384) #4A2
print("setupPWM pin 24")
pwm24 = pwmio.PWMOut(board.D24, frequency=5000, variable_frequency=False, duty_cycle=32767) #4A2
print("setupPWM pin 53")
pwm53 = pwmio.PWMOut(board.D53, frequency=5000, variable_frequency=False, duty_cycle=16384) #4A2
#pwm10 = pwmio.PWMOut(board.D10, frequency=5000, variable_frequency=True, duty_cycle=32767) #Q10
print("setup done")
while True:
    #if supervisor.runtime.serial_bytes_available:
    #    foo # cause it to break
    time.sleep(0.25)

