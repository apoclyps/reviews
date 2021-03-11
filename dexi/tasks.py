import asyncio
from time import sleep

from rich.live import Live

from dexi.layout.helpers import generate_layout, render_pull_request_table
from dexi.layout.terminal import generate_progress_tracker, render_layout
from dexi.source_control.client import GithubAPI


def render():
    """Renders Terminal UI Dashboard"""
    layout = generate_layout()

    (
        job_progress,
        layout,
        overall_progress,
        overall_task,
        progress_table,
    ) = generate_progress_tracker(layout)

    overall_progress = None

    repo = GithubAPI().get_repository(org="slicelife", repo="ros-service")
    pull_requests = GithubAPI().get_pull_requests(
        repository=repo, state="open", sort="created", base="master"
    )

    body = render_pull_request_table(pull_requests=pull_requests)
    render_layout(layout=layout, progress_table=progress_table, body=body)

    # TODO: fetch from database
    # database = config.DATA_PATH + "/" + config.FILENAME
    # conn = create_connection(database)
    # cur = conn.cursor()
    # cur.execute("SELECT * FROM pull_requests")
    # rows = cur.fetchall()

    with Live(layout, refresh_per_second=30, screen=True):
        while True:
            if not overall_progress or overall_progress.finished:
                (
                    job_progress,
                    layout,
                    overall_progress,
                    overall_task,
                    progress_table,
                ) = generate_progress_tracker(layout)

            body = render_pull_request_table(pull_requests=pull_requests)
            if not body:
                body = ""
            render_layout(layout=layout, progress_table=progress_table, body=body)

            while not overall_progress.finished:
                sleep(0.1)
                for job in job_progress.tasks:
                    if not job.finished:
                        job_progress.advance(job.id)

                pull_requests = GithubAPI().get_pull_requests(
                    repository=repo, state="open", sort="created", base="master"
                )

                completed = sum(task.completed for task in job_progress.tasks)
                overall_progress.update(overall_task, completed=completed)


async def update():
    """Updates data in the background."""

    while True:
        print("working")
        await asyncio.sleep(1)
