from ledstrip.apalib import apa102_lib
from ledstrip.apalib import colorschemes, colorcycletemplate
from threading import Thread
_color = 0xFFFFFF
_brightness = 5
_my_cycle = None
_num_led = 0

def init(num_led):
    global _num_led
    _num_led = num_led

def is_on():
    return  colorcycletemplate.light_is_on

def toggle_lights():
    if(is_on()):
        turn_all_lights_off()
    else:
        turn_all_lights_on()

def turn_all_lights_off():
    global _my_cycle
    colorcycletemplate.light_is_on = False
    _my_cycle.cleanup()

def turn_all_lights_on():
    global _my_cycle
    colorcycletemplate.light_is_on = True
    _my_cycle = colorschemes.Solid(num_led=_num_led,color=_color,brightness=_brightness)
    _my_cycle.start()

def set_brightness(brightness):
    global _brightness
    _brightness = brightness

def set_color(light_rgb):
    global _color
    _color = light_rgb