import machine
import utime

# Define the HC595N pins
data_pin = machine.Pin(20, machine.Pin.OUT)
latch_pin = machine.Pin(16, machine.Pin.OUT)
clock_pin = machine.Pin(18, machine.Pin.OUT)

def shift_out(data):
    latch_pin.low()
    for i in range(8):
        if data & (1 << (7 - i)):
            data_pin.high()
        else:
            data_pin.low()
        clock_pin.high()
        utime.sleep(0.001)
        clock_pin.low()
    latch_pin.high()

# Now, let's light up the LEDs one by one and then turn them off in reverse order
while True:
    for i in range(4):
        shift_out(1 << i)
        utime.sleep(0.5)

    for i in range(4):
        shift_out(1 << (3 - i))
        utime.sleep(0.5)
