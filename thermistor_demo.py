import machine
from math import log
import utime

# Constants for the specific thermistor (10k NTC Thermistor with B=3380)
A       = 0.001129148
B       = 0.000234125
C       = 0.0000000876741

# Pin connected to the thermistor
adc     = machine.ADC(26)

# The resistance of the fixed resistor
R_fixed = 10000

while True:
    # Read the ADC value
    adc_value    = adc.read_u16()

    # Convert the ADC reading into a voltage
    Vout         = 3.3 * (adc_value / 65535)

    # Calculate the resistance of the thermistor
    R_thermistor = R_fixed * (3.3 - Vout) / Vout

    # Use the Steinhart-Hart equation to calculate temperature in Kelvin
    logR        = log(R_thermistor)
    T           = 1.0 / (A + B * logR + C * logR * logR * logR)

    # Convert from Kelvin to Celsius
    Tc          = T - 273.15

    # Convert from Celsius to Fahrenheit
    Tf          = (Tc * 9.0/5.0) + 32.0

    print("Temperature: {:.2f} °F, {:.2f} °C".format(Tf,Tc))
    utime.sleep(1)
