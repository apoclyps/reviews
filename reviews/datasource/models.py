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
    draft: bool
    created_at: datetime
    updated_at: datetime
    approved: str
    approved_by_others: bool
    labels: List[Label] = field(default_factory=list)
