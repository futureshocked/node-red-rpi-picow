from machine import Pin
from time import sleep
from umqtt.simple import MQTTClient
import network

led = Pin(15, Pin.OUT)

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
SERVER       = '<--SERVER-IP-ADDRESS-->'  # Replace with your MQTT broker IP
CLIENT_ID    = b'PICO'
TOPIC_LED    = b'led_state'
TOPIC_BUTTON = b'button_state'
USER         = b'<--MQTT_USER-->'    # Replace with your MQTT username
PASSWORD     = b'<--MQTT_PASSWORD-->'# Replace with your MQTT password

client       = MQTTClient( CLIENT_ID,
                           SERVER,
                           user=USER,
                           password=PASSWORD,
                           keepalive=3600
                           )
client.connect()

def button_callback(pin):
    if button.value():
        print('Button Pressed')
        client.publish(TOPIC_BUTTON, "1")
    else:
        print('Button Unpressed')
        client.publish(TOPIC_BUTTON, "0")

button = Pin(14, Pin.IN, Pin.PULL_UP)
button.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=button_callback)

def led_callback(topic, msg):
    if msg == b'on':
        print('LED ON')
        led.value(1)
    elif msg == b'off':
        print('LED OFF')
        led.value(0)

client.set_callback(led_callback)
client.subscribe(TOPIC_LED)

while True:
    client.wait_msg()
