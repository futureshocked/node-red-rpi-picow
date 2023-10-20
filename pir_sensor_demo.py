from machine import Pin
import time

pir = Pin(18, Pin.IN)

while True:
    if pir.value():
        print("Motion detected!")
    else:
        print("No motion.")
    time.sleep(1)
