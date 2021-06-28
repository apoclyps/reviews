from datetime import datetime
from time import sleep
from typing import List, Tuple

from rich.console import RenderGroup
from rich.live import Live
from rich.panel import Panel

from .config import settings
from .config.controller import render_config_table
from .config.helpers import get_configuration
from .controller import GithubPullRequestController, GitlabPullRequestController, PullRequestController
from .layout import (
    RenderLayoutManager,
    generate_layout,
    generate_log_table,
    generate_progress_tracker,
    generate_tree_layout,
)

logs: List[Tuple[str, str]] = []


def add_log_event(message: str) -> List[Tuple[str, str]]:
    """adds a log event to a list of logs and displays the top 20."""
    global logs

    logs = logs[-20:]
    logs.append((str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), f"[white]{message}"))
    return logs


def single_render(provider: str) -> None:
    """Renders the Terminal UI Dashboard once before closing the application"""

    configuration = None
    body = None

    if provider == "gitlab":
        configuration = get_configuration(config=settings.REVIEWS_GITLAB_REPOSITORY_CONFIGURATION)
        body = GitlabPullRequestController().render(configuration=configuration)
    else:
        configuration = get_configuration(config=settings.REVIEWS_GITHUB_REPOSITORY_CONFIGURATION)
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


def render(provider: str) -> None:
    """Renders Terminal UI Dashboard"""
    (
        job_progress,
        overall_progress,
        overall_task,
        progress_table,
    ) = generate_progress_tracker()

    # initial load should be from database
    add_log_event(message="initializing...")

    configuration = None
    controller: PullRequestController

    if provider == "gitlab":
        configuration = get_configuration(config=settings.REVIEWS_GITLAB_REPOSITORY_CONFIGURATION)
        controller = GitlabPullRequestController()
    else:
        configuration = get_configuration(config=settings.REVIEWS_GITHUB_REPOSITORY_CONFIGURATION)
        controller = GitlabPullRequestController()
        controller = GithubPullRequestController()

    layout_manager = RenderLayoutManager(layout=generate_layout())
    layout_manager.render_layout(
        progress_table=progress_table,
        body=Panel(
            RenderGroup(),
            title="Activity",
            border_style="blue",
        ),
        pull_request_component=generate_tree_layout(configuration=configuration),
        log_component=generate_log_table(logs=logs),
    )

    with Live(layout_manager.layout, refresh_per_second=5, screen=True):
        while True:
            if not overall_progress or overall_progress.finished:
                (
                    job_progress,
                    overall_progress,
                    overall_task,
                    progress_table,
                ) = generate_progress_tracker()

            add_log_event(message="waiting...")

            # update view (blocking operation)
            layout_manager.render_layout(
                progress_table=progress_table,
                body=controller.render(configuration=configuration),
                pull_request_component=generate_tree_layout(configuration=configuration),
                log_component=generate_log_table(logs=logs),
            )

            delay = settings.REVIEWS_DELAY_REFRESH * 0.01
            while not overall_progress.finished:
                sleep(delay)
                for job in job_progress.tasks:
                    if not job.finished:
                        job_progress.advance(job.id)

                completed = sum(task.completed for task in job_progress.tasks)
                overall_progress.update(overall_task, completed=completed)

            add_log_event(message="updated")


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
        {"name": "REVIEWS_PATH_TO_CONFIG", "value": f"{settings.REVIEWS_PATH_TO_CONFIG}"},
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
