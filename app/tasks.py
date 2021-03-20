import asyncio
from datetime import datetime
from time import sleep
from typing import List, Tuple

from rich.console import RenderGroup
from rich.live import Live
from rich.panel import Panel

from app import config
from app.controller import retrieve_pull_requests
from app.layout.helpers import generate_layout, generate_log_table, generate_tree_layout
from app.layout.managers import RenderLayoutManager, generate_progress_tracker
from app.notifications.domain import PullRequestNotification
from app.notifications.enums import Language
from app.notifications.notify import NotificationClient

logs: List[Tuple[str, str]] = []


def add_log_event(message: str) -> List[Tuple[str, str]]:
    """adds a log event to a list of logs and displays the top 20."""
    global logs

    logs = logs[-20:]
    logs.append(
        (str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), f"[white]{message}")
    )
    return logs


def _render_pull_requests(configuration: List[Tuple[str, str]]):
    """ Renders all pull requests for the provided configuration"""

    tables = [
        retrieve_pull_requests(org=org, repository=repo)
        for (org, repo) in configuration
    ]

    # filter unrenderable `None` results
    return Panel(
        RenderGroup(*[t for t in tables if t]),
        title="Activity",
        border_style="blue",
    )


def render():
    """Renders Terminal UI Dashboard"""
    (
        job_progress,
        overall_progress,
        overall_task,
        progress_table,
    ) = generate_progress_tracker()

    overall_progress = None

    # initial load should be from database
    add_log_event(message="initializing...")

    configuration = config.get_configuration()

    notification_client = NotificationClient()
    layout_manager = RenderLayoutManager(layout=generate_layout())
    layout_manager.render_layout(
        progress_table=progress_table,
        body=_render_pull_requests(configuration=configuration),
        pull_request_component=generate_tree_layout(configuration=configuration),
        log_component=generate_log_table(logs=logs),
    )

    add_log_event(message="refreshing view...")

    with Live(layout_manager.layout, refresh_per_second=30, screen=True):
        while True:
            if not overall_progress or overall_progress.finished:
                (
                    job_progress,
                    overall_progress,
                    overall_task,
                    progress_table,
                ) = generate_progress_tracker()

            add_log_event(message="awaiting...")

            # update view (blocking operation)
            layout_manager.render_layout(
                progress_table=progress_table,
                body=_render_pull_requests(configuration=configuration),
                pull_request_component=generate_tree_layout(
                    configuration=configuration
                ),
                log_component=generate_log_table(logs=logs),
            )

            # wait for update
            while not overall_progress.finished:
                sleep(0.1)
                for job in job_progress.tasks:
                    if not job.finished:
                        job_progress.advance(job.id)

                completed = sum(task.completed for task in job_progress.tasks)
                overall_progress.update(overall_task, completed=completed)

            add_log_event(message="view refreshed")

            if config.ENABLE_NOTIFICATIONS:
                add_log_event(message="sending notification")
                org, repo = configuration[0]
                pull_request = PullRequestNotification(
                    org=org,
                    repository=repo,
                    name="nootifier",
                    language=Language.PYTHON,
                    number=1,
                )
                notification_client.send_pull_request_approved(model=pull_request)
                add_log_event(message="notification sent")


async def update():
    """Updates data in the background."""

    while True:
        print("working")
        await asyncio.sleep(1)
