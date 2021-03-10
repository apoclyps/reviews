import time

from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.table import Table

from scheduler.enums import Tasks


def generate_progress():
    return Progress(
        "{task.description}",
        SpinnerColumn(),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    )


def generate_tasks(progress):
    tasks = {
        Tasks.PULL_REQUESTS: progress.add_task("[white]Pull Requests", total=10),
        Tasks.ORG_SCAN: progress.add_task("[white]Comments", total=60),
    }
    return tasks


def generate_table(progress):
    table = Table.grid()
    table.add_row(
        Panel.fit(
            progress, title="[b]Next Update", border_style="blue", padding=(1, 2)
        ),
    )
    return table


def render():
    progress = generate_progress()
    tasks = generate_tasks(progress=progress)
    table = generate_table(progress=progress)

    with Live(table, refresh_per_second=10, screen=False):
        while True:
            complete = False
            while not complete:
                for task in progress.tasks:
                    if task := progress.tasks[task.id]:
                        if not task.finished:
                            progress.advance(task.id, advance=0.6)

                complete = all([t.finished for t in progress.tasks])
                if not complete:
                    time.sleep(1)

            while complete:
                for job in progress.tasks:
                    if job.finished:
                        progress.reset(job.id)
                complete = False
