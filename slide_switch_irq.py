from machine import Pin

slide = Pin(14, Pin.IN, Pin.PULL_DOWN)

def check_slide():
   if slide.value():
      print('Right')
   else:
      print('Left')

def button_callback(pin):
    check_slide()

slide.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=button_callback)

check_slide()

while True:
    pass