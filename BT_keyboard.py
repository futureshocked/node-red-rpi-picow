import bluetooth
import time

# Initialize Bluetooth
bt = bluetooth.Bluetooth()

# Start Bluetooth
bt.active(True)

# Make device discoverable
bt.advertise("PicoW")

# Connect to Bluetooth Keyboard
keyboard_address = "CC:C5:0A:22:16:83"  # Replace with your keyboard's Bluetooth address

if bt.connect(keyboard_address):
    print("Connected to the keyboard!")
else:
    print("Failed to connect.")
    bt.active(False)

# Read data from keyboard
while True:
    if bt.isconnected():
        data = bt.recv(64)
        if data:
            print("Received:", data.decode())
    else:
        print("Disconnected. Exiting loop.")
        break

    time.sleep(0.1)
