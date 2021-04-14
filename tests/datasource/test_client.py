from reviews.datasource.managers import pull_requests
from datetime import datetime

from freezegun import freeze_time
import pytest

from reviews.datasource.client import SQLClient
from reviews.datasource import PullRequestManager
from reviews.datasource import PullRequest, Label


@pytest.fixture
def manager(setup_database):
    client = SQLClient(connection=setup_database)
    manager = PullRequestManager(client=client)
    manager.create_table()
    yield manager


@pytest.fixture
@freeze_time("2020-01-01T00:00:00+00:00")
def pull_request():
    return PullRequest(
        number=1,
        title="[1] Initial Commit",
        created_at=datetime.now(),
        updated_at=datetime.now(),
        approved=False,
        labels=[Label(name="Python")],
    )


def test_table_created(manager):
    assert manager.exists() is True


def test_table_dropped(manager):
    manager.drop_table()

    assert manager.exists() is False


def test_insert(manager, pull_request):
    manager.insert(model=pull_request)

    assert len(manager.all()) == 1


def test_select_by_id(manager, pull_request):
    manager.insert(model=pull_request)

    results = manager.get_by_id(row_id=1)

    assert len(results) == 1


def test_bulk_insert(manager):
    manager.insert_all(
        models=[
            PullRequest(
                number=1,
                title="[1] Initial Commit",
                created_at=datetime.now(),
                updated_at=datetime.now(),
                approved=False,
                labels=[Label(name="Python")],
            ),
            PullRequest(
                number=2,
                title="[2] Adds README",
                created_at=datetime.now(),
                updated_at=datetime.now(),
                approved=False,
                labels=[Label(name="Python")],
            ),
        ]
    )

    assert len(manager.all()) == 2


def test_update(manager, pull_request):
    last_row_id = manager.insert(model=pull_request)

    pull_request.title = "[1] Initial setup of repository"
    manager.update(row_id=last_row_id, model=pull_request)

    assert len(manager.all()) == 1
    assert manager.get_by_id(row_id=last_row_id) == [
        (
            1,
            1,
            "[1] Initial setup of repository",
            "2020-01-01 00:00:00",
            "2020-01-01 00:00:00",
            0,
        )
    ]


def test_delete(manager, pull_request):
    manager.insert(model=pull_request)

    assert len(manager.all()) == 1

    manager.delete(row_id=1)

    assert len(manager.all()) == 0
