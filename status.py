from time import sleep

from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.table import Table

import asyncio
import time


def update():
    while True:
        # do some work
        for i in range(0, 100):
            time.sleep(10)


def render():
    job_progress = Progress(
        "{task.description}",
        SpinnerColumn(),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    )
    job_progress.add_task("[white]Request Pull Requests", total=10)
    job_progress.add_task("[white]Request Comments", total=25)
    job_progress.add_task("[white]Request Labels", total=35)

    progress_table = Table.grid()
    progress_table.add_row(
        Panel.fit(job_progress, title="[b]Background", border_style="red", padding=(1, 2)),
    )

    with Live(progress_table, refresh_per_second=10):
        while True:
            complete = False
            while not complete:
                sleep(0.1)
                for job in job_progress.tasks:
                    if not job.finished:
                        job_progress.advance(job.id)

                complete = all([task.finished for task in job_progress.tasks])

            while complete:
                for job in job_progress.tasks:
                    if job.finished:
                        job_progress.reset(job.id)

                complete = False

            

async def main():
    await asyncio.gather(
        asyncio.to_thread(update),
        asyncio.to_thread(render),
    )


asyncio.run(main())