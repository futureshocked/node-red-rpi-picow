from machine import Pin, PWM
import time

motor1 = Pin(14, machine.Pin.OUT)
pin    = Pin(15, machine.Pin.OUT)
pwm    = PWM(pin)
pwm.freq(50)

motor1.low()

while True:
    duty(51)
    time.sleep(1)
    for d in range(52,103):
        duty(d)
        time.sleep(0.2)
    time.sleep(1)
