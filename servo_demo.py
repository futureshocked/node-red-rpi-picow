from machine import Pin, PWM
import utime

# Define the GPIO pin and the frequency (50Hz is common for servo motors)
GPIO_PIN = 18
FREQ     = 50

# Create a PWM object
pwm = PWM(Pin(GPIO_PIN))

# Set the PWM frequency
pwm.freq(FREQ)

def set_angle(angle):
    # Duty cycle for servo is between 2.5% (0 degrees) and 12.5% (180 degrees)
    duty = 2.5 + (angle / 180) * 10
    # Update duty cycle
    pwm.duty_u16(int(duty * 65535 / 100))

# Set the servo to 90 degrees
set_angle(90)
utime.sleep(1)

# Set the servo to 180 degrees
set_angle(180)
utime.sleep(1)

# Set the servo to 0 degrees
set_angle(0)
utime.sleep(1)


# Make the servo motor continuously rotate from 0 to 180 degrees and back
while True:
    for angle in range(0, 180, 10): # Go from 0 to 180 degrees
        set_angle(angle)
        utime.sleep(0.5)
    for angle in range(180, -1, -10): # Go from 180 back to 0 degrees
        set_angle(angle)
        utime.sleep(0.5)

# Turn off PWM
pwm.deinit()
