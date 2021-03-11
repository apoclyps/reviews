from pathlib import Path

from decouple import config

GITHUB_TOKEN = config("GITHUB_TOKEN")
DEFAULT_PAGE_SIZE = config("DEFAULT_PAGE_SIZE", cast=int, default=100)


DATA_PATH = config("DATA_PATH", cast=str, default=f"{str(Path.home())}/.dexi")
FILENAME = config("FILENAME", cast=str, default="dexi.db")
