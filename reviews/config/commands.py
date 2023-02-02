from .controller import render_config_table
from .settings import (
    GITHUB_DEFAULT_PAGE_SIZE,
    GITHUB_TOKEN,
    GITHUB_URL,
    GITHUB_USER,
    GITLAB_TOKEN,
    GITLAB_URL,
    GITLAB_USER,
    REVIEWS_DELAY_REFRESH,
    REVIEWS_GITHUB_REPOSITORY_CONFIGURATION,
    REVIEWS_GITLAB_REPOSITORY_CONFIGURATION,
    REVIEWS_LABEL_CONFIGURATION,
    REVIEWS_PATH_TO_CONFIG,
)


def render_config(show: bool) -> None:
    """Renders a table displaying configuration used by Reviews."""
    configurations = [
        {
            "name": "GITHUB_TOKEN",
            "value": GITHUB_TOKEN if show else "".join("*" for _ in range(len(GITHUB_TOKEN))),
        },
        {"name": "GITHUB_USER", "value": GITHUB_USER},
        {"name": "GITHUB_URL", "value": GITHUB_URL},
        {
            "name": "GITLAB_TOKEN",
            "value": GITLAB_TOKEN if show else "".join("*" for _ in range(len(GITLAB_TOKEN))),
        },
        {"name": "GITLAB_USER", "value": GITLAB_USER},
        {"name": "GITLAB_URL", "value": GITLAB_URL},
        {"name": "REVIEWS_PATH_TO_CONFIG", "value": f"{REVIEWS_PATH_TO_CONFIG}"},
        {
            "name": "GITHUB_DEFAULT_PAGE_SIZE",
            "value": f"{GITHUB_DEFAULT_PAGE_SIZE}",
        },
        {"name": "REVIEWS_DELAY_REFRESH", "value": f"{REVIEWS_DELAY_REFRESH}"},
        {
            "name": "REVIEWS_GITHUB_REPOSITORY_CONFIGURATION",
            "value": ", ".join(REVIEWS_GITHUB_REPOSITORY_CONFIGURATION),
        },
        {
            "name": "REVIEWS_GITLAB_REPOSITORY_CONFIGURATION",
            "value": ", ".join(REVIEWS_GITLAB_REPOSITORY_CONFIGURATION),
        },
        {
            "name": "REVIEWS_LABEL_CONFIGURATION",
            "value": ", ".join(REVIEWS_LABEL_CONFIGURATION),
        },
    ]

    render_config_table(configurations=configurations)
