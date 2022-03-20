from threading import Thread
import logging
import socket
from flask import Flask
from flask import jsonify
from baby_monitor.monitor import Monitor

app = Flask(__name__)
m = Monitor()


@app.route('/get')
def get():
    return jsonify({"movement": m.movement,
                    "image": m.image,
                    "size": m.camera_size})


if __name__ == "__main__":
    # Print the local IP address. Source: https://www.delftstack.com/howto/python/get-ip-address-python/
    print("Address:", socket.gethostbyname(socket.gethostname()))
    # Disable most logging. Source: https://stackoverflow.com/a/18379764
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    Thread(target=lambda: app.run(host="0.0.0.0", port=42069, debug=False)).start()
    m.run()
