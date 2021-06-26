import os
from unittest import mock

from reviews import config


@mock.patch.dict(os.environ, {"REVIEWS_GITHUB_REPOSITORY_CONFIGURATION": "apoclyps/reviews"})
def test_reviews_github_repository_configuration():
    configuration = config.get_configuration(config=config.REVIEWS_GITHUB_REPOSITORY_CONFIGURATION)

    assert configuration == [
        ("apoclyps", "reviews"),
    ]


@mock.patch.dict(os.environ, {"REVIEWS_GITLAB_REPOSITORY_CONFIGURATION": "27629846:apoclyps/reviews"})
def test_reviews_gitlab_repository_configuration():
    configuration = config.get_configuration(config=config.REVIEWS_GITLAB_REPOSITORY_CONFIGURATION)

    assert configuration == [
        ("27629846", "apoclyps/reviews"),
    ]
