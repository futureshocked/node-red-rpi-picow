import time
from machine import Pin
from dht import DHT11

# Create a DHT11 instance
dht11 = DHT11(Pin(18))  # the DATA pin is connected to GP2 on the Raspberry Pi Pico

while True:
    dht11.measure()  # make a new measurement
    temp = dht11.temperature()  # read temperature
    hum  = dht11.humidity()  # read humidity
    print('Temperature:', temp, 'C', 'Humidity:', hum, '%')
    time.sleep(5)  # wait for 5 seconds
