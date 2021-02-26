from datetime import datetime

from rich import box
from rich.align import Align
from rich.console import Console, RenderGroup
from rich.layout import Layout
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.text import Text
from rich.tree import Tree

console = Console()


def make_layout() -> Layout:
    """Define the layout."""
    layout = Layout(name="root")

    layout.split(
        Layout(name="header", size=3),
        Layout(name="main", ratio=1),
        Layout(name="footer", size=7),
    )
    layout["main"].split(
        Layout(name="side"),
        Layout(name="body", ratio=2, minimum_size=60),
        Layout(name="right_side"),
        direction="horizontal",
    )
    layout["side"].split(Layout(name="pull_requests"))
    layout["right_side"].split(Layout(name="review"), Layout(name="ship"))
    return layout


def make_sponsor_message() -> Panel:
    """Some example content."""

    intro_message = Text.from_markup(
        """Consider supporting my work via Github Sponsors, or buy me a coffee to say thanks. - Kyle Harrison"""
    )

    message = Table.grid(padding=1)
    message.add_column()
    message.add_column(no_wrap=True)
    message.add_row(intro_message)

    message_panel = Panel(
        Align.center(
            RenderGroup(intro_message),
            vertical="middle",
        ),
        box=box.ROUNDED,
        padding=(1, 2),
        title="[b white]Activity Log",
        border_style="bright_blue",
    )
    return message_panel


class Header:
    """Display header with clock."""

    def __rich__(self) -> Panel:
        grid = Table.grid(expand=True)
        grid.add_column(justify="center", ratio=1)
        grid.add_column(justify="right")
        grid.add_row(
            "[b]Dexi[/b] Code Review Manager",
            datetime.now().ctime().replace(":", "[blink]:[/]"),
        )
        return Panel(grid, style="white on blue")


def tree_layout(workspace, tree):
    if not tree:
        tree = Tree(f"[white]{workspace}")

    def build_tree(workspace, tree):
        icon = "🐍 Contains: Python"
        dexi_tree = tree.add(workspace)

        pr_tree = dexi_tree.add("[123123] Update something in the code")
        pr_tree.add(Text(icon))

        pr_tree = dexi_tree.add("[312312] Revert everything")
        pr_tree.add(Text(icon))

        return tree

    tree = build_tree(workspace=workspace, tree=tree)

    return tree


def new_job_progress(layout):
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

    pull_request_tree = tree_layout(workspace="apoclyps", tree=None)

    layout["header"].update(Header())
    layout["body"].update(make_sponsor_message())
    layout["pull_requests"].update(
        Panel(pull_request_tree, title="Pull Requests", border_style="blue")
    )

    layout["review"].update(Panel("", title="Ready to Review", border_style="blue"))

    layout["ship"].update(Panel("", title="Ready to Ship", border_style="blue"))
    layout["footer"].update(progress_table)

    return job_progress, layout, overall_progress, overall_task
