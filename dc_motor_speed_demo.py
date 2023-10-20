from machine import Pin, PWM
import time

motor1    = Pin(15, machine.Pin.OUT)
motor2pwm = Pin(14)

# Create a PWM object attached to motor2pwm pin
motor_pwm = PWM(motor2pwm)

# Set the PWM frequency (usually 50Hz to 2kHz for motor control)
motor_pwm.freq(50)

# Function to set motor speed (0 to 1023)
def set_speed(speed):
    if speed   < 0:
        speed  = 0
    elif speed > 1023:
        speed  = 1023
    motor_pwm.duty_u16(speed * 64) # PWM duty is 16-bit, so multiply by 64

# Example of using set_speed function to control motor speed
motor1.low()  # set spin direction
set_speed(1000) # 25% speed
time.sleep(2)

set_speed(0) # Stop
motor1.low()
time.sleep(5)

motor1.high()   # set oposite spin direction
set_speed(100) # 25% speed
time.sleep(2)

set_speed(0) # Stop
motor1.low()
time.sleep(2)
