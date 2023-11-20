import time
from machine import Pin, freq
from ir_rx.print_error import print_error
from ir_rx.nec import NEC_8
from umqtt.simple import MQTTClient
import network

pin_ir = Pin(17, Pin.IN)

def decodeKeyValue(data):
    if data == 0x16:
        return "0"
    if data == 0x0C:
        return "1"
    if data == 0x18:
        return "2"
    if data == 0x5E:
        return "3"
    if data == 0x08:
        return "4"
    if data == 0x1C:
        return "5"
    if data == 0x5A:
        return "6"
    if data == 0x42:
        return "7"
    if data == 0x52:
        return "8"
    if data == 0x4A:
        return "9"
    if data == 0x09:
        return "+"
    if data == 0x15:
        return "-"
    if data == 0x7:
        return "EQ"
    if data == 0x0D:
        return "U/SD"
    if data == 0x19:
        return "CYCLE"
    if data == 0x44:
        return "PLAY/PAUSE"
    if data == 0x43:
        return "FORWARD"
    if data == 0x40:
        return "BACKWARD"
    if data == 0x45:
        return "POWER"
    if data == 0x47:
        return "MUTE"
    if data == 0x46:
        return "MODE"
    return "ERROR"

# User callback
def callback(data, addr, ctrl):
    if data < 0:  # NEC protocol sends repeat codes.
        pass
    else:
        decoded_value = decodeKeyValue(data)
        print(decoded_value)
        client.publish(TOPIC, decoded_value)

ir = NEC_8(pin_ir, callback)  # Instantiate receiver
ir.error_function(print_error)  # Show debug information

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
SERVER     = '<--SERVER-IP-ADDRESS-->'  # Replace with your MQTT broker IP
CLIENT_ID  = b'PICO'
TOPIC      = b'IR_received_command'
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

try:
    while True:
        pass
except KeyboardInterrupt:
    ir.close()
