import os
from unittest import mock

from reviews import config


@mock.patch.dict(os.environ, {"REPOSITORY_CONFIGURATION": "apoclyps/reviews"})
def test_repository_configuration():
    configuration = config.get_configuration()

    assert configuration == [
        ("apoclyps", "reviews"),
    ]
