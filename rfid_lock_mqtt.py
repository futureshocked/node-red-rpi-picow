from mfrc522 import MFRC522
from umqtt.simple import MQTTClient
from time import sleep
import network

# The numbers below refer to Raspberry Pi Pico GPIOs.
# The spi_id number refers to the SPI channel in use, which is 0.
reader = MFRC522(spi_id=0,sck=2,miso=4,mosi=3,cs=0,rst=5)

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
TOPIC      = b'rfid_status'
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
    reader.init()
    (stat, tag_type) = reader.request(reader.REQIDL)
    if stat == reader.OK:
        (stat, uid) = reader.SelectTagSN()
        if stat == reader.OK:
            card = int.from_bytes(bytes(uid),"little",False)
            print("CARD ID: "+str(card))
            if card == 560441490:
                print("Card ID: "+ str(card)+" PASS: Open door")
                client.publish(TOPIC, "open")
            else:
                print("Card ID: "+ str(card)+" UNKNOWN CARD! Lock door")
                client.publish(TOPIC, "close")
    sleep(1)
