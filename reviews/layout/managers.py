from rich.console import Console
from rich.panel import Panel

from reviews.layout.components import Header

console = Console()


class RenderLayoutManager:
    """Renders the Layout for the Terminal UI"""

    def __init__(self, layout):
        self.layout = layout

    def render_layout(
        self, progress_table, body, pull_request_component, log_component
    ):
        """Renders the entire layout"""
        self.render_header()
        self.render_body(component=body)
        self.render_log(component=log_component)
        self.render_configuration(component=pull_request_component)
        self.render_footer(progress_table=progress_table)

        return self.layout

    def render_header(self):
        """Renders the Header component"""
        self.layout["header"].update(Header())

    def render_body(self, component):
        """Renders the Body component"""
        self.layout["body"].update(component)

    def render_configuration(self, component):
        """Renders the Main Body component"""
        self.layout["configuration"].update(
            Panel(component, title="Configuration", border_style="blue")
        )

    def render_log(self, component):
        """Rends the log component"""
        self.layout["log"].update(Panel(component, title="Log", border_style="blue"))

    def render_review(self, component):
        """Renders the Review Side Body component"""
        self.layout["review"].update(
            Panel(component, title="Ready to Review", border_style="blue")
        )

    def render_shippable(self, component):
        """Renders the Shippable Side Body component"""
        self.layout["ship"].update(
            Panel(component, title="Ready to Ship", border_style="blue")
        )

    def render_footer(self, progress_table):
        """Renders the Footer component"""
        self.layout["footer"].update(progress_table)
