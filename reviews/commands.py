from rich.console import Console

from .config import settings
from .config.controller import render_config_table
from .config.helpers import get_configuration
from .controller import GithubPullRequestController, GitlabPullRequestController


def render(provider: str) -> None:
    """Renders the Terminal UI Dashboard once before closing the application"""

    configuration = None
    body = None
    console: Console = Console()

    if provider == "gitlab":
        configuration = get_configuration(config=settings.REVIEWS_GITLAB_REPOSITORY_CONFIGURATION)
        body = GitlabPullRequestController().render(configuration=configuration)
    else:
        configuration = get_configuration(config=settings.REVIEWS_GITHUB_REPOSITORY_CONFIGURATION)
        body = GithubPullRequestController().render(configuration=configuration)

    console.print(body, justify="center")


def render_config(show: bool) -> None:
    """Renders a table displaying configuration used by Reviews."""
    configurations = [
        {
            "name": "GITHUB_TOKEN",
            "value": settings.GITHUB_TOKEN if show else "".join("*" for _ in range(len(settings.GITHUB_TOKEN))),
        },
        {"name": "GITHUB_USER", "value": settings.GITHUB_USER},
        {"name": "GITHUB_URL", "value": settings.GITHUB_URL},
        {
            "name": "GITLAB_TOKEN",
            "value": settings.GITLAB_TOKEN if show else "".join("*" for _ in range(len(settings.GITLAB_TOKEN))),
        },
        {"name": "GITLAB_USER", "value": settings.GITLAB_USER},
        {"name": "GITLAB_URL", "value": settings.GITLAB_URL},
        {
            "name": "REVIEWS_PATH_TO_CONFIG",
            "value": f"{settings.REVIEWS_PATH_TO_CONFIG}",
        },
        {
            "name": "GITHUB_DEFAULT_PAGE_SIZE",
            "value": f"{settings.GITHUB_DEFAULT_PAGE_SIZE}",
        },
        {"name": "REVIEWS_DELAY_REFRESH", "value": f"{settings.REVIEWS_DELAY_REFRESH}"},
        {
            "name": "REVIEWS_GITHUB_REPOSITORY_CONFIGURATION",
            "value": ", ".join(settings.REVIEWS_GITHUB_REPOSITORY_CONFIGURATION),
        },
        {
            "name": "REVIEWS_GITLAB_REPOSITORY_CONFIGURATION",
            "value": ", ".join(settings.REVIEWS_GITLAB_REPOSITORY_CONFIGURATION),
        },
        {
            "name": "REVIEWS_LABEL_CONFIGURATION",
            "value": ", ".join(settings.REVIEWS_LABEL_CONFIGURATION),
        },
    ]

    render_config_table(configurations=configurations)
