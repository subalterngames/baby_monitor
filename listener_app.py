from argparse import ArgumentParser
from baby_monitor.listener import Listener


"""
Launch the listener application.
"""

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--address", type=str)
    parser.add_argument("--port", type=int, default=42069)
    parser.add_argument("--audio_device", type=str)
    args = parser.parse_args()
    listener = Listener(url=f"http://{args.address}:{args.port}/get", audio_device=args.audio_device)
    listener.run()
