import os

from decouple import Csv, config

from reviews import config as application_config


def test_repository_configuration():
    os.environ[
        "REPOSITORY_CONFIGURATION"
    ] = "apoclyps/reviews, apoclyps/my-dev-space, apoclyps/magic-home"

    application_config.REPOSITORY_CONFIGURATION = config(
        "REPOSITORY_CONFIGURATION",
        cast=Csv(),
    )
    configuration = application_config.get_configuration()

    assert configuration == [
        ("apoclyps", "reviews"),
        ("apoclyps", "my-dev-space"),
        ("apoclyps", "magic-home"),
    ]
