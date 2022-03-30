from argparse import ArgumentParser
from threading import Thread
import logging
import netifaces as ni
from flask import Flask
from flask import jsonify
from baby_monitor.monitor import Monitor

parser = ArgumentParser()
parser.add_argument("--audio_device", type=str)
args = parser.parse_args()
app = Flask(__name__)
m = Monitor(args.audio_device)


@app.route('/get')
def get():
    return jsonify({"audio": m.audio,
                    "image": m.image,
                    "camera_size": m.camera_size})


if __name__ == "__main__":
    # Print the local IP address. Source: https://stackoverflow.com/a/24196955
    print("Address:", ni.ifaddresses(ni.gateways()[ni.AF_INET][0][1])[ni.AF_INET][0]['addr'])
    # Disable most logging. Source: https://stackoverflow.com/a/18379764
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    Thread(target=lambda: app.run(host="0.0.0.0", port=42069, debug=False)).start()
    m.run()
