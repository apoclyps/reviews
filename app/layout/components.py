from datetime import datetime

from rich.panel import Panel
from rich.table import Table


class Header:  # NOQA: R0903
    """Display header with clock."""

    def __rich__(self) -> Panel:  # NOQA: R0201
        grid = Table.grid(expand=True)
        grid.add_column(justify="center", ratio=1)
        grid.add_column(justify="right")
        grid.add_row(
            "[b]Code Review[/b] Manager",
            datetime.now().ctime().replace(":", "[blink]:[/]"),
        )
        return Panel(grid, style="white on blue")
