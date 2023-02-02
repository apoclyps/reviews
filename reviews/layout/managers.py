from rich.console import Console
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
    ) -> Layout:
        """Renders the entire layout"""
        self.render_body(component=body)

        return self.layout

    def render_body(self, component: Panel) -> None:
        """Renders the Body component"""
        self.layout["body"].update(component)
