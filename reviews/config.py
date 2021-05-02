from pathlib import Path
from typing import List, Tuple

from decouple import Csv, config

# Github Config
GITHUB_TOKEN = config("GITHUB_TOKEN", cast=str, default="")
GITHUB_USER = config("GITHUB_USER", cast=str, default="")
DEFAULT_PAGE_SIZE = config("DEFAULT_PAGE_SIZE", cast=int, default=100)

# Database Config
DATA_PATH = config(
    "DATA_PATH", cast=str, default=f"{str(Path.home())}/.code_review_manager"
)
FILENAME = config("FILENAME", cast=str, default="code_review_manager.db")

# Application Config
DELAY_REFRESH = config("DELAY_REFRESH", cast=int, default=60)
ENABLE_NOTIFICATIONS = config("ENABLE_NOTIFICATIONS", cast=bool, default=False)
ENABLE_PERSISTED_DATA = config("ENABLE_PERSISTED_DATA", cast=bool, default=False)
REPOSITORY_CONFIGURATION = config(
    "REPOSITORY_CONFIGURATION",
    cast=Csv(),
    default="apoclyps/code-review-manager",
)


def get_configuration() -> List[Tuple[str, str]]:
    """converts a comma seperated list of organizations/repositories into a list
    of tuples.
    """

    def _to_tuple(values):
        return (values[0], values[1])

    return [
        _to_tuple(values=configuration.split(sep="/", maxsplit=1))
        for configuration in REPOSITORY_CONFIGURATION
    ]
