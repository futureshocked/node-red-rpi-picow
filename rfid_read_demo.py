from mfrc522 import MFRC522
import utime
 
# The numbers below refer to Raspberry Pi Pico GPIOs.
# The spi_id number refers to the SPI channel in use, which is 0.
reader = MFRC522(spi_id=0,sck=2,miso=4,mosi=3,cs=0,rst=5)
 
print("Bring TAG closer...")
print("")
 
 
while True:
    reader.init()
    (stat, tag_type) = reader.request(reader.REQIDL)
    if stat == reader.OK:
        (stat, uid) = reader.SelectTagSN()
        if stat == reader.OK:
            card = int.from_bytes(bytes(uid),"little",False)
            print("CARD ID: "+str(card))

utime.sleep_ms(500) 