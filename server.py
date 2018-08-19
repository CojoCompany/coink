from io import BytesIO
import json

from flask import Flask
from flask import render_template
from flask import request
from flask import send_file
import matplotlib

from analysis import normalize
from analysis import raw_to_dataframe


matplotlib.use('svg')

server = Flask(__name__)
last_curve = None


@server.route("/", methods=['GET','POST'])
def addr_handler():
    return 'Hello ESP8266, from Flask'


@server.route('/whatesp', methods=['POST'])
def esp_handler():
    raw = request.get_data()
    df = raw_to_dataframe(raw)
    last_curve = df
    return 'ok'


@server.route('/curve.svg')
def curve():
    df = normalize(last_curve)
    figure = df.plot().get_figure()
    img = BytesIO()
    figure.savefig(img)
    img.seek(0)
    return send_file(img, mimetype='image/svg+xml')


@server.route('/result', methods=['GET'])
def result():
    if last_curve is None:
        return 'No data received'
    return render_template('result.html')


config = json.load(open('config.json'))
x = config['server']
server.run(host=x['host'],port=int(x['port']))
