import time
import board
import digitalio
import rotaryio
from rainbowio import colorwheel
import neopixel
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

kbd = Keyboard(usb_hid.devices)
cc = ConsumerControl(usb_hid.devices)

encoder = rotaryio.IncrementalEncoder(board.D10, board.D9)
last_position = encoder.position

pixel_pin = board.D2
num_pixels = 4

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=1, auto_write=False)


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            rc_index = (i * 256 // num_pixels) + j
            pixels[i] = colorwheel(rc_index & 255)
        pixels.show()
        time.sleep(wait)

BLACK = (0,0,0)
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)

keySwitchLEDTimeout = [0,0,0,0]
KeySwitchPins = [board.D7, board.D3, board.D1, board.D4] # Up Down Left Right
LED_index = [3, 1, 0, 2] # Up Down Left Right\
KeySwitchIOs = []
for key in KeySwitchPins:
    thisSwitch = digitalio.DigitalInOut(key)
    thisSwitch.pull = digitalio.Pull.UP
    KeySwitchIOs.append(thisSwitch)

while True:
    time.sleep(0.1)
    for i in range(len(KeySwitchIOs)):
        if KeySwitchIOs[i].value is False:
            pixels[LED_index[i]] = BLUE
            pixels.show()
        else:
            pixels[LED_index[i]] = BLACK

    current_position = encoder.position
    position_change = current_position - last_position
    if position_change > 0:
        for _ in range(position_change):
            cc.send(ConsumerControlCode.VOLUME_INCREMENT)
    elif position_change < 0:
        for _ in range(-position_change):
            cc.send(ConsumerControlCode.VOLUME_DECREMENT)
    last_position = current_position
