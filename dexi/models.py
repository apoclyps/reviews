from dataclasses import dataclass, field
from datetime import datetime
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
    created_at: datetime
    updated_at: datetime
    approved: bool
    labels: List[Label] = field(default_factory=list)
