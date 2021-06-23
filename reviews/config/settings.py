import os

from decouple import AutoConfig, Csv

# configures decouple to use settings.ini or .env file from another directory
if REVIEWS_PATH_TO_CONFIG := os.environ.get("REVIEWS_PATH_TO_CONFIG", None):
    config = AutoConfig(search_path=REVIEWS_PATH_TO_CONFIG)
else:
    config = AutoConfig()

# Github Config
GITHUB_TOKEN = config("GITHUB_TOKEN", cast=str, default="")
GITHUB_USER = config("GITHUB_USER", cast=str, default="")
GITHUB_URL = config("GITHUB_URL", cast=str, default="https://api.github.com")
GITHUB_DEFAULT_PAGE_SIZE = config("GITHUB_DEFAULT_PAGE_SIZE", cast=int, default=100)

# Gitlab config
GITLAB_TOKEN = config("GITLAB_TOKEN", cast=str, default="")
GITLAB_USER = config("GITLAB_USER", cast=str, default="")
GITLAB_URL = config("GITLAB_URL", cast=str, default="https://gitlab.com")
GITLAB_DEFAULT_PAGE_SIZE = config("GITLAB_DEFAULT_PAGE_SIZE", cast=int, default=100)

# Application Config
REVIEWS_PATH_TO_CONFIG = config("REVIEWS_PATH_TO_CONFIG", cast=str, default=None)
REVIEWS_DELAY_REFRESH = config("REVIEWS_DELAY_REFRESH", cast=int, default=60)
REVIEWS_GITHUB_REPOSITORY_CONFIGURATION = config(
    "REVIEWS_GITHUB_REPOSITORY_CONFIGURATION",
    cast=Csv(),
    default="apoclyps/reviews",
)
REVIEWS_GITLAB_REPOSITORY_CONFIGURATION = config(
    "REVIEWS_GITLAB_REPOSITORY_CONFIGURATION",
    cast=Csv(),
    default="27629846:apoclyps/reviews",
)
REVIEWS_LABEL_CONFIGURATION = config(
    "REVIEWS_LABEL_CONFIGURATION",
    cast=Csv(),
    default="blocked/orange,docker/blue,security/red,python/green",
)
