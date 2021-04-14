from datetime import datetime
from typing import Dict, List, Tuple

import humanize
from rich import box
from rich.console import RenderGroup
from rich.layout import Layout
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.tree import Tree

from reviews.datasource import PullRequest


def render_pull_request_table(title: str, pull_requests: List[PullRequest]) -> Table:
    """Renders a list of pull requests as a table"""
    table = Table(show_header=True, header_style="bold white")
    table.add_column("#", style="dim", width=5)
    table.add_column(title, width=60)
    table.add_column("Labels", width=40)
    table.add_column("Activity", width=15)
    table.add_column("Status", width=10)

    pull_requests = sorted(pull_requests, key=lambda x: x.updated_at, reverse=True)

    for pr in pull_requests:
        approved = "[green]Approved" if pr.approved else ""
        updated_at = humanize.naturaltime(pr.updated_at)

        colour = ""
        if (datetime.now() - pr.updated_at).days >= 7:
            colour = "[red]"
        elif (datetime.now() - pr.updated_at).days >= 1:
            colour = "[yellow]"
        updated_at = f"{colour}{updated_at}"

        labels = ", ".join([label.name for label in pr.labels])

        table.add_row(
            f"[white]{pr.number} ",
            f"[white]{pr.title}",
            f"{labels}",
            f"{updated_at}",
            f"{approved}",
        )

    return table


def generate_layout() -> Layout:
    """Define the layout for the terminal UI."""
    layout = Layout(name="root")

    layout.split(
        Layout(name="header", size=3),
        Layout(name="main", ratio=1),
        Layout(name="footer", size=7),
    )
    layout["main"].split_row(
        Layout(name="left_side"),
        Layout(name="body", ratio=2, minimum_size=60),
    )
    layout["left_side"].split(Layout(name="configuration"), Layout(name="log"))
    return layout


def generate_tree_layout(configuration: List[Tuple[str, str]]) -> RenderGroup:
    """Generates a tree layout for the settings configuration"""
    organization_tree_mapping: Dict[str, Tree] = {}
    for (org, repo) in configuration:
        tree = organization_tree_mapping.get(f"{org}", Tree(f"[white]{org}"))
        tree.add(f"[link=https://www.github.com/{org}/{repo}]{repo}[/link]")
        organization_tree_mapping[org] = tree

    return RenderGroup(*organization_tree_mapping.values())


def generate_log_table(logs):
    """Generetes a table for logging activity"""
    table = Table("Time", "Message", box=box.SIMPLE)

    for log in logs:
        time, message = log
        table.add_row(time, message)

    return table


def generate_progress_tracker():
    """Tracks the progress of background tasks"""
    progress = Progress(
        "{task.description}",
        SpinnerColumn(),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    )
    progress.add_task("[white]Pull Requests", total=100)

    total = sum(task.total for task in progress.tasks)
    overall_progress = Progress()
    overall_task = overall_progress.add_task("All", total=int(total))

    progress_table = Table.grid(expand=True)
    progress_table.add_row(
        Panel(
            overall_progress,
            title="Next Refresh",
            border_style="blue",
        ),
        Panel(
            progress, title="[b]Next fetch for:", border_style="blue", padding=(1, 2)
        ),
    )

    return progress, overall_progress, overall_task, progress_table
