import time
import math
import board
import digitalio
import rotaryio
from rainbowio import colorwheel
import neopixel
import usb_hid
from adafruit_hid.keyboard import Keyboard, Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode


kbd = Keyboard(usb_hid.devices)
cc = ConsumerControl(usb_hid.devices)

encoder = rotaryio.IncrementalEncoder(board.D9, board.D10)
last_position = encoder.position

pixel_pin = board.D2
num_pixels = 4

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.5, auto_write=False)


last_led_rainbow_time = time.monotonic() 
current_led_color_pos = 0
rainbow_cycle_speed = 0.5 ## Speed: 0 < s <= 1

def rainbow_cycle(led_loop_pos):
    a = math.floor(led_loop_pos * rainbow_cycle_speed) % 255
    for i in range(num_pixels):
        rc_index = (i * 256 // num_pixels) + a
        pixels[i] = colorwheel(rc_index & 255)
    pixels.show()


last_key_press_time = [time.monotonic(),time.monotonic(),time.monotonic(),time.monotonic()]
keySwitchLEDTimeout = [0,0,0,0]
KeySwitchPins = [board.D8, board.D3, board.D1, board.D4] # Up Down Left Right 
keySwitchKeyCode = [Keycode.UP_ARROW, Keycode.DOWN_ARROW, Keycode.LEFT_ARROW, Keycode.RIGHT_ARROW]
LED_index = [3, 1, 0, 2] # Up Down Left Right\
KeySwitchIOs = []
for key in KeySwitchPins:
    thisSwitch = digitalio.DigitalInOut(key)
    thisSwitch.pull = digitalio.Pull.UP
    KeySwitchIOs.append(thisSwitch)

while True:
    
    current_time = time.monotonic()

    rainbow_cycle(current_led_color_pos)
    current_led_color_pos = (current_led_color_pos + 1) % math.floor(256 / rainbow_cycle_speed)
    
    for index in range(0,3):
        if (current_time - last_key_press_time[index]) > 0.2:
            last_key_press_time[index] = current_time
            if KeySwitchIOs[index].value is False:
                pixels[LED_index[index]] = (255,255,255)
                pixels.show()
                kbd.press(keySwitchKeyCode[index])
                kbd.release_all()
    
    current_position = encoder.position
    position_change = current_position - last_position
    if position_change > 0:
        for _ in range(position_change):
            cc.send(ConsumerControlCode.VOLUME_INCREMENT)
    elif position_change < 0:
        for _ in range(-position_change):
            cc.send(ConsumerControlCode.VOLUME_DECREMENT)
    last_position = current_position
