import machine
import time

# Define the pins where the sensor is connected
trigger = machine.Pin(19, machine.Pin.OUT)
echo    = machine.Pin(18, machine.Pin.IN)

def get_distance():
    # Send a 10 microsecond pulse.
    trigger.low()
    time.sleep_us(2)  # Wait for 2 microseconds low pulse
    trigger.high()
    time.sleep_us(10)  # Keep the trigger high for 10 microseconds
    trigger.low()
    
    # Wait for the pulse on the echo pin.
    while echo.value() == 0:
        pass
    start = time.ticks_us()
    
    # Measure the duration of the high pulse.
    while echo.value() == 1:
        pass
    finish = time.ticks_us()
    
    # Calculate the distance in centimeters and return it.
    return (finish - start) / 58.0

while True:
    print("Distance: ", get_distance(), "cm")
    time.sleep(1)
