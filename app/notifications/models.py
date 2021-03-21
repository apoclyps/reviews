from dataclasses import dataclass
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


@dataclass
class PullRequestNotification:
    """Represents a pull request notification"""

    org: str
    repository: str
    name: str
    number: int

    def __repr__(self):
        return f"{self.org}/{self.repository} updated with {self.name}"
