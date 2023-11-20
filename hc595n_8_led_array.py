import machine
import time

# Define pins
ser = machine.Pin(20, machine.Pin.OUT)
rclk = machine.Pin(18, machine.Pin.OUT)
srclk = machine.Pin(16, machine.Pin.OUT)

# Define LED patterns in an array
led_patterns = [0b10000001, 0b01000010, 0b00100100, 0b00011000,
                0b00011000, 0b00100100, 0b01000010, 0b10000001]

# Function to shift data into 74HC595
def hc595_shift(dat):
    rclk.low()
    time.sleep_ms(5)
    for bit in range(7, -1, -1):
        srclk.low()
        time.sleep_ms(5)
        value = 1 & (dat >> bit)
        ser.value(value)
        time.sleep_ms(5)
        srclk.high()
        time.sleep_ms(5)
    time.sleep_ms(5)
    rclk.high()
    time.sleep_ms(5)

# Main loop to iterate through the LED patterns
while True:
    for pattern in led_patterns:
        hc595_shift(pattern)
        print("{:0>8b}".format(pattern)) # Print the pattern in binary
        time.sleep_ms(200)
