from typing import Optional

import humanize
from github.Repository import Repository
from rich.console import Console
from rich.table import Table

from ..config import REVIEWS_GITHUB_REPOSITORY_CONFIGURATION, get_configuration
from ..errors import RepositoryDoesNotExist
from ..source_control import GithubAPI


def repository_metrics() -> None:
    """Renders an aggregated table view displaying contributors by contributors
    for the lifetime of a repository.
    """
    console = Console()

    for org, repo in get_configuration(config=REVIEWS_GITHUB_REPOSITORY_CONFIGURATION):
        client = GithubAPI()
        repository: Optional[Repository] = None
        try:
            repository = client.get_repository(org=org, repo=repo)
        except RepositoryDoesNotExist:
            continue

        console.print()
        table = Table(title=f"Repository Activity for {org}/{repo}")
        table.add_column("User", no_wrap=True, width=25)
        table.add_column("Additions", width=10)
        table.add_column("Deletions", width=10)
        table.add_column("Commits", width=10)

        if repository:
            for contributor in repository.get_stats_contributors():  # type: ignore
                name = contributor.author.name
                if not name:
                    continue

                additions = 0
                deletions = 0
                commits = 0
                for week in contributor.weeks:
                    additions += week.a
                    deletions += week.d
                    commits += week.c

                additions = f"[green]+{humanize.intcomma(additions)}[/]"
                deletions = f"[red]-{humanize.intcomma(deletions)}[/]"
                commits = f"[white]{humanize.intcomma(commits)}[/]"

                table.add_row(name, additions, deletions, commits)

        console.print(table)
        console.print()
