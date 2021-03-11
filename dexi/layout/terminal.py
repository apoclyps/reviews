from rich.console import Console
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn
from rich.table import Table

from dexi.layout.components import Header
from dexi.layout.helpers import generate_tree_layout

console = Console()


def render_layout(layout, progress_table, body):
    pull_request_tree = generate_tree_layout(workspace="apoclyps", tree=None)

    layout["header"].update(Header())
    layout["body"].update(body)
    layout["pull_requests"].update(
        Panel(pull_request_tree, title="Pull Requests", border_style="blue")
    )
    layout["review"].update(Panel("", title="Ready to Review", border_style="blue"))
    layout["ship"].update(Panel("", title="Ready to Ship", border_style="blue"))
    layout["footer"].update(progress_table)


def generate_progress_tracker(layout):
    job_progress = Progress(
        "{task.description}",
        SpinnerColumn(),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    )
    job_progress.add_task("[white]Pull Requests", total=45)
    job_progress.add_task("[white]Ready to Review", total=120)
    job_progress.add_task("[white]Ready to Shop", total=180)

    total = sum(task.total for task in job_progress.tasks)
    overall_progress = Progress()
    overall_task = overall_progress.add_task("All Jobs", total=int(total))

    progress_table = Table.grid(expand=True)
    progress_table.add_row(
        Panel(
            overall_progress,
            title="Update Progress",
            border_style="blue",
        ),
        Panel(job_progress, title="[b]Jobs", border_style="blue", padding=(1, 2)),
    )

    return job_progress, layout, overall_progress, overall_task, progress_table
