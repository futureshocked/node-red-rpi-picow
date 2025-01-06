import machine
import utime
from umqtt.simple import MQTTClient
import ujson
import network
from time import sleep
from time import sleep_ms

# Define pins
ser   = machine.Pin(20, machine.Pin.OUT)
rclk  = machine.Pin(18, machine.Pin.OUT)
srclk = machine.Pin(16, machine.Pin.OUT)

# Define LED patterns in an array
led_patterns = [0b10000001, 0b01000010, 0b00100100, 0b00011000,
                0b00011000, 0b00100100, 0b01000010, 0b10000001, 0b00000000]

# Wi-Fi credentials
SSID        = '<--WIFI-NETWORK-NAME-->'
PASSWORD    = '<--WIFI-PASSWORD-->'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID,PASSWORD)

while not wlan.isconnected():
    pass

print('Connected to Wi-Fi')
print(wlan.ifconfig())

# MQTT parameters
SERVER      = '<--SERVER-IP-ADDRESS-->'  # Replace with your MQTT broker IP
CLIENT_ID   = b'pico'
TOPIC       = b'LED_shift'
USER        = b'<--MQTT_USER-->'    # Replace with your MQTT username
PASSWORD    = b'<--MQTT_PASSWORD-->'# Replace with your MQTT password

# Function to shift data into 74HC595
def hc595_shift(dat):
    rclk.low()
    sleep_ms(5)
    for bit in range(7, -1, -1):
        srclk.low()
        sleep_ms(5)
        value = 1 & (dat >> bit)
        ser.value(value)
        sleep_ms(5)
        srclk.high()
        sleep_ms(5)
    sleep_ms(5)
    rclk.high()
    sleep_ms(5)

def mqtt_connect():
   client = MQTTClient(CLIENT_ID, SERVER, user=USER, password=PASSWORD, keepalive=3600)
   client.connect()
   print('Connected to %s MQTT Broker'%(SERVER))
   return client

def reconnect():
   print('Failed to connect to the MQTT Broker. Reconnecting...')
   sleep(5)
   machine.reset()

def on_message(topic, msg):
    print("Received message:", msg.decode())
    hc595_shift(led_patterns[int(msg.decode())])

def main(server, topic, username, passw):
    client = MQTTClient(CLIENT_ID, server, user=username, password=passw, keepalive=3600)
    client.set_callback(on_message)
    client.connect()
    client.subscribe(topic)
    print("Connected to %s, subscribed to %s topic" % (server, topic))

    try:
        while True:
            client.check_msg()
            sleep(0.5)

    finally:
        client.disconnect()

main(SERVER, TOPIC, USER, PASSWORD)
