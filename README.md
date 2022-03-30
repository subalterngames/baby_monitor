# Baby Monitor

A baby monitor and listener. Run the monitor script on a computer with a webcam in the room you want to listen to. Run the listener app on another computer.

This program "listens" to motion on the webcam. Every half-second, it will capture an image and compare if to the previous image. If there is a big difference, then there was movement.

I made this program because I have a mischievous puppy named Bruce.

![](bruce.jpg)

## Why you should use this program

**This is not a smart (surveillance) app.** It doesn't connect to a remote server that sells information about you and your house to whomever. This program works strictly on your local WiFi or LAN network and doesn't save anything or upload anything to the cloud.

## Why you shouldn't use this program

If you're not on the same network (for example, if the monitor is at home and you are at an office), this program won't work.

## Requirements

- A monitoring computer:
  - Windows, OS X, or Linux
  - Python 3.6+
  - A webcam + microphone
- A listening computer:
  - Windows, OS X, or Linux
  - Python 3.6+
  - Optional: Audio output device (e.g. headphones)

## Setup

**Follow these steps for BOTH the monitoring computer AND the listening computer.**

1. Clone this repo: `git clone https://github.com/subalterngames/baby_monitor`
2. `cd baby_monitor`
3. `pip3 install -e .` Windows users may need to add `--user` at the end. OS X and Linux users may need to add `sudo` at the beginning.

## Run the monitor app

Run `monitor_app.py` on the computer with the webcam. It will print its local IP address, which the listener app will connect to (see below).

Windows:

```bash
python3 monitor_app.py
```

OS X and Linux:

```bash
python3 monitor_app.py
```

## Run the listener app

The listener app connects to `monitor_app.py`. It will show images from the webcam and play audio. If there is movement, a green circle will light up. Press the Escape key to close the app.

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

## Credits

- [Raleway font](https://fonts.google.com/specimen/Raleway) Matt McInerney, Pablo Impallari, Rodrigo Fuenzalida

## Changelog

### 1.1.0

- Added audio input (microphone) data.
- Moved movement detection from `monitor.py` to `listener.py`
- Removed "ding" sound effect.