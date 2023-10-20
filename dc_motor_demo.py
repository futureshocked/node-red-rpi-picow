import machine
import utime

motor1 = machine.Pin(14, machine.Pin.OUT)
motor2 = machine.Pin(15, machine.Pin.OUT)

def clockwise():
    motor1.high()
    motor2.low()

def anticlockwise():
    motor1.low()
    motor2.high()

def stopMotor():
    motor1.low()
    motor2.low()

while True:
    clockwise()
    utime.sleep(1)
    stopMotor()
    utime.sleep(1)
    anticlockwise()
    utime.sleep(1)
    stopMotor()
    utime.sleep(1)