from machine import Pin
from umqtt.simple import MQTTClient
import time
import network

# Configure your Wi-Fi credentials
SSID     = '<--WIFI-NETWORK-NAME-->'
PASSWORD = '<--WIFI-PASSWORD-->'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID,PASSWORD)

while not wlan.isconnected():
    pass

print('Connected to Wi-Fi')
print(wlan.ifconfig())

# Configure MQTT
SERVER    = '<--SERVER-IP-ADDRESS-->'  # Replace with your MQTT broker IP
CLIENT_ID = b'PICO'
TOPIC     = b'pico/range'
USER      = b'<--MQTT_USER-->'    # Replace with your MQTT username
PASSWORD  = b'<--MQTT_PASSWORD-->'# Replace with your MQTT password

# Define the pins where the sensor is connected
trigger   = machine.Pin(19, machine.Pin.OUT)
echo      = machine.Pin(18, machine.Pin.IN)

def get_distance():
    # Send a 10 microsecond pulse.
    trigger.low()
    time.sleep_us(2)  # Wait for 2 microseconds low pulse
    trigger.high()
    time.sleep_us(10)  # Keep the trigger high for 10 microseconds
    trigger.low()

    # Wait for the pulse on the echo pin.
    while echo.value() == 0:
        pass
    start = time.ticks_us()

    # Measure the duration of the high pulse.
    while echo.value() == 1:
        pass
    finish = time.ticks_us()

    # Calculate the distance in centimeters and return it.
    return (finish - start) / 58.0

def mqtt_connect():
   client = MQTTClient(CLIENT_ID,
                       SERVER,
                       user=USER,
                       password=PASSWORD,
                       keepalive=3600)
   client.connect()
   print('Connected to %s MQTT Broker'%(SERVER))
   return client

def reconnect():
   print('Failed to connect to the MQTT Broker. Reconnecting...')
   time.sleep(5)
   machine.reset()

try:
    print("Connecting to the MQTT Broker...")
    client = mqtt_connect()
except OSError as e:
    reconnect()

# Send range to MQTT broker every second
while True:
    distance = get_distance()
    print("Distance: ", distance, "cm")
    client.publish(TOPIC, str(distance))
    time.sleep(1)
