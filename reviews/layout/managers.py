from typing import Optional

from rich.console import Console, RenderGroup
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table

from ..layout.components import Header

console = Console()


class RenderLayoutManager:
    """Renders the Layout for the Terminal UI"""

    def __init__(self, layout: Layout) -> None:
        self.layout = layout

    def render_layout(
        self,
        body: Panel,
        pull_request_component: RenderGroup,
        log_component: Optional[Table],
        progress_table: Optional[Table],
    ) -> Layout:
        """Renders the entire layout"""
        self.render_header()
        self.render_body(component=body)
        if log_component:
            self.render_log(component=log_component)
        self.render_configuration(component=pull_request_component)
        if progress_table:
            self.render_footer(progress_table=progress_table)

        return self.layout

    def render_header(self) -> None:
        """Renders the Header component"""
        self.layout["header"].update(Header())

    def render_body(self, component: Panel) -> None:
        """Renders the Body component"""
        self.layout["body"].update(component)

    def render_configuration(self, component: RenderGroup) -> None:
        """Renders the Main Body component"""
        self.layout["configuration"].update(Panel(component, title="Configuration", border_style="blue"))

    def render_log(self, component: Table) -> None:
        """Rends the log component"""
        self.layout["log"].update(Panel(component))

    def render_footer(self, progress_table: Table) -> None:
        """Renders the Footer component"""
        self.layout["footer"].update(progress_table)
