from unittest.mock import patch

import pytest

from reviews.notifications import PullRequestNotification
from reviews.notifications import NotificationClient


@pytest.fixture
def client() -> NotificationClient:
    return NotificationClient()


@pytest.fixture
def pull_request() -> PullRequestNotification:
    return PullRequestNotification(
        org="apoclyps",
        repository="Reviews",
        name="Pull Request Approved",
        number=1,
    )


@patch("notifypy.Notify.send")
def test_sending_reviewed_pull_request(mock_notify_client, client, pull_request):
    client.send_pull_request_review(pull_request)

    mock_notify_client.assert_called_once()


@patch("notifypy.Notify.send")
def test_sending_approved_pull_request(mock_notify_client, client, pull_request):
    client.send_pull_request_approved(pull_request)

    mock_notify_client.assert_called_once()


@patch("notifypy.Notify.send")
def test_sending_merged_pull_request(mock_notify_client, client, pull_request):
    client.send_pull_request_merged(pull_request)

    mock_notify_client.assert_called_once()
