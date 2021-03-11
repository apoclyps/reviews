from dataclasses import dataclass

from dexi.notifications.enums import Language

@dataclass
class PullRequestNotification:
    org: str
    repository: str
    name: str
    language: Language
