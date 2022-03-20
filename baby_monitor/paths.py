from pathlib import Path
from pkg_resources import resource_filename
from platform import system


# The path to the data files.
DATA_DIRECTORY = Path(resource_filename(__name__, "data"))
# Set the data path for compiled games.
if not DATA_DIRECTORY.exists():
    if system() == "Darwin":
        from Foundation import NSBundle
        DATA_DIRECTORY = Path(NSBundle.mainBundle().bundlePath()).joinpath("Contents/data")
    else:
        DATA_DIRECTORY = Path("data").resolve()
FONT_PATH = DATA_DIRECTORY.joinpath("fonts/raleway/Raleway-SemiBold.otf")
IMAGES_DIRECTORY = DATA_DIRECTORY.joinpath("images")
AUDIO_DIRECTORY = DATA_DIRECTORY.joinpath("audio")
