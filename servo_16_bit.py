from machine import Pin, PWM
import time

# Define the pin where PWM signal will be generated
pwm_pin = Pin(18)

# Initialize the PWM object on the specified pin with 16-bit resolution
pwm     = PWM(pwm_pin)

# Set the frequency (for example, 50 Hz)
pwm.freq(50)

# Set the duty cycle using the full 16-bit resolution (0 to 65535)
pwm.duty_u16(32768) # 50% duty cycle

# Optional: Ramp the duty cycle from 0 to 100%
for i in range(65536):
    pwm.duty_u16(i)
    time.sleep(0.001)

# Deinitialize to stop the PWM
pwm.deinit()
