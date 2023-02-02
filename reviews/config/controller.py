from typing import Dict, List

from rich.console import Console
from rich.table import Table


def render_config_table(configurations: List[Dict[str, str]]) -> None:
    """Renders a table using the supplied configuration."""
    table = Table()
    table.add_column("Name", style="white", no_wrap=True)
    table.add_column("Value", style="cyan")

    for configuration in configurations:
        table.add_row(configuration["name"], configuration["value"])

    console = Console()
    console.print(table)
