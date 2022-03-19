from time import sleep
from requests import get
from requests.exceptions import ConnectionError


class ListenerApp:
    def __init__(self, framerate: float = 0.5, url: str = "http://127.0.0.1:5000/get"):
        self._framerate: float = framerate
        self._url: str = url
        self.audio: bool = False
        self.visual: bool = False

    def run(self) -> None:
        while True:
            try:
                resp = get(self._url)
                if resp.status_code == 200:
                    print(resp.json())
            except ConnectionError:
                pass
            sleep(self._framerate)


if __name__ == "__main__":
    ListenerApp().run()
