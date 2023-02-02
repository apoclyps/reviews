from datetime import datetime
from typing import List, Tuple

from rich.live import Live

from ..controller import GithubPullRequestController, GitlabPullRequestController
from ..layout import RenderLayoutManager, generate_layout, generate_tree_layout
from .controller import render_config_table
from .helpers import get_configuration
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

logs: List[Tuple[str, str]] = []


def add_log_event(message: str) -> List[Tuple[str, str]]:
    """adds a log event to a list of logs and displays the top 20."""
    global logs

    logs = logs[-20:]
    logs.append((str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), f"[white]{message}"))
    return logs


def render(provider: str) -> None:
    """Renders the Terminal UI Dashboard once before closing the application"""

    configuration = None
    body = None

    if provider == "gitlab":
        configuration = get_configuration(config=REVIEWS_GITLAB_REPOSITORY_CONFIGURATION)
        body = GitlabPullRequestController().render(configuration=configuration)
    else:
        configuration = get_configuration(config=REVIEWS_GITHUB_REPOSITORY_CONFIGURATION)
        body = GithubPullRequestController().render(configuration=configuration)

    layout_manager = RenderLayoutManager(layout=generate_layout(log=False, footer=False))
    layout_manager.render_layout(
        progress_table=None,
        body=body,
        pull_request_component=generate_tree_layout(configuration=configuration),
        log_component=None,
    )

    with Live(
        renderable=layout_manager.layout,
        refresh_per_second=5,
        transient=False,
        screen=False,
    ):
        add_log_event(message="updated")


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
