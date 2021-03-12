from dataclasses import dataclass

from dexi.notifications.enums import Language


@dataclass
class PullRequestNotification:
    """Represents a pull request notification"""

    org: str
    repository: str
    name: str
    language: Language

    def __repr__(self):
        return f"A {self.language} notification has been sent for {self.org}/{self.repository}: {self.name}"
