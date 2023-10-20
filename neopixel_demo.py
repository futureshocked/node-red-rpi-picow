from machine import Pin
import neopixel

# create NeoPixel driver on GPIO0 for 8 pixels
np = neopixel.NeoPixel(Pin(28), 8) # Using GP28 because it is convenient.

# set the first pixel to red
np[0] = (255, 0, 0)
np[1] = (0, 255, 0)
np[2] = (0, 0, 255)

# write data to all pixels
np.write()
