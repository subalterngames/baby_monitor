from datetime import datetime
from base64 import b64decode
from time import sleep
import numpy as np
from requests import get
from requests.exceptions import ConnectionError
import pygame
import pygame.mixer
from baby_monitor.paths import FONT_PATH, IMAGES_DIRECTORY, AUDIO_DIRECTORY


class Listener:
    """
    Listen to the baby monitor. Show the webcam. Ping the user ("ding") when there is movement.
    """

    def __init__(self, framerate: float = 0.5, url: str = "http://127.0.0.1:5000/get"):
        """
        :param framerate: Sleep this many seconds between frames.
        :param url: The **local** address and port of the monitor, e.g. `"http://10.0.0.62:42069/get"`.
        """

        self._framerate: float = framerate
        self._url: str = url
        self._movement: bool = False

    def run(self) -> None:
        # Initialize the window.
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
        # Get the light surfaces.
        light_position = (display_size[0] - text_size[0] - 16 + 20,
                          display_size[1] - text_size[1] - 16 - 80)
        lit = pygame.image.load(str(IMAGES_DIRECTORY.joinpath("lit.png"))).convert()
        unlit = pygame.image.load(str(IMAGES_DIRECTORY.joinpath("unlit.png"))).convert()
        movement_time = "Never"
        while True:
            # Quit when the user presses the Escape key.
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if pygame.key.name(event.key) == "escape":
                        exit()
            try:
                # Redraw the screen.
                pygame.display.get_surface().fill((255, 255, 255))
                pygame.display.get_surface().blit(text_surface, (display_size[0] - text_size[0] - 16,
                                                                 display_size[1] - text_size[1] - 16))
                # Get data from the monitor.
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
                        movement_time = datetime.today().strftime("%H:%M:%S")
                        # Ding!
                        if not self._movement:
                            sound.play()
                        self._movement = True
                    # Show the unlit light.
                    else:
                        pygame.display.get_surface().blit(unlit, light_position)
                        self._movement = False
                    move_time_surface = font.render(f"Last movement: {movement_time}", True, (0, 0, 0), (255, 255, 255))
                    pygame.display.get_surface().blit(move_time_surface, (16, display_size[1] - text_size[1] - 16))
                    pygame.display.flip()
            except ConnectionError:
                pass
            # Wait.
            sleep(self._framerate)
