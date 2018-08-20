from datetime import datetime
from io import BytesIO
import json

from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request
from flask import send_file
import matplotlib

from analysis import classify_coin
from analysis import normalize
from analysis import raw_to_dataframe


matplotlib.use('svg')
from matplotlib import pyplot
matplotlib.pyplot.style.use('seaborn')

server = Flask(__name__)
last_coin = {}
last_coin['curve'] = None
last_coin['coin'] = 'unknown'
last_coin['datetime'] = datetime.today().isoformat()


@server.route("/", methods=['GET'])
def view():
    return render_template('view.html')


@server.route('/analyze', methods=['POST'])
def analyze():
    raw = request.get_data()
    curve = raw_to_dataframe(raw)
    last_coin['curve'] = curve
    last_coin['datetime'] = datetime.today().isoformat()
    coin = classify_coin(curve)
    last_coin['coin'] = coin
    if last_coin['coin'] == -1:
        last_coin['coin'] = 'unknown'
    return 'ok'


@server.route('/curve')
def curve():
    if last_coin['curve'] is None:
        return send_file('static/insert_coin.svg', mimetype='image/svg+xml')
    df = normalize(last_coin['curve'])
    figure = df.plot().get_figure()
    img = BytesIO()
    figure.savefig(img)
    img.seek(0)
    return send_file(img, mimetype='image/svg+xml')


@server.route('/result', methods=['GET'])
def result():
    return jsonify(coin=last_coin['coin'], datetime=last_coin['datetime'])


config = json.load(open('config.json'))
x = config['server']
server.run(host=x['host'],port=int(x['port']))
