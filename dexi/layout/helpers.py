import humanize
from rich.layout import Layout
from rich.table import Table
from rich.text import Text
from rich.tree import Tree


def render_pull_request_table(pull_requests):
    table = Table(show_header=True, header_style="bold white")
    table.add_column("#", style="dim", width=4)
    table.add_column("Title", width=10)
    table.add_column("Latest Activity")
    table.add_column("Approved")

    for pr in pull_requests:
        approved = any([r for r in pr.get_reviews()])
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
        Layout(name="side"),
        Layout(name="body", ratio=2, minimum_size=60),
        Layout(name="right_side"),
        direction="horizontal",
    )
    layout["side"].split(Layout(name="pull_requests"))
    layout["right_side"].split(Layout(name="review"), Layout(name="ship"))
    return layout


def generate_tree_layout(workspace, tree):
    if not tree:
        tree = Tree(f"[white]{workspace}")

    def build_tree(workspace, tree):
        icon = "🐍 Contains: Python"
        dexi_tree = tree.add(workspace)

        pr_tree = dexi_tree.add("[123123] Update something in the code")
        pr_tree.add(Text(icon))

        pr_tree = dexi_tree.add("[312312] Revert everything")
        pr_tree.add(Text(icon))

        return tree

    tree = build_tree(workspace=workspace, tree=tree)

    return tree
