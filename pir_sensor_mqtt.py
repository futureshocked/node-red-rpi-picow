from machine import Pin
import time
from umqtt.simple import MQTTClient
from time import sleep
import network

# Configure your Wi-Fi credentials
SSID      = '<--WIFI-NETWORK-NAME-->'
PASSWORD  = '<--WIFI-PASSWORD-->'

print('Starting...')

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID,PASSWORD)

print('Trying to connect to Wifi...')

while not wlan.isconnected():
    print('.', end='')
    time.sleep(1)
    pass

print('Connected to Wi-Fi')
print(wlan.ifconfig())

# Configure MQTT
SERVER     = '<--SERVER-IP-ADDRESS-->'  # Replace with your MQTT broker IP
CLIENT_ID  = b'PICO'
TOPIC      = b'pir'
USER       = b'<--MQTT_USER-->'    # Replace with your MQTT username
PASSWORD   = b'<--MQTT_PASSWORD-->'# Replace with your MQTT password

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
   sleep(5)
   machine.reset()

try:
   client = mqtt_connect()
except OSError as e:
   reconnect()

pir = Pin(18, Pin.IN)

while True:
    if pir.value():
        print("Motion detected!")
        client.publish(TOPIC, "Motion detected!")
    else:
        print("No motion.")
        client.publish(TOPIC, "No motion.")
    time.sleep(1)
