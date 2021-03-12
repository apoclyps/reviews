from typing import List, Union

from rich.table import Table

from dexi import config
from dexi.datasource.client import SQLClient
from dexi.datasource.managers import PullRequestManager
from dexi.layout.helpers import render_pull_request_table
from dexi.models import Label, PullRequest
from dexi.source_control.client import GithubAPI


def retrieve_pull_requests(org: str, repository: str) -> Union[Table, None]:
    """Renders Terminal UI Dashboard"""
    client = SQLClient(path=config.DATA_PATH, filename=config.FILENAME)
    manager = PullRequestManager(client=client)

    title = f"{org}/{repository}"
    pull_requests = update_pull_requests(org=org, repository=repository)

    if not pull_requests:
        return None

    manager.insert_all(models=pull_requests)

    # TODO: add adapter to convert rows back into models
    # all_pull_requests = manager.all()

    return render_pull_request_table(title=title, pull_requests=pull_requests)


def update_pull_requests(org: str, repository: str) -> List[PullRequest]:
    """ Updates repository models."""
    client = GithubAPI()
    pull_requests = client.get_pull_requests(org=org, repo=repository)

    return [
        PullRequest(
            number=pull_request.number,
            title=pull_request.title,
            created_at=pull_request.created_at,
            updated_at=pull_request.updated_at,
            approved=any([r for r in pull_request.get_reviews()]),  # NOQA: R1721
            labels=[
                Label(name=label.name)
                for label in pull_request.get_labels()
                if label.name
            ],
        )
        for pull_request in pull_requests
    ]
