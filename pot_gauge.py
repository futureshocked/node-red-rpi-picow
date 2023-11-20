from machine import Pin, ADC
from umqtt.simple import MQTTClient
from time import sleep
import network

# Configure the potentiometer
pot = ADC(26) # if connected to GP26 which is ADC0

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
TOPIC     = b'pot_gauge'
USER      = b'<--MQTT_USER-->'    # Replace with your MQTT username
PASSWORD  = b'<--MQTT_PASSWORD-->'# Replace with your MQTT password

def mqtt_connect():
   client = MQTTClient(CLIENT_ID, SERVER, user=USER, password=PASSWORD, keepalive=3600)
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
    value = pot.read_u16()
    client.publish(TOPIC, str(value))
    print("Pot value = ", value)
    sleep(1.0)
