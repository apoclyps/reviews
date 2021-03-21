import dataclasses

from app.notifications import PullRequestNotification


def test_model_with_required_fields():
    model = PullRequestNotification(
        org="apoclyps",
        repository="Code Review Manager",
        name="Pull Request Approved",
        number=1,
    )

    assert dataclasses.asdict(model) == {
        "org": "apoclyps",
        "repository": "Code Review Manager",
        "name": "Pull Request Approved",
        "number": 1,
    }
