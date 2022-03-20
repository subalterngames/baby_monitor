from base64 import b64decode
from time import sleep
import numpy as np
from requests import get
from requests.exceptions import ConnectionError
import pygame
import pygame.mixer
from baby_monitor.paths import FONT_PATH, IMAGES_DIRECTORY, AUDIO_DIRECTORY
from procemon_rpg.commands.add_text import AddText


class Listener:
    def __init__(self, framerate: float = 0.5, url: str = "http://127.0.0.1:5000/get"):
        self._framerate: float = framerate
        self._url: str = url
        self.movement: bool = False

    def run(self) -> None:
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Baby Listener")
        pygame.display.get_surface().fill((255, 255, 255))
        # Get the sound.
        sound = pygame.mixer.Sound(str(AUDIO_DIRECTORY.joinpath("gmae.wav").resolve()))
        # Print some text.
        font = pygame.font.Font(str(FONT_PATH.resolve()), 24)
        text_surface = font.render("Movement", True, (0, 0, 0), (255, 255, 255))
        text_size = text_surface.get_size()
        display_size = pygame.display.get_surface().get_size()
        pygame.display.get_surface().blit(text_surface, (display_size[0] - text_size[0] - 16,
                                                         display_size[1] - text_size[1] - 16))
        light_position = (display_size[0] - text_size[0] - 16 + 20,
                          display_size[1] - text_size[1] - 16 - 80)
        lit = pygame.image.load(str(IMAGES_DIRECTORY.joinpath("lit.png"))).convert()
        unlit = pygame.image.load(str(IMAGES_DIRECTORY.joinpath("unlit.png"))).convert()
        while True:
            try:
                resp = get(self._url)
                if resp.status_code == 200:
                    js = resp.json()
                    # Show the camera image.
                    image_bytes = b64decode(js["image"])
                    image_arr = np.frombuffer(image_bytes, dtype=np.uint8)
                    image_arr = np.reshape(image_arr, (js["size"][0], js["size"][1], 3))
                    image = pygame.surfarray.make_surface(image_arr)
                    pygame.display.get_surface().blit(image, (16, 16))
                    # Show the light.
                    if js["movement"]:
                        pygame.display.get_surface().blit(lit, light_position)
                        # Ding!
                        if not self.movement:
                            sound.play()
                        self.movement = True
                    else:
                        pygame.display.get_surface().blit(unlit, light_position)
                        self.movement = False
                    pygame.display.flip()
            except ConnectionError:
                pass
            sleep(self._framerate)


if __name__ == "__main__":
    Listener().run()
