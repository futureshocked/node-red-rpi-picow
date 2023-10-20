import machine
import utime
import time
from umqtt.simple import MQTTClient
from time import sleep
import network

# Configure your Wi-Fi credentials
SSID     = '<--WIFI-NETWORK-NAME-->'
PASSWORD = '<--WIFI-PASSWORD-->'

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
SERVER    = '<--SERVER-IP-ADDRESS-->'  # Replace with your MQTT broker IP
CLIENT_ID = b'PICO'
TOPIC     = b'waterlevel'
USER      = b'<--MQTT_USER-->'    # Replace with your MQTT username
PASSWORD  = b'<--MQTT_PASSWORD-->'# Replace with your MQTT password

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

sensor = machine.ADC(26)

while True:
    value = sensor.read_u16()
    print(value)
    client.publish(TOPIC, str(value))
    utime.sleep_ms(200)
