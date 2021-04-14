from typing import List

from github import Github
from github.PullRequest import PullRequest
from github.Repository import Repository

from reviews import config


class GithubAPI:
    """ create and maintain queries to the Github"""

    def __init__(self) -> None:
        self._client = Github(config.GITHUB_TOKEN, per_page=config.DEFAULT_PAGE_SIZE)

    def get_repository(self, org: str, repo: str) -> Repository:
        """Returns a repository for a given organization."""
        return self._client.get_repo(f"{org}/{repo}")

    @staticmethod
    def _get_pull_requests(
        repository: Repository,
        state: str = "open",
        sort: str = "created",
    ) -> List[PullRequest]:
        return list(repository.get_pulls(state=state, sort=sort))

    def get_pull_requests(self, org: str, repo: str) -> List[PullRequest]:
        """Returns a list of pull requests for a given organization and repository."""
        repository = self.get_repository(org=org, repo=repo)
        return self._get_pull_requests(repository=repository)
