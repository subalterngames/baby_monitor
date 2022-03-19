from time import sleep
import numpy as np
import pygame.camera
import pygame.mixer
from PIL import Image, ImageChops
import pyaudio
import audioop


class Monitor:
    CHUNK = 1024 * 4
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100

    def __init__(self, camera_name: str = None, framerate: float = 0.5, visual_threshold: float = 10,
                 audio_threshold: float = 80):
        pygame.camera.init(pygame.camera.get_backends()[0])
        camera_names = pygame.camera.list_cameras()
        if camera_name is None:
            camera_name = camera_names[0]
        else:
            assert camera_name in camera_names, f"Camera {camera_name} not found"
        # Get the camera.
        self._camera = pygame.camera.Camera(camera_names[camera_names.index(camera_name)])
        self._framerate: float = framerate
        self._visual_threshold: float = visual_threshold
        self._audio_threshold: float = audio_threshold
        self.visual: bool = False
        self.audio: bool = False

    def run(self) -> None:
        # Initialize audio capture.
        # Source: https://stackoverflow.com/a/26579447
        p = pyaudio.PyAudio()
        stream = p.open(format=Monitor.FORMAT,
                        channels=Monitor.CHANNELS,
                        rate=Monitor.RATE,
                        input=True,
                        frames_per_buffer=Monitor.CHUNK)
        audio_data = stream.read(Monitor.CHUNK)
        previous_volume = audioop.rms(audio_data, 2)
        self._camera.start()
        done = False
        # Check deltas.
        camera_size = self._camera.get_size()
        previous_arr = np.zeros(shape=(camera_size[0], camera_size[1], 3), dtype=np.uint8)
        try:
            while not done:
                try:
                    # Get an image from the camera and convert it to a numpy array.
                    arr = pygame.surfarray.array3d(self._camera.get_image())
                    # Convert the numpy arrays to images, get the difference, and get the mean of the difference.
                    q = np.mean(np.array(ImageChops.difference(Image.fromarray(previous_arr), Image.fromarray(arr))))
                    self.visual = bool(q > self._visual_threshold)
                    # Set the previous frame as this frame.
                    previous_arr = arr.copy()
                    # Listen to audio.
                    audio_data = stream.read(Monitor.CHUNK)
                    volume = audioop.rms(audio_data, 2)
                    self.audio = bool(np.linalg.norm(volume - previous_volume) > self._audio_threshold)
                    previous_volume = volume
                    # Wait.
                    sleep(self._framerate)
                except KeyboardInterrupt:
                    done = True
        finally:
            self._camera.stop()


if __name__ == "__main__":
    m = Monitor()
    m.run()
