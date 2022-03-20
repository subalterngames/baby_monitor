from typing import Tuple
from time import sleep
from base64 import b64encode, b64decode
import numpy as np
import pygame.camera
from PIL import Image, ImageChops


class Monitor:
    def __init__(self, camera_name: str = None, framerate: float = 0.5, movement_threshold: float = 10):
        pygame.camera.init(pygame.camera.get_backends()[0])
        camera_names = pygame.camera.list_cameras()
        if camera_name is None:
            camera_name = camera_names[0]
        else:
            assert camera_name in camera_names, f"Camera {camera_name} not found"
        # Get the camera.
        self._camera = pygame.camera.Camera(camera_names[camera_names.index(camera_name)])
        self._framerate: float = framerate
        self._movement_threshold: float = movement_threshold
        self.movement: bool = False
        self.image: str = ""
        self.camera_size: Tuple[int, int] = (0, 0)

    def run(self) -> None:
        self._camera.start()
        done = False
        # Check deltas.
        self.camera_size = self._camera.get_size()
        previous_arr = np.zeros(shape=(self.camera_size[0], self.camera_size[1], 3), dtype=np.uint8)
        try:
            while not done:
                try:
                    # Get an image from the camera.
                    surface = self._camera.get_image()
                    # Convert the surface to a numpy array.
                    arr = pygame.surfarray.array3d(surface)
                    # Save the image as a string.
                    self.image = b64encode(arr).decode("utf-8")
                    # Convert the numpy arrays to images, get the difference, and get the mean of the difference.
                    q = np.mean(np.array(ImageChops.difference(Image.fromarray(previous_arr), Image.fromarray(arr))))
                    self.movement = bool(q > self._movement_threshold)
                    # Set the previous frame as this frame.
                    previous_arr = arr.copy()
                    # Wait.
                    sleep(self._framerate)
                except KeyboardInterrupt:
                    done = True
        finally:
            self._camera.stop()


if __name__ == "__main__":
    m = Monitor()
    m.run()
