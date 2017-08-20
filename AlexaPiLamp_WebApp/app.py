import json
import datetime
from helpers import colors
import requests
from flask import Flask, render_template, request
import urllib.parse
from threading import Thread

app = Flask(__name__, template_folder="./templates",
            static_url_path="/static",
            static_folder="./static")


# routes
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/togglelight', methods=['POST'])
def toggle_light():
    res = requests.get("http://192.168.178.33:8080/apa102?sequence=toggle")
    print('response from server:', res.text)
    return json.dumps({'status': 'OK'})


@app.route('/setlightcolor', methods=['POST'])
def set_light_color():
    res = requests.get("http://192.168.178.33:8080/apa102?color=" + str(tuple(request.json)))
    print('response from server:', res.text)
    return json.dumps({'status': 'OK'})

@app.route('/setleds', methods=['POST'])
def set_leds():
    res = requests.get("http://192.168.178.33:8080/apa102?leds=" + str(int(request.json)))
    print('response from server:', res.text)
    return json.dumps({'status': 'OK'})

@app.route('/setmodus', methods=['POST'])
def set_modus():
    res = requests.get("http://192.168.178.33:8080/apa102?sequence=" + str(request.json))
    print('response from server:', res.text)
    return json.dumps({'status': 'OK'})

if __name__ == "__main__":
    # run flask app
    app.run(host='0.0.0.0', port=80)
