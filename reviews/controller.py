from datetime import datetime, timezone
from typing import Dict, List, Tuple, Union

from github.PullRequest import PullRequest as ghPullRequest
from gitlab.v4.objects.merge_requests import MergeRequest as GitlabMergeRequest
from rich.console import RenderGroup
from rich.panel import Panel
from rich.table import Table

from reviews.source_control.client import GitlabAPI

from . import config
from .errors import RepositoryDoesNotExist
from .layout import render_pull_request_table, render_repository_does_not_exist
from .source_control import GithubAPI, Label, PullRequest


class PullRequestController:
    """Abstract base class for providier specific pull request controllers"""

    def render(self, configuration: List[Tuple[str, str]]) -> Panel:
        """Renders all pull requests for the provided configuration"""
        raise NotImplementedError("the render method needs to be implemented for your specified provider")


class GithubPullRequestController(PullRequestController):
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
                title=title,
                link=f"https://www.github.com/{org}/{repository}",
            )

        if not pull_requests:
            return None

        return render_pull_request_table(
            title=title,
            pull_requests=pull_requests,
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
                    repository_url=f"https://www.github.com/{org}/{repository}",
                    link=f"https://www.github.com/{org}/{repository}/pull/{pull_request.number}",
                    additions=pull_request.additions,
                    deletions=pull_request.deletions,
                    created_at=pull_request.created_at.astimezone(tz=timezone.utc),
                    updated_at=pull_request.updated_at.astimezone(tz=timezone.utc),
                    approved=approved_by_me,
                    approved_by_others=approved_by_others,
                    labels=labels,
                )
            )

        return code_review_requests

    def render(self, configuration: List[Tuple[str, str]]) -> Panel:
        """Renders all pull requests for the provided configuration"""

        tables = [self.retrieve_pull_requests(org=org, repository=repo) for (org, repo) in configuration]

        # filter unrenderable `None` results
        return Panel(
            RenderGroup(*[t for t in tables if t]),
            title="Activity",
            border_style="blue",
        )


class GitlabPullRequestController(PullRequestController):
    """retrieve and store pull requests."""

    def __init__(self) -> None:
        self.client = GitlabAPI()

    def retrieve_pull_requests(self, project_id: str, namespace: str) -> Union[Table, None]:
        """Renders Terminal UI Dashboard"""
        pull_requests = []
        try:
            pull_requests = self.update_pull_requests(project_id=project_id, namespace=namespace)
        except RepositoryDoesNotExist:
            return render_repository_does_not_exist(
                title=namespace,
                link=f"https://gitlab.com/{namespace}",
            )

        if not pull_requests:
            return None

        return render_pull_request_table(
            title=namespace,
            pull_requests=pull_requests,
        )

    def update_pull_requests(self, project_id: str, namespace: str) -> List[PullRequest]:
        """Updates repository models."""

        def _get_reviews(pull_request: GitlabMergeRequest) -> Dict[str, str]:
            """Inner function to retrieve reviews for a pull request"""
            reviews = pull_request.approvals.get()

            return {reviewer["user"]["username"]: "approved" for reviewer in reviews.approvers}

        # ProjectMergeRequest
        pull_requests = self.client.get_pull_requests(project_id=project_id, namespace=namespace)

        code_review_requests = []
        for pull_request in pull_requests:

            reviews = _get_reviews(pull_request=pull_request)

            if pull_request.author["username"] == config.GITLAB_USER:
                approved_by_me = "AUTHOR"
            else:
                approved_by_me = reviews.get(config.GITLAB_USER, "")  # NOQA: R1721

            approved_by_others = any(
                [True for user, status in reviews.items() if user != config.GITLAB_USER and status == "APPROVED"]
            )

            def get_labels(labels: List[str]) -> List[Label]:
                visible_labels = []
                labels_mapping = {label: len(label) for label in labels}

                current_size = 0
                max_size = 18
                hidden_labels = 0
                for label, size in labels_mapping.items():
                    if current_size == 0:
                        current_size += size
                        visible_labels.append(label)
                        continue

                    if current_size + size < max_size:
                        current_size += size
                        visible_labels.append(label)
                    else:
                        hidden_labels += 1

                labels = [Label(name=label) for label in visible_labels]

                if hidden_labels:
                    labels.append(Label(name=f"+{hidden_labels} others"))

                return labels

            labels = get_labels(labels=pull_request.labels)

            link = pull_request.web_url

            code_review_requests.append(
                PullRequest(
                    number=pull_request.iid,
                    title=pull_request.title,
                    draft=pull_request.draft,
                    additions=0,
                    deletions=0,
                    link=link,
                    repository_url=link.split("/-/")[0],
                    created_at=datetime.strptime(pull_request.created_at, "%Y-%m-%dT%H:%M:%S.%f%z"),
                    updated_at=datetime.strptime(pull_request.updated_at, "%Y-%m-%dT%H:%M:%S.%f%z"),
                    approved=approved_by_me,
                    approved_by_others=approved_by_others,
                    labels=labels,
                )
            )

        return code_review_requests

    def render(self, configuration: List[Tuple[str, str]]) -> Panel:
        """Renders all pull requests for the provided configuration"""

        tables = [
            self.retrieve_pull_requests(project_id=project_id, namespace=namespace)
            for (project_id, namespace) in configuration
        ]

        # filter unrenderable `None` results
        return Panel(
            RenderGroup(*[t for t in tables if t]),
            title="Activity",
            border_style="blue",
        )
