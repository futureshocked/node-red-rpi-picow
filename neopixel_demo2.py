from machine import Pin
import neopixel
import time

np = neopixel.NeoPixel(Pin(28), 8)

while True:
    for i in range(8):
        np[i] = (255, 0, 0)
        np.write()
        time.sleep(0.5)
        np[i] = (0, 0, 0)