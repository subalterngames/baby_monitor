from typing import Tuple
from base64 import b64encode
import pygame.camera
import pyaudio


class Monitor:
    """
    Watch for movement using a webcam.
    """

    def __init__(self, camera_name: str = None, framerate: float = 0.5, audio_chunk: int = 64, camera_scale: float = 0.5):
        """
        :param camera_name: The expected name of the webcam. If None, defaults to the first camera.
        :param framerate: Seconds per image capture.
        :param image_scale: Scale the image by this factor.
        """

        # Initialize the camera.
        pygame.camera.init(pygame.camera.get_backends()[0])
        camera_names = pygame.camera.list_cameras()
        if camera_name is None:
            camera_name = camera_names[0]
        else:
            assert camera_name in camera_names, f"Camera {camera_name} not found"
        # Get the camera.
        self._camera = pygame.camera.Camera(camera_names[camera_names.index(camera_name)])
        self._camera_scale: float = camera_scale
        self._framerate: float = framerate
        """:field
        The image from this frame encoded as a base64 string.
        """
        self.image: str = ""
        """:field
        The audio data from this frame encoded as a base64 string.
        """
        self.audio: str = ""
        """:field
        The camera pixel dimensions.
        """
        self.camera_size: Tuple[int, int] = (0, 0)
        self._audio_chunk: int = audio_chunk

    def run(self) -> None:
        # Turn on the camera.
        self._camera.start()
        # Start the audio stream.
        p = pyaudio.PyAudio()
        audio_stream = p.open(format=pyaudio.paInt16,
                              channels=2,
                              rate=44100,
                              input=True,
                              frames_per_buffer=self._audio_chunk)
        done = False
        # Check deltas.
        self.camera_size = self._camera.get_size()
        self.camera_size = (int(self.camera_size[0] * self._camera_scale), int(self.camera_size[1] * self._camera_scale))
        try:
            while not done:
                try:
                    # Get an image from the camera. Resize it. Convert the surface to a numpy array. Save the image as a string.
                    self.image = b64encode(pygame.surfarray.array3d(pygame.transform.scale(self._camera.get_image(),
                                                                                           self.camera_size))).decode("utf-8")
                    audio = b''
                    for i in range(0, int(44100 / self._audio_chunk * self._framerate)):
                        audio += audio_stream.read(self._audio_chunk)
                    self.audio = b64encode(audio).decode("utf-8")
                except KeyboardInterrupt:
                    done = True
        finally:
            self._camera.stop()
            audio_stream.stop_stream()
            audio_stream.close()
            p.terminate()
