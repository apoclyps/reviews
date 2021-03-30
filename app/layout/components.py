from datetime import datetime

from rich.panel import Panel
from rich.table import Table


class Header:
    """Display header with clock."""

    def __rich__(self) -> Panel:
        grid = Table.grid(expand=True)
        grid.add_column(justify="center", ratio=1)
        grid.add_column(justify="right")
        grid.add_row(
            "[b]Code Review[/b] Manager",
            datetime.now().ctime().replace(":", "[blink]:[/]"),
        )
        return Panel(grid, style="white on blue")
