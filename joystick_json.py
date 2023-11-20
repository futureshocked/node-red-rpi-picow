from machine import ADC, Pin
import utime
import json

# Initialize ADC for the joystick's VRx and VRy pins
adc_x = ADC(26)
adc_y = ADC(27)

# Initialize Pin for the joystick's SW pin (button)
button = Pin(17, Pin.IN, Pin.PULL_UP)

while True:
    # Read X and Y coordinates
    x = adc_x.read_u16()
    y = adc_y.read_u16()
    
    # Read button state
    btn_state = button.value()


    
    # Create a dictionary to hold the data
    data = {
        'x_value': x,
        'y_value': y,
        'button_value': 'Pressed' if btn_state == 0 else 'Not Pressed'
    }
    
    print('X:', x, 'Y:', y, 'Button:', 'Pressed' if btn_state == 0 else 'Not pressed')
    
    # Convert the dictionary to a JSON string
    data_json = json.dumps(data)
    
    print(data_json)

    # Delay to avoid flooding console
    utime.sleep(0.1)

