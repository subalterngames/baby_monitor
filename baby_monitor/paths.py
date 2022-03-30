from pathlib import Path
from pkg_resources import resource_filename


# The path to the data files.
DATA_DIRECTORY = Path(resource_filename(__name__, "data"))
FONT_PATH = DATA_DIRECTORY.joinpath("fonts/raleway/Raleway-SemiBold.otf")
IMAGES_DIRECTORY = DATA_DIRECTORY.joinpath("images")
