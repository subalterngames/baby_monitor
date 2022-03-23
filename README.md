# Baby Monitor

A baby monitor and listener. Run the monitor script on a computer with a webcam in the room you want to listen to. Run the listener app on another computer.

This program "listens" to motion on the webcam. Every half-second, it will capture an image and compare if to the previous image. If there is a big difference, then there was movement.

## Why I use this program

- I have a mischievous puppy. 

## Why you should use this program

- This is not smart technology. It doesn't use server that is records your house and reports to Google/Amazon/etc. everything that you do. This program works strictly on your local WiFi or LAN network and doesn't save anything or upload anything to the cloud.
- This program is simple and portable (assuming that you know how to run Python programs). It will run on just about any machine from the past 15 years.

## Why you shouldn't use this program

- If you're not on the same network (for example, if the monitor is at home and you are at an office), this program won't work.
- If you want to listen to audio; this program doesn't listen to the monitor computer's microphone.

## Requirements

- A monitoring computer:
  - Windows, OS X, or Linux
  - Python 3.6+
  - A webcam
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

The listener app connects to `monitor_app.py`. It will show images from the webcam. If there is movement, a green circle will light up and play a "ding" sound. Press the Escape key to close the app.

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
- [Ding sound](https://opengameart.org/content/completion-sound) by Brandon Morris