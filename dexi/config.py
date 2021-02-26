from decouple import config

GITHUB_TOKEN = config("GITHUB_TOKEN")
DEFAULT_PAGE_SIZE = config("DEFAULT_PAGE_SIZE", cast=int, default=100)
