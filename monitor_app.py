from threading import Thread
from flask import Flask
from flask import jsonify
from baby_monitor.monitor import Monitor

app = Flask(__name__)
m = Monitor()


@app.route('/get')
def get():
    return jsonify({"visual": m.visual,
                    "audio": m.audio})


if __name__ == "__main__":
    Thread(target=lambda: app.run()).start()
    m.run()
