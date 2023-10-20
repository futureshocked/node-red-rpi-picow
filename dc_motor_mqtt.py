from machine import Pin, PWM
from time import sleep
from umqtt.simple import MQTTClient
import network

motor1    = Pin(15, machine.Pin.OUT)
motor2pwm = Pin(14)

# Create a PWM object attached to motor2pwm pin
motor_pwm = PWM(motor2pwm)

# Set the PWM frequency (usually 50Hz to 2kHz for motor control)
motor_pwm.freq(50)


def map_value(value, from_min=0, from_max=10, to_min=0, to_max=65472):
    # Ensure the value is within the expected range
    value = max(min(value, from_max), from_min)

    # Perform the mapping
    return int((value - from_min) * (to_max - to_min) / (from_max - from_min) + to_min)


# Function to set motor speed (expected input is from 0 to 10)
def set_speed(speed):
    if speed   < 0:
        speed  = 0
    elif speed > 10:
        speed  = 10
    motor_pwm.duty_u16(map_value(speed)) # PWM duty is 16-bit


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
SERVER    = '<--SERVER-IP-ADDRESS-->'  # Replace with your MQTT broker IP
CLIENT_ID = b'PICO'
TOPIC     = b'motor_control'
USER      = b'<--MQTT_USER-->'    # Replace with your MQTT username
PASSWORD  = b'<--MQTT_PASSWORD-->'# Replace with your MQTT password

def reconnect():
   print('Failed to connect to the MQTT Broker. Reconnecting...')
   sleep(5)
   machine.reset()

def on_message(topic, msg):
    direction_speed = msg.decode()
    print("Received message:", direction_speed)
    components      = direction_speed.split(',')
    direction       = int(components[0])
    speed           = int(components[1])

    if direction == 0:
        motor1.low()
    else:
        motor1.high()
        speed = 10 - speed # reverse the speed to make it compatible with the direction

    set_speed(speed)

    sleep(2)
    # now, stop the motor
    motor1.low()
    set_speed(0)
    sleep(1)

def main(server, topic, username, passw):
    client = MQTTClient(CLIENT_ID,
                        server,
                        user=username,
                        password=passw,
                        keepalive=3600)
    client.set_callback(on_message)
    client.connect()
    client.subscribe(topic)
    print("Connected to %s, subscribed to %s topic" % (server, topic))

    try:
        while True:
            client.check_msg()
            sleep(1)

    finally:
        client.disconnect()

main(SERVER, TOPIC, USER, PASSWORD)
