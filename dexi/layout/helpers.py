from datetime import datetime

import humanize
from rich.console import RenderGroup
from rich.layout import Layout
from rich.table import Table
from rich.text import Text
from rich.tree import Tree

from dexi.models import PullRequest


def render_pull_request_table(title, pull_requests):
    table = Table(show_header=True, header_style="bold white")
    table.add_column("#", style="dim", width=3)
    table.add_column(title, width=70)
    table.add_column("Latest Activity")
    table.add_column("Status", width=10)

    pull_requests = sorted(pull_requests, key=lambda x: x.updated_at, reverse=True)

    for pr in pull_requests:
        approved = "Approved" if pr.approved else ""
        updated_at = humanize.naturaltime(pr.updated_at)

        table.add_row(
            f"[white]{pr.number} ",
            f"[white]{pr.title}",
            f"{updated_at}",
            f"{approved}",
        )

    return table


def generate_layout() -> Layout:
    """Define the layout."""
    layout = Layout(name="root")

    layout.split(
        Layout(name="header", size=3),
        Layout(name="main", ratio=1),
        Layout(name="footer", size=7),
    )
    layout["main"].split(
        Layout(name="left_side"),
        Layout(name="body", ratio=2, minimum_size=60),
        Layout(name="right_side"),
        direction="horizontal",
    )
    layout["left_side"].split(Layout(name="configuration"), Layout(name="log"))
    layout["right_side"].split(Layout(name="review"), Layout(name="ship"))
    return layout


def generate_tree_layout():
    data = [
        {
            "org": "apoclyps",
            "repository_name": "dexi",
            "pull_requests": [
                PullRequest(
                    number=1,
                    title="test",
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                    approved=False,
                ),
            ],
        },
        {
            "org": "slicelife",
            "repository_name": "ros-service",
            "pull_requests": [
                PullRequest(
                    number=2,
                    title="test",
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                    approved=True,
                ),
            ],
        },
        {
            "org": "slicelife",
            "repository_name": "delivery-service",
            "pull_requests": [
                PullRequest(
                    number=1,
                    title="test",
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                    approved=False,
                ),
                PullRequest(
                    number=3,
                    title="test",
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                    approved=True,
                ),
            ],
        },
        {
            "org": "slicelife",
            "repository_name": "pos-integration",
            "pull_requests": [
                PullRequest(
                    number=2,
                    title="test",
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                    approved=True,
                ),
            ],
        },
    ]

    trees = {}
    for org in data:
        workspace = org["org"]
        tree = trees.get(workspace, Tree(f"[white]{workspace}"))

        # icon = "🐍 Contains: Python"
        inner_tree = tree.add(org.get("repository_name", []))

        for pull_request in org.get("pull_requests", []):
            repo_tree = inner_tree.add(f"[{pull_request.number}] {pull_request.title}")
            # repo_tree.add(Text(icon))

        trees[workspace] = tree

    return RenderGroup(*[t for t in trees.values()])
