from threading import Thread
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
    Thread(target=lambda: app.run()).start()
    m.run()
