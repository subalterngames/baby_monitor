from datetime import datetime
from base64 import b64decode
from time import sleep
import audioop
import numpy as np
from PIL import Image, ImageChops
from requests import get
from requests.exceptions import ConnectionError
import pygame
import pygame.mixer
from baby_monitor.paths import FONT_PATH, IMAGES_DIRECTORY, AUDIO_DIRECTORY


class Listener:
    """
    Listen to the baby monitor. Show the webcam. Ping the user ("ding") when there is movement.
    """

    def __init__(self, framerate: float = 0.5, url: str = "http://127.0.0.1:5000/get", movement_threshold: float = 5,
                 audio_threshold: float = 100):
        """
        :param framerate: Sleep this many seconds between frames.
        :param url: The **local** address and port of the monitor, e.g. `"http://10.0.0.62:42069/get"`.
        :param movement_threshold: A scalar defining movement. A higher value means that more movement is ignored.
        :param audio_threshold: A scalar defining an audio threshold volume. Don't play audio below this.
        """

        self._framerate: float = framerate
        self._url: str = url
        self._movement_threshold: float = movement_threshold
        self._audio_threshold: float = audio_threshold
        self._previous_arr: np.array = np.zeros([0])
        self._has_previous_image: bool = False
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
        channel: pygame.mixer.Channel = pygame.mixer.find_channel()
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
                    image_arr = np.reshape(image_arr, (js["camera_size"][0], js["camera_size"][1], 3))
                    if self._has_previous_image:
                        # Convert the numpy arrays to images, get the difference, and get the mean of the difference.
                        q = np.mean(np.array(ImageChops.difference(Image.fromarray(self._previous_arr),
                                                                   Image.fromarray(image_arr))))
                        movement = bool(q > self._movement_threshold)
                        # Update the previous image.
                        self._previous_arr = image_arr.copy()
                    else:
                        self._has_previous_image = True
                        self._previous_arr = image_arr.copy()
                        movement = False
                    image = pygame.surfarray.make_surface(image_arr)
                    pygame.display.get_surface().blit(image, (16, 16))
                    # Show the light.
                    if movement:
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
                    audio = b64decode(js["audio"])
                    rms = audioop.rms(audio, 2)
                    if rms > self._audio_threshold:
                        # Queue up audio.
                        channel.play(pygame.mixer.Sound(audio))
            except ConnectionError:
                pass
            # Wait.
            sleep(self._framerate)
