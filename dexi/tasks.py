import asyncio
from time import sleep

from rich.console import RenderGroup
from rich.live import Live
from rich.panel import Panel

from dexi.controller import retrieve_pull_requests
from dexi.layout.helpers import generate_layout, generate_tree_layout
from dexi.layout.managers import RenderLayoutManager, generate_progress_tracker
from dexi.notifications.domain import PullRequestNotification
from dexi.notifications.notify import Notification
from dexi.notifications.enums import Language

def _render_pull_requests():
    return Panel(
        RenderGroup(
            retrieve_pull_requests(org="slicelife", repository="ros-service"),
            retrieve_pull_requests(org="slicelife", repository="delivery-service"),
            retrieve_pull_requests(org="slicelife", repository="pos-integration"),
            retrieve_pull_requests(
                org="slicelife", repository="candidate-code-challenges"
            ),
            retrieve_pull_requests(org="apoclyps", repository="dexi"),
        ),
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

    # intial load should be from database
    layout_manager = RenderLayoutManager(layout=generate_layout())
    layout_manager.render_layout(
        progress_table=progress_table,
        body=_render_pull_requests(),
        status="loading",
        pull_request_component=generate_tree_layout(),
        log_component="",
    )

    with Live(layout_manager.layout, refresh_per_second=30, screen=True):
        while True:
            if not overall_progress or overall_progress.finished:
                (
                    job_progress,
                    overall_progress,
                    overall_task,
                    progress_table,
                ) = generate_progress_tracker()

            # update view (blocking operation)
            layout_manager.render_review(component="pending")
            layout_manager.render_layout(
                progress_table=progress_table,
                body=_render_pull_requests(),
                status="updated",
                pull_request_component=generate_tree_layout(),
                log_component="",
            )

            # wait for update
            while not overall_progress.finished:
                sleep(0.1)
                for job in job_progress.tasks:
                    if not job.finished:
                        job_progress.advance(job.id)

                completed = sum(task.completed for task in job_progress.tasks)
                overall_progress.update(overall_task, completed=completed)
            
            # trigger notification
            pr_info = PullRequestNotification(org="Slice", repository="ros-service", name="nootifier", language=Language.PYTHON)
            Notification.send_pull_request_approved(pr_info)


async def update():
    """Updates data in the background."""

    while True:
        print("working")
        await asyncio.sleep(1)
