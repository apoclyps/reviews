import os
from typing import Dict, List, Tuple

from decouple import AutoConfig, Csv
from rich.color import ANSI_COLOR_NAMES

# configures decouple to use settings.ini or .env file from another directory
if path_to_config := os.environ.get("PATH_TO_CONFIG", None):
    config = AutoConfig(search_path=path_to_config)
else:
    config = AutoConfig()

# Github Config
GITHUB_TOKEN = config("GITHUB_TOKEN", cast=str, default="")
GITHUB_USER = config("GITHUB_USER", cast=str, default="")
GITHUB_URL = config("GITHUB_URL", cast=str, default="https://api.github.com")
DEFAULT_PAGE_SIZE = config("DEFAULT_PAGE_SIZE", cast=int, default=100)

# Application Config
PATH_TO_CONFIG = config("PATH_TO_CONFIG", cast=str, default=None)
DELAY_REFRESH = config("DELAY_REFRESH", cast=int, default=60)
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
