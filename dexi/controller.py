from dexi import config
from dexi.datasource.client import SQLClient
from dexi.datasource.managers import PullRequestManager
from dexi.layout.helpers import render_pull_request_table
from dexi.models import PullRequest
from dexi.source_control.client import GithubAPI


def retrieve_pull_requests(org, repository):
    """Renders Terminal UI Dashboard"""
    client = SQLClient(path=config.DATA_PATH, filename=config.FILENAME)
    manager = PullRequestManager(client=client)

    title = f"{org}/{repository}"
    pull_requests = update_pull_requests(org=org, repository=repository)

    if not pull_requests:
        return

    manager.insert_all(pull_requests=pull_requests)

    # TODO: add adapter to convert rows back into models
    all_pull_requests = manager.all()

    return render_pull_request_table(title=title, pull_requests=pull_requests)


def update_pull_requests(org, repository):
    """ Updates repository models."""
    client = GithubAPI()
    pull_requests = client.get_pull_requests(org=org, repo=repository)

    prs = []
    for pull_request in pull_requests:
        pr = PullRequest(
            number=pull_request.number,
            title=pull_request.title,
            created_at=pull_request.created_at,
            updated_at=pull_request.updated_at,
            approved=any([r for r in pull_request.get_reviews()]),
        )
        prs.append(pr)

    return prs
