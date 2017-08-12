import json
import datetime
from helpers import colors
import requests
from flask import Flask, render_template, request
import urllib.parse
from threading import Thread

from display import disp7seg
from audio import alarm
from gpio import btn
from ledstrip import apa102

app = Flask(__name__, template_folder="./templates",
        static_url_path="/static",
        static_folder="./static")

running_threads = []
#helper methods

# routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/startclock')
def start_clock():
    thread = Thread(target=disp7seg.start)
    thread.start()
    running_threads.append(thread)
    return json.dumps({'status':'OK'})

@app.route('/togglelight', methods=['POST'])
def toggle_light():
    thread = Thread(target=apa102.toggle_lights)
    thread.start()
    running_threads.append(thread)
    return json.dumps({'status':'OK'})\

@app.route('/setlightcolor', methods=['POST'])
def set_light_color():
    thread = Thread(target=apa102.set_color, args=[colors.getIfromRGB(tuple(request.json))])
    thread.start()
    running_threads.append(thread)
    return json.dumps({'status':'OK'})

@app.route('/setbrightness', methods=['POST'])
def set_brightness():
    thread = Thread(target=apa102.set_brightness, args=[int(request.json)])
    thread.start()
    running_threads.append(thread)
    return json.dumps({'status':'OK'})

@app.route('/setalarm', methods=['POST'])
def set_alarm():
    thread = Thread(target=apa102.set_alarm, args=[str(request.json)])
    thread.start()
    running_threads.append(thread)
    return json.dumps({'status':'OK'})

if __name__ == "__main__":
    btn_pin = 18
    num_led = 430
    btn.init(btn_pin)
    apa102.init(num_led)
    disp7seg.init()
    app.run()