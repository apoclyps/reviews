from time import sleep

from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.table import Table

import asyncio
import time
import schedule
import queue


jobqueue = queue.Queue(maxsize=1000)


def pull_request_job():
    # print("Fetching Pull Requests...")
    jobqueue.put(1)


def organisation_scan_job():
    # print("Fetching Repositories for Organization...")
    # sleep(30)
    jobqueue.put(2)


def update():
    schedule.every(1).seconds.do(pull_request_job)
    # schedule.every(30).seconds.do(organisation_scan_job)

    while True:
        schedule.run_pending()
        sleep(1)


def render():
    job_progress = Progress(
        "{task.description}",
        SpinnerColumn(),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    )
    task1 = job_progress.add_task("[white]Pull Requests", total=10)
    job_2 = job_progress.add_task("[white]Comments", total=25)
    job_3 = job_progress.add_task("[white]Labels", total=35)

    progress_table = Table.grid()
    progress_table.add_row(
        Panel.fit(
            job_progress, title="[b]Next Update", border_style="red", padding=(1, 2)
        ),
    )

    with Live(progress_table, refresh_per_second=10):
        while True:
            complete = False
            while not complete:
                sleep(0.5)
                # for job in job_progress.tasks:

                if not jobqueue.empty():
                    counter = jobqueue.get()

                    if counter == 1:
                        task = job_progress.tasks[counter]
                        if not task.finished:
                            job_progress.advance(task.id)

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


if __name__ == "__main__":
    asyncio.run(main())
