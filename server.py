from flask import Flask, request
import json

server = Flask(__name__)


@server.route("/", methods=['GET','POST'])
def addr_handler():
    return 'Hello ESP8266, from Flask'


@server.route('/whatesp', methods=['POST'])
def esp_handler():
    with open('input_epb', 'w') as f:
        f.write(request.get_data().decode('ascii'))
    return 'ok'


config = json.load(open('config.json'))
x = config['server']
server.run(host=x['host'],port=int(x['port']))
