import os

from decouple import AutoConfig, Csv

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
