import json

from flask import Flask, request

from analysis import normalize
from analysis import raw_to_dataframe


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


@server.route('/result', methods=['GET'])
def result():
    if last_curve is None:
        return 'No data received'
    df = normalize(last_curve)
    return str(df)


config = json.load(open('config.json'))
x = config['server']
server.run(host=x['host'],port=int(x['port']))
