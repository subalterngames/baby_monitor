# Baby Monitor

A simple baby monitor and listener.

# Requirements

- A monitoring computer:
  - Windows, OS X, or Linux
  - Python 3.6+
  - A webcam
- A listening computer:
  - Windows, OS X, or Linux
  - Python 3.6+
  - Optional: Audio output device (e.g. headphones)

# Setup:

**Follow these steps for BOTH the monitoring computer AND the listening computer.**

1. Clone this repo: `git clone https://github.com/subalterngames/baby_monitor`

## The listener app

Rung `listener_app.py` to launch an app that connects to `monitor_app.py`. It will show images from the webcam. If there is movement, a green circle will light up and play a "ding" sound.

### Usage

Windows:

```bash
python3 listener_app.py --address ADDRESS
```

OS X and Linux:

```bash
python3 listener_app.py --address ADDRESS
```

- `ADDRESS` is the local address of the monitor. `monitor_app.py` prints the address when it first launches.
- Optionally, you can add `--port PORT` but this is rarely needed.

# Credits

- [Raleway font](https://fonts.google.com/specimen/Raleway) Matt McInerney, Pablo Impallari, Rodrigo Fuenzalida
- [Ding sound](https://opengameart.org/content/completion-sound) by Brandon Morris