import utime
from machine import Pin, freq
from ir_rx.print_error import print_error
from ir_rx.nec import NEC_8

pin_ir = Pin(17, Pin.IN)

# Define the callback function
def callback(data, addr, ctrl):
    if data < 0:  # NEC protocol sends repeat codes.
        pass
    else:
        print('Data received: ', data)
        print('Address: ', addr)
        print('Control bit: ', ctrl)

# Initialize the IR_RX object
ir = NEC_8(pin_ir, callback)
ir.error_function(print_error)  # Show debug information

try:
    while True:
        pass
except KeyboardInterrupt:
    ir.close()
