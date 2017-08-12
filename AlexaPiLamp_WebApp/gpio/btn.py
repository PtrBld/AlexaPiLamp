import RPi.GPIO as GPIO

from audio import alarm
from ledstrip import apa102
GPIO.setmode(GPIO.BCM)

def init(btn_pin):
    #TODO right method?
    GPIO.clear_all()
    GPIO.setup(btn_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(btn_pin, GPIO.FALLING, callback=btn_click, bouncetime=2000)

def btn_click():
    if alarm.is_running():
        alarm.turn_off()
    else:
        apa102.toggle_lights()