"""The module contains templates for colour cycles"""
import time

from ledstrip.apalib import apa102_lib
from threading import Thread


class ColorCycleTemplate:
    """This class is the basis of all color cycles.

    A specific color cycle must subclass this template, and implement at least the
    'update' method.
    """
    def __init__(self, num_led, pause_value = 0, num_steps_per_cycle = 100,
                 num_cycles = -1, global_brightness = 255, order = 'rbg', color = 0xFFFFFF, brightness = 5):
        self.num_led = num_led # The number of LEDs in the strip
        self.pause_value = pause_value # How long to pause between two runs
        self.num_steps_per_cycle = num_steps_per_cycle # Steps in one cycle.
        self.num_cycles = num_cycles # How many times will the program run
        self.global_brightness = global_brightness # Brightness of the strip
        self.order = order # Strip colour ordering
        self.color = color # Strip colour ordering
        self.brightness = brightness # Strip colour ordering
        self.light_is_on = True

    def init(self, strip, num_led):
        """This method is called to initialize a color program.

        The default does nothing. A particular subclass could setup
        variables, or even light the strip in an initial color.
        """
        pass

    def shutdown(self, strip, num_led):
        """This method is called before exiting.

        The default does nothing
        """
        pass

    def update(self, strip, num_led, num_steps_per_cycle, current_step,
               current_cycle):
        """This method paints one subcycle. It must be implemented.

        current_step:  This goes from zero to numStepsPerCycle-1, and then
          back to zero. It is up to the subclass to define what is done in
          one cycle. One cycle could be one pass through the rainbow.
          Or it could be one pixel wandering through the entire strip
          (so for this case, the numStepsPerCycle should be equal to numLEDs).
        current_cycle: Starts with zero, and goes up by one whenever a full
          cycle has completed.
        """

        raise NotImplementedError("Please implement the update() method")

    def cleanup(self, strip):
        """Cleanup method."""
        self.shutdown(strip, self.num_led)
        strip.clear_strip()
        strip.cleanup()

    def clean(self):
        """Cleanup method."""
        global strip
        self.shutdown(strip, self.num_led)
        strip.clear_strip()
        strip.cleanup()


    def start(self):
        """This method does the actual work."""
        global strip
        strip = apa102_lib.APA102(num_led=self.num_led,
                              global_brightness=self.global_brightness,
                              order=self.order) # Initialize the strip
        strip.clear_strip()
        self.init(strip, self.num_led) # Call the subclasses init method
        strip.show()
        current_cycle = 0
        while self.light_is_on:  # Loop forever
            for current_step in range (self.num_steps_per_cycle):
                need_repaint = self.update(strip, self.num_led,
                                           self.num_steps_per_cycle,
                                           current_step, current_cycle)
                if need_repaint:
                    strip.show() # repaint if required
                time.sleep(self.pause_value) # Pause until the next step
            current_cycle += 1
            if self.num_cycles != -1 and current_cycle >= self.num_cycles:
                break