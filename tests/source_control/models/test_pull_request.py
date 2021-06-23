from datetime import datetime, timezone
from typing import Dict

import pytest
from freezegun import freeze_time

from reviews.source_control import PullRequest, Label


@pytest.fixture
def organization() -> str:
    return "my-org"


@pytest.fixture
def repository() -> str:
    return "my-repo"


@pytest.fixture
def label_colour_map() -> Dict[str, str]:
    return {"python": "[green]"}


@pytest.fixture
@freeze_time("2020-01-01T00:00:00+00:00")
def pull_request(organization, repository) -> PullRequest:
    return PullRequest(
        number=1,
        draft=True,
        repository_url=f"https://www.github.com/{organization}/{repository}",
        link=f"https://www.github.com/{organization}/{repository}/pull/1",
        title="[1] Initial Commit",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
        approved="",
        approved_by_others=False,
        labels=[Label(name="Python")],
    )


@pytest.mark.parametrize(
    "approved, expected",
    [
        ("", ""),
        ("APPROVED", "[green]Approved[/]"),
        ("CHANGES_REQUESTED", "[red]Changes Requested[/]"),
    ],
)
def test_pull_request_renders_approved(pull_request, approved, expected):
    pull_request.approved = approved
    rendered = pull_request.render_approved()
    assert rendered == expected


@pytest.mark.parametrize(
    "approved_by_others, expected",
    [
        (False, ""),
        (True, "[green]Ready[/]"),
    ],
)
def test_pull_request_renders_approved_by_others(pull_request, approved_by_others, expected):
    pull_request.approved_by_others = approved_by_others
    rendered = pull_request.render_approved_by_others()
    assert rendered == expected


@pytest.mark.parametrize(
    "labels, expected",
    [
        ([Label(name="Python")], "[green]Python[/]"),
        ([Label(name="Enhancement")], "[white]Enhancement[/]"),
        (
            [Label(name="Python"), Label(name="Enhancement")],
            "[green]Python[/], [white]Enhancement[/]",
        ),
    ],
)
def test_pull_request_renders_labels(pull_request, label_colour_map, labels, expected):
    pull_request.labels = labels
    rendered = pull_request.render_labels(label_colour_map)
    assert rendered == expected


@pytest.mark.parametrize(
    "title, draft, expected",
    [
        ("[1] Initial Commit", False, "[white]"),
        ("[Security][1] Initial Commit", False, "[bold red][Security][/][white]"),
        ("[1] Initial Commit", True, "[bold grey][Draft][/] [white]"),
        (
            "[Security][1] Initial Commit",
            True,
            "[bold red][Security][/][bold grey][Draft][/] [white]",
        ),
    ],
)
def test_pull_request_renders_title(pull_request, organization, repository, title, draft, expected):
    pull_request.draft = draft
    pull_request.title = title
    rendered = pull_request.render_title()
    assert rendered.startswith(expected)


@pytest.mark.parametrize(
    "since, expected",
    [
        (datetime(2020, 1, 2).astimezone(tz=timezone.utc), "[yellow]a day ago[/]"),
        (datetime(2020, 1, 8).astimezone(tz=timezone.utc), "[red]7 days ago[/]"),
    ],
)
def test_pull_request_renders_updated_at(pull_request, since, expected):
    rendered = pull_request.render_updated_at(since=since)
    assert rendered == expected
