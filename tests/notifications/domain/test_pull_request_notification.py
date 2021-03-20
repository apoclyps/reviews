import dataclasses

from dexi.notifications import PullRequestNotification
from dexi.notifications import Language


def test_model_with_required_fields():
    model = PullRequestNotification(
        org="apoclyps",
        repository="Code Review Manager",
        name="Pull Request Approved",
        language=Language.PYTHON,
        number=1,
    )

    assert dataclasses.asdict(model) == {
        "org": "apoclyps",
        "repository": "Code Review Manager",
        "name": "Pull Request Approved",
        "language": Language.PYTHON,
        "number": 1,
    }
