from dataclasses import dataclass, field
from typing import List


@dataclass
class Label:
    """Labels on a Pull Request."""

    name: str


@dataclass
class PullRequest:
    """Models a Pull Request"""

    number: int
    title: str
    created_at: str
    updated_at: str
    approved: bool
    labels: List[Label] = field(default_factory=list)
