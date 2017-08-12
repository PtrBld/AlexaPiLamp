#!/usr/bin/python

import time, datetime
from time import strftime, gmtime
from Adafruit_LED_Backpack import SevenSegment
import urllib.request
import json

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

def init():
	_display = SevenSegment.SevenSegment()
	_clock_running = False
	
def start():
	if _display is None:
		return
	_display.begin()
	loading()
	_clock_running = True
	while _clock_running:
		clock()
		weather()
		
def end():
	_clock_running = False
	_display.clear()

def loading():
	panel = 1
	_display.clear()

	for y in range(0, 16):
		for x in range(0,4):
			_display.set_digit_raw(x, panel)
		try: 
			_display.write_display()
		except:
			print("Write error")
			pass

		panel = panel * 2
		if panel > 32:
			panel = 1

		time.sleep(0.05)
	
def clock():
	_display.clear()
	colon = True
	for x in range(0,10):
		_display.set_colon(colon)
		t = float(strftime("%H.%M"))
		dt = datetime.datetime.now()

		_display.print_float(t)
		try: 
			if dt.hour > 8:
				_display.set_brightness(8)
			elif dt.hour > 20:
				_display.set_brightness(4)
			_display.write_display()
		except:
			print("Write error")
			pass

		colon = not colon
		time.sleep(1)

def weather():
	_display.clear()
	loop = True
	try:
		response = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?id=2954172&appid=ce55bc97088a050b871d39dbc8199de1&units=metric')
		data = json.load(response)
		t = str(int(round(data['main']['temp'])))

		for x in range (0, 5):
			try:			
				if len(t) <= 1:
					_display.set_digit_raw(1, DIGIT_VALUES.get(str(t[0]).upper(), 0x00))
				else:
					_display.set_digit_raw(0, DIGIT_VALUES.get(str(t[0]).upper(), 0x00))
					_display.set_digit_raw(1, DIGIT_VALUES.get(str(t[1]).upper(), 0x00))
				_display.set_digit_raw(2, 0x63)
				_display.set_digit_raw(3, 0x39)
				_display.write_display()
			except:
				print("Write error")
			time.sleep(1)
	except:
		print("URL error")
		pass


