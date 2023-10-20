import machine
import utime

sensor = machine.ADC(26)

while True:
    value = sensor.read_u16()
    print(value)
    utime.sleep_ms(200)
    
    
'''
# detecting significant changes in the water level

threshold = 25000 # This value needs to be as needed.

while True:
       value = sensor.read_u16()
       if value < threshold :
           print("Liquid leakage!")
       utime.sleep_ms(200)
'''