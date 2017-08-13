import RPi.GPIO as GPIO

from audio import alarm
from ledstrip import apa102
from threading import Thread


def btn_click():
    if alarm.is_running():
        alarm.turn_off()
    else:
        apa102.toggle_lights()

class ButtonThread(Thread):

    def __init__(self,btn_pin):
        Thread.__init__(self)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(btn_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(btn_pin, GPIO.FALLING, callback=btn_click, bouncetime=2000)

    def run(self):
        while True:
            continue

