from typing import List

from github import Github
from github.GithubException import BadCredentialsException, UnknownObjectException
from github.PullRequest import PullRequest
from github.Repository import Repository
from gitlab import Gitlab
from gitlab.v4.objects.merge_requests import MergeRequest as GitlabMergeRequest
from gitlab.v4.objects.projects import Project as GitlabRepository

from .. import config
from ..errors import InvalidGithubToken, InvalidGitlabToken, RepositoryDoesNotExist


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


class GitlabAPI:
    """Create and execute requests using the Gitlab API"""

    def __init__(self) -> None:
        self._client = Gitlab(url=config.GITLAB_URL, private_token=config.GITLAB_TOKEN)

    def get_repository(self, project_id: str, namespace: str) -> GitlabRepository:
        """Returns a repository for a given organization."""
        try:
            return self._client.projects.get(id=project_id)  # type: ignore
        except UnknownObjectException:
            raise RepositoryDoesNotExist(f"{project_id} does not exist for {namespace}")
        except BadCredentialsException:
            raise InvalidGitlabToken("GITLAB_TOKEN is not valid.")

    @staticmethod
    def _get_pull_requests(
        repository: Repository,
        state: str = "open",
        sort: str = "created",
    ) -> List[PullRequest]:
        return list(repository.get_pulls(state=state, sort=sort))

    def get_pull_requests(self, project_id: str, namespace: str) -> List[GitlabMergeRequest]:
        """Returns a list of pull requests for a given organization and repository."""
        repository = self.get_repository(project_id=project_id, namespace=namespace)
        return repository.mergerequests.list(state="opened", order_by="created_at", sort="asc")  # type: ignore
