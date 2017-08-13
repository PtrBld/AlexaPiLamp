import json
import datetime
from helpers import colors
import requests
from flask import Flask, render_template, request
import urllib.parse
from threading import Thread

from display.disp7seg import DisplayThread
from audio.alarm import AlarmThread
from gpio.btn import ButtonThread
from ledstrip.apa102 import ApaStripThread

app = Flask(__name__, template_folder="./templates",
            static_url_path="/static",
            static_folder="./static")


# routes
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/togglelight', methods=['POST'])
def toggle_light():
    _apa_strip.toggle_lights()
    return json.dumps({'status': 'OK'})


@app.route('/setlightcolor', methods=['POST'])
def set_light_color():
    _apa_strip.set_color(colors.getIfromRGB(tuple(request.json)))
    return json.dumps({'status': 'OK'})


@app.route('/setbrightness', methods=['POST'])
def set_brightness():
    _apa_strip.set_brightness(int(request.json))
    return json.dumps({'status': 'OK'})


@app.route('/setleds', methods=['POST'])
def set_leds():
    _apa_strip.set_leds(int(request.json))
    return json.dumps({'status': 'OK'})

@app.route('/setmodus', methods=['POST'])
def set_modus():
    _apa_strip.set_modus(str(request.json))
    return json.dumps({'status': 'OK'})


@app.route('/setalarm', methods=['POST'])
def set_alarm():
    _alarm.set_alarm(str(request.json))
    return json.dumps({'status': 'OK'})


_display = DisplayThread()
_button = ButtonThread(17)
_apa_strip = ApaStripThread(430)
_alarm = AlarmThread()

if __name__ == "__main__":
    # instantiate modules
    _display.start()
    _button.start()
    _apa_strip.start()
    _alarm.start()
    # run flask app
    app.run()
