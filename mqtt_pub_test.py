from machine import Pin
from time import sleep
from umqtt.simple import MQTTClient
import network
from random import *

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

# Setup MQTT
SERVER     = '<--SERVER-IP-ADDRESS-->'  # Replace with your MQTT broker IP
CLIENT_ID  = b'PICO'
TOPIC_TEMP = b'sensor_temperature'
TOPIC_HUMD = b'sensor_humidity'
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

while True:
    temp = randint(10, 30)
    humd = randint(50, 90)
    client.publish(TOPIC_TEMP, str(temp))
    client.publish(TOPIC_HUMD, str(humd))
    print("Published temp = ", temp, ", humd = ", humd)
    sleep(5.0)
