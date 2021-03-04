# import click
import asyncclick as click

from time import sleep
from rich.live import Live
from dexi.fullscreen import new_job_progress, make_layout
from dexi.source_control import get_repos
from create import prepare_database

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS)
async def main():
    """Click entrypoint with help provided by default."""


@main.command(help="Display a dashboard")
async def dashboard():
    """ Dashboard command. """

    click.echo("start dashboard")

    prepare_database()

    layout = make_layout()

    (
        job_progress,
        layout,
        overall_progress,
        overall_task,
    ) = new_job_progress(layout)

    overall_progress = None

    with Live(layout, refresh_per_second=30, screen=True):
        while True:
            if not overall_progress or overall_progress.finished:
                (
                    job_progress,
                    layout,
                    overall_progress,
                    overall_task,
                ) = new_job_progress(layout)

            table = await get_repos(layout)
            layout["body"].update(table)

            while not overall_progress.finished:
                # TODO: use async defer
                sleep(0.05)

                for job in job_progress.tasks:
                    if not job.finished:
                        job_progress.advance(job.id)

                completed = sum(task.completed for task in job_progress.tasks)
                overall_progress.update(overall_task, completed=completed)


if __name__ == "__main__":
    # click.anyio_backend = "asyncio"

    main(_anyio_backend="asyncio")
