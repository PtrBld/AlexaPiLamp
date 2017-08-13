#!/usr/bin/python

import time, datetime
from threading import Thread
from time import strftime, gmtime
from Adafruit_LED_Backpack import SevenSegment
import urllib.request
import json


class DisplayThread(Thread):
    _display = None
    DIGIT_VALUES = {
        ' ': 0x00,
        '-': 0x40,
        '0': 0x3F,
        '1': 0x06,
        '2': 0x5B,
        '3': 0x4F,
        '4': 0x66,
        '5': 0x6D,
        '6': 0x7D,
        '7': 0x07,
        '8': 0x7F,
        '9': 0x6F,
        'A': 0x77,
        'B': 0x7C,
        'C': 0x39,
        'D': 0x5E,
        'E': 0x79,
        'F': 0x71
    }

    def __init__(self):
        Thread.__init__(self)
        self._display = SevenSegment.SevenSegment()
        self._clock_running = False
        self._display.begin()
        self.loading()

    def run(self):
        self._clock_running = True
        # TODO introduce mode for alarm
        while True:
            if self._clock_running:
                self.clock()
                self.weather()

    def end(self):
        self._clock_running = False
        self._display.clear()

    def loading(self):
        panel = 1
        self._display.clear()

        for y in range(0, 16):
            for x in range(0, 4):
                self._display.set_digit_raw(x, panel)
            try:
                self._display.write_display()
            except:
                print("Write error")
                pass

            panel = panel * 2
            if panel > 32:
                panel = 1

            time.sleep(0.05)

    def clock(self):
        self._display.clear()
        colon = True
        for x in range(0, 10):
            self._display.set_colon(colon)
            t = float(strftime("%H.%M"))
            dt = datetime.datetime.now()

            self._display.print_float(t)
            try:
                if dt.hour > 8:
                    self._display.set_brightness(8)
                elif dt.hour > 20:
                    self._display.set_brightness(4)
                self._display.write_display()
            except:
                print("Write error")
                pass

            colon = not colon
            time.sleep(1)

    def weather(self):
        self._display.clear()
        try:
            response = urllib.request.urlopen(
                'http://api.openweathermap.org/data/2.5/weather?id=2954172&appid=ce55bc97088a050b871d39dbc8199de1&units=metric')
            str_response = response.read(response.length).decode('utf-8')
            data = json.loads(str_response)
            t = str(int(round(data['main']['temp'])))

            for x in range(0, 5):
                try:
                    if len(t) <= 1:
                        self._display.set_digit_raw(1, self.DIGIT_VALUES.get(str(t[0]).upper(), 0x00))
                    else:
                        self._display.set_digit_raw(0, self.DIGIT_VALUES.get(str(t[0]).upper(), 0x00))
                        self._display.set_digit_raw(1, self.DIGIT_VALUES.get(str(t[1]).upper(), 0x00))
                    self._display.set_digit_raw(2, 0x63)
                    self._display.set_digit_raw(3, 0x39)
                    self._display.write_display()
                except:
                    print("Write error")
                time.sleep(1)
        except:
            print("URL error")
            pass
