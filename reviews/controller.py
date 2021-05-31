from typing import Dict, List, Union

from github.PullRequest import PullRequest as ghPullRequest
from rich.table import Table

from . import config
from .errors import RepositoryDoesNotExist
from .layout import render_pull_request_table, render_repository_does_not_exist
from .source_control import GithubAPI, Label, PullRequest


class PullRequestController:
    """retrieve and store pull requests."""

    def __init__(self) -> None:
        self.client = GithubAPI()

    def retrieve_pull_requests(self, org: str, repository: str) -> Union[Table, None]:
        """Renders Terminal UI Dashboard"""

        title = f"{org}/{repository}"
        pull_requests = []
        try:
            pull_requests = self.update_pull_requests(org=org, repository=repository)
        except RepositoryDoesNotExist:
            return render_repository_does_not_exist(
                title=f"{title} does not exist",
                org=org,
                repository=repository,
            )

        if not pull_requests:
            return None

        return render_pull_request_table(
            title=title,
            pull_requests=pull_requests,
            org=org,
            repository=repository,
        )

    def update_pull_requests(self, org: str, repository: str) -> List[PullRequest]:
        """Updates repository models."""

        def _get_reviews(pull_request: ghPullRequest) -> Dict[str, str]:
            """Inner function to retrieve reviews for a pull request"""
            reviews = pull_request.get_reviews()
            res, seen = {}, []

            for review in reviews:
                if review.user.login in seen or review.state == "COMMENTED":
                    continue
                res[review.user.login] = review.state
                seen.append(review.user.login)
            return res

        pull_requests = self.client.get_pull_requests(org=org, repo=repository)

        code_review_requests = []
        for pull_request in pull_requests:

            reviews = _get_reviews(pull_request=pull_request)

            if pull_request.user.login == config.GITHUB_USER:
                approved_by_me = "AUTHOR"
            else:
                approved_by_me = reviews.get(config.GITHUB_USER, "")  # NOQA: R1721

            approved_by_others = any(
                [True for user, status in reviews.items() if user != config.GITHUB_USER and status == "APPROVED"]
            )
            labels = [Label(name=label.name) for label in pull_request.get_labels() if label.name]

            code_review_requests.append(
                PullRequest(
                    number=pull_request.number,
                    title=pull_request.title,
                    draft=pull_request.draft,
                    additions=pull_request.additions,
                    deletions=pull_request.deletions,
                    created_at=pull_request.created_at,
                    updated_at=pull_request.updated_at,
                    approved=approved_by_me,
                    approved_by_others=approved_by_others,
                    labels=labels,
                )
            )

        return code_review_requests
