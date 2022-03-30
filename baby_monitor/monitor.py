from typing import Tuple, Optional
from base64 import b64encode
import pygame.camera
import sounddevice as sd


class Monitor:
    """
    Watch for movement using a webcam.
    """

    def __init__(self, audio_device: str, camera_name: str = None, camera_scale: float = 0.5, framerate: float = 0.5,
                 audio_chunk: int = 64):
        """
        :param camera_name: The expected name of the webcam. If None, defaults to the first camera.
        :param framerate: Seconds per image capture.
        :param camera_scale: Scale the image by this factor.
        :param audio_chunk: The size of the audio chunk. A lower value is lower-quality audio. The default is low-quality (1024 is more typical).
        :param audio_device: The name of the input audio device.
        """

        self._camera_name: Optional[str] = camera_name
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
        The shape of the audio array.
        """
        self.audio_shape: Tuple[int, int] = (0, 0)
        """:field
        The camera pixel dimensions.
        """
        self.camera_size: Tuple[int, int] = (0, 0)
        """:field
        Resive the camera image by this factor.
        """
        self.camera_scale: float = camera_scale
        sd.default.device = (audio_device, None)
        self._audio_chunk: int = audio_chunk

    def run(self) -> None:
        # Initialize the camera.
        pygame.camera.init(pygame.camera.get_backends()[0])
        camera_names = pygame.camera.list_cameras()
        if self._camera_name is None:
            self._camera_name = camera_names[0]
        else:
            assert self._camera_name in camera_names, f"Camera {self._camera_name} not found"
        # Get the camera.
        camera = pygame.camera.Camera(camera_names[camera_names.index(self._camera_name)])
        # Turn on the camera.
        camera.start()
        done = False
        # Check deltas.
        self.camera_size = camera.get_size()
        self.camera_size = (int(self.camera_size[0] * self.camera_scale), int(self.camera_size[1] * self.camera_scale))
        try:
            while not done:
                try:
                    # Get an image from the camera. Resize it. Convert the surface to a numpy array. Save the image as a string.
                    self.image = b64encode(pygame.surfarray.array3d(pygame.transform.scale(camera.get_image(),
                                                                                           self.camera_size))).decode("utf-8")
                    # Get a chunk of audio.
                    audio_arr = sd.rec(frames=int(44100 * self._framerate), samplerate=44100, channels=2, blocking=True)
                    # Encode the audio chunk.
                    self.audio = b64encode(audio_arr.flatten()).decode("utf-8")
                    self.audio_shape = audio_arr.shape
                except KeyboardInterrupt:
                    done = True
        finally:
            camera.stop()
