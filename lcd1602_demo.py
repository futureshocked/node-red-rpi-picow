from machine import I2C, Pin
from time import sleep
from pico_i2c_lcd import I2cLcd
i2c = I2C(1, sda=Pin(14), scl=Pin(15), freq=400000)

I2C_ADDR = i2c.scan()[0]
lcd_device = I2cLcd(i2c, I2C_ADDR, 2, 16)

lcd_device.putstr("Hello world")
counter = 0

while True:
    lcd_device.move_to(0, 1)
    lcd_device.putstr(str(counter))

    counter += 1
    sleep(1)
