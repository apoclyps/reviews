from dataclasses import dataclass


@dataclass
class PullRequest:
    """Models a Pull Request"""

    number: int
    title: str
    created_at: str
    updated_at: str
    approved: bool
