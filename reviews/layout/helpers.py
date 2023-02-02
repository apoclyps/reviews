from operator import attrgetter
from typing import Dict, List

from rich.color import ANSI_COLOR_NAMES
from rich.table import Table

from ..config import settings
from ..source_control import PullRequest


def get_label_colour_map() -> Dict[str, str]:
    """converts a comma separated list of organizations/repositories into a list
    of tuples.
    """

    def _preproc(label_colour: str) -> List[str]:
        return label_colour.lower().split(sep="/")

    return {
        label: f"[{colour}]"
        for label, colour in map(_preproc, settings.REVIEWS_LABEL_CONFIGURATION)
        if colour in ANSI_COLOR_NAMES
    }


def render_repository_does_not_exist(
    title: str,
    link: str,
) -> Table:
    """Renders a list of pull requests as a table"""
    table = Table()
    table.add_column("#", style="dim", width=7)
    table.add_column(
        f"[link={link}]{title}[/link]",
        width=160,
    )

    table.add_row(
        "",
        "Please confirm this repository exists and that you can access it before attempting to use it.",
    )

    return table


def render_pull_request_table(
    title: str,
    pull_requests: List[PullRequest],
) -> Table:
    """Renders a list of pull requests as a table"""

    if pull_requests and pull_requests[0].repository_url:
        link = f"[link={pull_requests[0].repository_url}]{title}[/link]"
    else:
        link = f"{title}"

    table = Table(show_header=True, header_style="bold white")
    table.add_column("#", style="dim", width=8)
    table.add_column(link, width=55)
    table.add_column("Author", width=13)
    table.add_column("Labels", width=20)
    table.add_column("Activity", width=15)
    table.add_column("Approved", width=10)
    table.add_column("Ready", width=10)

    label_colour_map = get_label_colour_map()

    for pr in sorted(pull_requests, key=attrgetter("updated_at"), reverse=True):
        row = [
            f"[white]{pr.number} ",
            pr.render_title(),
        ]

        row.append(pr.render_author())
        row.append(pr.render_labels(label_colour_map))
        row.append(pr.render_updated_at())
        row.append(pr.render_approved())
        row.append(pr.render_approved_by_others())

        table.add_row(*row)

    return table
