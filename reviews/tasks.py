import asyncio
from datetime import datetime
from time import sleep
from typing import List, Tuple

from rich.console import RenderGroup
from rich.live import Live
from rich.panel import Panel

from reviews import config
from reviews.controller import PullRequestController
from reviews.layout import (
    RenderLayoutManager,
    generate_layout,
    generate_log_table,
    generate_progress_tracker,
    generate_tree_layout,
)
from reviews.notifications import NotificationClient, PullRequestNotification

logs: List[Tuple[str, str]] = []


def add_log_event(message: str) -> List[Tuple[str, str]]:
    """adds a log event to a list of logs and displays the top 20."""
    global logs

    logs = logs[-20:]
    logs.append(
        (str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), f"[white]{message}")
    )
    return logs


def _render_pull_requests(
    controller: PullRequestController, configuration: List[Tuple[str, str]]
):
    """Renders all pull requests for the provided configuration"""

    tables = [
        controller.retrieve_pull_requests(org=org, repository=repo)
        for (org, repo) in configuration
    ]

    # filter unrenderable `None` results
    return Panel(
        RenderGroup(*[t for t in tables if t]),
        title="Activity",
        border_style="blue",
    )


def render(no_reload: bool):
    """Renders Terminal UI Dashboard"""
    prog_tracker = generate_progress_tracker()
    prog_tracker["overall_progress"] = None

    # initial load should be from database
    add_log_event(message="initializing...")

    configuration = config.get_configuration()
    controller = PullRequestController()

    notification_client = NotificationClient()
    layout_manager = RenderLayoutManager(layout=generate_layout())
    layout_manager.render_layout(
        progress_table=prog_tracker["progress_table"],
        body=Panel(
            RenderGroup(),
            title="Activity",
            border_style="blue",
        ),
        pull_request_component=generate_tree_layout(configuration=configuration),
        log_component=generate_log_table(logs=logs),
    )

    with Live(
        layout_manager.layout, refresh_per_second=5, screen=(not no_reload)
    ) as live:
        while True:
            if (
                not prog_tracker["overall_progress"]
                or prog_tracker["overall_progress"].finished
            ):
                prog_tracker = generate_progress_tracker()

            add_log_event(message="waiting...")

            # update view (blocking operation)
            layout_manager.render_layout(
                progress_table=prog_tracker["progress_table"],
                body=_render_pull_requests(
                    controller=controller, configuration=configuration
                ),
                pull_request_component=generate_tree_layout(
                    configuration=configuration
                ),
                log_component=generate_log_table(logs=logs),
            )
            if no_reload:
                live.stop()
                break

            if config.ENABLE_NOTIFICATIONS:
                add_log_event(message="sending notification")
                org, repo = configuration[0]
                pull_request = PullRequestNotification(
                    org=org,
                    repository=repo,
                    name="nootifier",
                    number=1,
                )
                notification_client.send_pull_request_approved(model=pull_request)
                add_log_event(message="notification sent")

            delay = config.DELAY_REFRESH * 0.01
            while not prog_tracker["overall_progress"].finished:
                sleep(delay)
                for job in prog_tracker["job_progress"].tasks:
                    if not job.finished:
                        prog_tracker["job_progress"].advance(job.id)

                completed = sum(
                    task.completed for task in prog_tracker["job_progress"].tasks
                )
                prog_tracker["overall_progress"].update(
                    prog_tracker["overall_task"], completed=completed
                )

            add_log_event(message="updated")


async def update():
    """Updates data in the background."""

    while True:
        print("working")
        await asyncio.sleep(1)
