from enum import Enum, unique


@unique
class Sound(Enum):
    """Enum used to provide a mapping to sound files."""

    SUCCESS = "audio/success.wav"
    FAILURE = "audio/failure.wav"


@unique
class Language(Enum):
    """Enum used to provide a mapping to icon files."""

    PYTHON = "icon/python_icon.png"
    RUBY = "icon/ruby_icon.png"
    GO = "icon/go_icon.png"
    JAVASCRIPT = "icon/javascript_icon.png"
    TERRAFORM = "icon/terraform_icon.png"
