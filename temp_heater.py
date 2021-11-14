import analogio
import board
import time
from digitalio import DigitalInOut, Direction

led = DigitalInOut(board.D13)

led.direction = Direction.OUTPUT

thermistor = analogio.AnalogIn(board.A7)

def steinhart_temperature_C(r, Ro=10000.0, To=25.0, beta=3950.0):
    import math
    steinhart = math.log(r / Ro) / beta      # log(R/Ro) / beta
    steinhart += 1.0 / (To + 273.15)         # log(R/Ro) / beta + 1/To
    steinhart = (1.0 / steinhart) - 273.15   # Invert, convert to C
    return steinhart

while True:
    R = 10000 / (65535/thermistor.value - 1)
    print('Thermistor resistance: {} ohms'.format(R))

    temp = steinhart_temperature_C(R)
    if temp >= 80:
        led.value = True
    else:
        led.value = False

    led.value = True
    time.sleep(5)
    print(temp)
