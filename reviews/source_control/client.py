from typing import List

from github import Github
from github.GithubException import BadCredentialsException, UnknownObjectException
from github.PullRequest import PullRequest
from github.Repository import Repository

from .. import config
from ..errors import InvalidGithubToken, RepositoryDoesNotExist


class GithubAPI:
    """Create and execute requests using the Github API"""

    def __init__(self) -> None:
        self._client = Github(
            config.GITHUB_TOKEN,
            per_page=config.GITHUB_DEFAULT_PAGE_SIZE,
            base_url=config.GITHUB_URL,
        )

    def get_repository(self, org: str, repo: str) -> Repository:
        """Returns a repository for a given organization."""
        try:
            return self._client.get_repo(f"{org}/{repo}")
        except UnknownObjectException:
            raise RepositoryDoesNotExist(f"{org}/{repo} does not exist")
        except BadCredentialsException:
            raise InvalidGithubToken("GITHUB_TOKEN is not valid.")

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
