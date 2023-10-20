from machine import Pin
import neopixel
import urandom
import time

# create NeoPixel driver on GPIO0 for 8 pixels
np = neopixel.NeoPixel(Pin(28), 8)

while True:
    for i in range(8):  # 8 for the number of LEDs in the strip
        # generate random RGB values
        r = urandom.randint(0, 100)
        g = urandom.randint(0, 100)
        b = urandom.randint(0, 100)

        # set the LED to the random color
        np[i] = (r, g, b)

    # write data to all pixels
    np.write()

    # wait for a second
    time.sleep(0.1)
