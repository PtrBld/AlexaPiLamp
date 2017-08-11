import json
import datetime
from helpers import colors
import requests
from flask import Flask, render_template, request
import urllib.parse

from audio import alarm
from gpio import btn
from ledstrip import apa102

app = Flask(__name__, template_folder="./templates",
        static_url_path="/static",
        static_folder="./static")

#helper methods


# routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/togglelight', methods=['POST'])
def set_light_color():
    apa102.toggle_lights()
    return json.dumps({'status':'OK'})

@app.route('/setlightcolor', methods=['POST'])
def set_light_color():
    apa102.set_color(colors.getIfromRGB(tuple(request.json)))
    return json.dumps({'status':'OK'})

@app.route('/setbrightness', methods=['POST'])
def set_light_color():
    apa102.set_brightness(request.json)
    return json.dumps({'status':'OK'})

@app.route('/setalarm', methods=['POST'])
def set_light_color():
    alarm.set_alarm(request.json)
    return json.dumps({'status':'OK'})

if __name__ == "__main__":
    btn_pin = 18
    num_led = 430
    btn.init(btn_pin)
    apa102.init(num_led)
    app.run()