from time import sleep

from ledstrip.apalib import apa102_lib
from ledstrip.apalib import colorschemes, colorcycletemplate
from threading import Thread


class ApaStripThread(Thread):
    _color = 0xFFFFFF
    _brightness = 5
    _my_cycle = None
    _num_led = 0
    _modus = "solid"

    def __init__(self, num_led):
        Thread.__init__(self)
        self._num_led = num_led

    def run(self):
        pass

    def is_on(self):
        if self._my_cycle is None:
            return False
        return self._my_cycle.light_is_on

    def toggle_lights(self):
        if self.is_on():
            self.turn_all_lights_off()
        else:
            self.turn_all_lights_on()

    def turn_all_lights_off(self):
        self._my_cycle.light_is_on = False

    def turn_all_lights_on(self):
        if self._my_cycle is not None:
            self._my_cycle.light_is_on = False
        if self._modus == 'solid':
            self._my_cycle = colorschemes.Solid(num_led=self._num_led, color=self._color, brightness=self._brightness)
        if self._modus == 'rainbow':
            self._my_cycle = colorschemes.Rainbow(num_led=self._num_led, color=self._color, brightness=self._brightness)
        if self._modus == 'theaterCase':
            self._my_cycle = colorschemes.TheaterCase(num_led=self._num_led, color=self._color, brightness=self._brightness)
        if self._modus == 'roundAndRound':
            self._my_cycle = colorschemes.RoundAndRound(num_led=self._num_led, color=self._color, brightness=self._brightness)
        if self._modus == 'alexa':
            self._my_cycle = colorschemes.RoundAndRound(num_led=31, pause_value=0, num_steps_per_cycle=32)
        thread = Thread(target=self._my_cycle.start)
        thread.start()

    def set_modus(self, modus):
        self._modus = modus
        if self._my_cycle is not None and self._my_cycle.light_is_on:
            self.turn_all_lights_on()

    def set_brightness(self, brightness):
        self._brightness = brightness
        if self._my_cycle is not None and self._my_cycle.light_is_on:
            self.turn_all_lights_on()

    def set_color(self, light_rgb):
        self._color = light_rgb
        if self._my_cycle is not None and self._my_cycle.light_is_on:
            self.turn_all_lights_on()

    def set_leds(self, leds):
        self._num_led = leds
        if self._my_cycle is not None and self._my_cycle.light_is_on:
            self.turn_all_lights_on()
