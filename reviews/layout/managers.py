from rich.console import Console, Group
from rich.layout import Layout
from rich.panel import Panel

console = Console()


class RenderLayoutManager:
    """Renders the Layout for the Terminal UI"""

    def __init__(self, layout: Layout) -> None:
        self.layout = layout

    def render_layout(
        self,
        body: Panel,
        pull_request_component: Group,
    ) -> Layout:
        """Renders the entire layout"""
        self.render_body(component=body)

        self.render_configuration(component=pull_request_component)

        return self.layout

    def render_body(self, component: Panel) -> None:
        """Renders the Body component"""
        self.layout["body"].update(component)

    def render_configuration(self, component: Group) -> None:
        """Renders the Main Body component"""
        self.layout["configuration"].update(Panel(component, title="Configuration", border_style="blue"))
