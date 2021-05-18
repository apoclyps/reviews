from pathlib import Path
from typing import Dict, List, Tuple

from decouple import Csv, config
from rich.color import ANSI_COLOR_NAMES

# Github Config
GITHUB_TOKEN = config("GITHUB_TOKEN", cast=str, default="")
GITHUB_USER = config("GITHUB_USER", cast=str, default="")
GITHUB_URL = config("GITHUB_URL", cast=str, default="https://api.github.com")
DEFAULT_PAGE_SIZE = config("DEFAULT_PAGE_SIZE", cast=int, default=100)

# Database Config
DATA_PATH = config("DATA_PATH", cast=str, default=f"{str(Path.home())}/.reviews")
FILENAME = config("FILENAME", cast=str, default="reviews.db")

# Application Config
DELAY_REFRESH = config("DELAY_REFRESH", cast=int, default=60)
ENABLE_PERSISTED_DATA = config("ENABLE_PERSISTED_DATA", cast=bool, default=False)
REPOSITORY_CONFIGURATION = config(
    "REPOSITORY_CONFIGURATION",
    cast=Csv(),
    default="apoclyps/reviews",
)
LABEL_CONFIGURATION = config(
    "LABEL_CONFIGURATION",
    cast=Csv(),
    default="blocked/orange,docker/blue,security/red,python/green",
)


def get_configuration() -> List[Tuple[str, str]]:
    """converts a comma seperated list of organizations/repositories into a list
    of tuples.
    """

    def _to_tuple(values: List[str]) -> Tuple[str, str]:
        return (values[0], values[1])

    return [
        _to_tuple(values=configuration.split(sep="/", maxsplit=1))
        for configuration in REPOSITORY_CONFIGURATION
    ]


def get_label_colour_map() -> Dict[str, str]:
    """converts a comma seperated list of organizations/repositories into a list
    of tuples.
    """

    def _preproc(label_colour: str) -> List[str]:
        return label_colour.lower().split(sep="/")

    return {
        label: f"[{colour}]"
        for label, colour in map(_preproc, LABEL_CONFIGURATION)
        if colour in ANSI_COLOR_NAMES
    }
