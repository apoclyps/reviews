import dataclasses

from reviews.notifications import PullRequestNotification


def test_model_with_required_fields():
    model = PullRequestNotification(
        org="apoclyps",
        repository="Reviews",
        name="Pull Request Approved",
        number=1,
    )

    assert dataclasses.asdict(model) == {
        "org": "apoclyps",
        "repository": "Reviews",
        "name": "Pull Request Approved",
        "number": 1,
    }
