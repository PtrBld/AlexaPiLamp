from ledstrip.apalib import apa102_lib
from ledstrip.apalib import colorschemes

_num_led = 0
_light_is_on = False
_color = 0xFFFFFF
_brightness = 5
_my_cycle = None


def init(num_led):
    _num_led = num_led

def is_on():
    return  _light_is_on

def toggle_lights():
    if(is_on):
        turn_all_lights_off()
    else:
        turn_all_lights_on()

def turn_all_lights_off():
    _light_is_on = False
    _my_cycle.cleanup()

def turn_all_lights_on():
    _light_is_on = True
    _my_cycle = colorschemes.Solid(num_led=_num_led,color=_color,brightness=_brightness)
    _my_cycle.start()

def set_brightness(brightness):
    _brightness = brightness

def set_color(light_rgb):
    _color = light_rgb