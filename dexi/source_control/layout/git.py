import asyncio
from github import Github
from rich.table import Table
import humanize


from dexi.source_control.client import GithubAPI


async def get_repos(layout):
    await asyncio.sleep(1)

    table = Table(show_header=True, header_style="bold white")
    table.add_column("#", style="dim", width=4)
    table.add_column("Title")
    table.add_column("Created At")
    table.add_column("Updated At")
    table.add_column("Approved")

    repo = GithubAPI().get_repository(org="slicelife", repo="ros-service")
    pulls = GithubAPI().get_pull_requests(
        repository=repo, state="open", sort="created", base="master"
    )

    for pr in pulls:
        approved = any([r for r in pr.get_reviews()])
        created_at = humanize.naturaltime(pr.created_at)
        updated_at = humanize.naturaltime(pr.updated_at)

        table.add_row(
            f"[white]{pr.number} ",
            f"[red]{pr.title}",
            f"{created_at}",
            f"{updated_at}",
            f"{approved}",
        )

    return table
