from pathlib import Path

from decouple import config

# Github Config
GITHUB_TOKEN = config("GITHUB_TOKEN")
DEFAULT_PAGE_SIZE = config("DEFAULT_PAGE_SIZE", cast=int, default=100)

# Database Config
DATA_PATH = config("DATA_PATH", cast=str, default=f"{str(Path.home())}/.dexi")
FILENAME = config("FILENAME", cast=str, default="dexi.db")

# Application Config
ENABLE_NOTIFICATIONS = config("ENABLE_NOTIFICATIONS", cast=bool, default=False)
